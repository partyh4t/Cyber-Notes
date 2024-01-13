# Forest
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/b5f78c88-9502-468b-87ee-63a6895921f8)


## 0) Machine Overview
- 


1. [Scans](#1-scans)
2. [LDAP Enumeration](#2-ldap-enumeration)
3. [AS-REPRoasting](#3-as-reproasting)
4. [Privilege Escalation](#4-privilege-escalation)

## 1) Scans

![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/d2c3fec9-46e2-47a4-a390-8206f8f15406)

Seems like we're going to be interacting with Active Directory. After some enumeration and help from HackTricks, we find that the Domain is susceptible to anonymous binding, which allows us to enumerate/query LDAP for all kinds of information. Most importantly, we want to look for users.

## 2) LDAP Enumeration
We first use ldapsearch: (Here I specified CN=users to gather some user information, which with this command it didn't prove too useful. However, the command in and of itself proves that anonymous bind works. Check [HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ldap#windapsearch) for more on syntax and tool usage)

(Turns out ldapsearch is useful, but the reason certain users didnt show up was because the actual users were not in CN=Users, but rather in OU=Employees. Although we'll just use windapsearch in this case as its easier to filter through.)
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/30e331fd-8e4a-48bf-94a1-053ad8c549a1)

We can see some actual users:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/6fe0f74c-27e8-432b-a37c-2049b98c150e)

Now that we have a list of users, lets see if any users do not have the "Kerberos Pre-Authentication Required" ***(DONT_REQ_PREAUTH)*** attribute. 

What we're about to do is called AS-REPRoasting.


## 3) AS-REPRoasting

Now we can use a tool called GetNPUsers.py that will do this for us. (If confused, check link up above). 
We can either give a list of usernames along with the domain:
```
python GetNPUsers.py jurassic.park/ -usersfile usernames.txt -format hashcat -outputfile hashes.asreproast
```

Or we can supply credentials and let the tool automatically grab us a list of users:
```
python GetNPUsers.py jurassic.park/triceratops:Sh4rpH0rns -request -format hashcat -outputfile hashes.asreproast
```

In our case, since we know anonymous-bind is enabled, we can provide no credentials and still have the tool retrieve the users for us: (Don't need '':'')
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/c440b8ef-b48c-4b56-9e0f-c15d6f9f3508)

That means now we can try and crack svc-alfrescos password offline.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/467c0264-c86e-4b36-bbd2-a71c9f2b2f6d)

Now that we have credentials, we can look back to the services that are open, and see which way may want to connect.

WinRM's is open, we can try evil-winrm:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/cf34fe7c-e148-4019-b7fd-69235928e8ef)

How about Psexec since SMB is open? 
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/997d6eb6-d93c-4633-9187-efc28b389796)

No luck. In any case, we have a foothold. Let's begin with some enumeration via BloodHound. 


## 4) Privilege Escalation

For this, I uploaded SharpHound.ps1 via WinRM, but i couldn't get it to work properly. So let's try the python ingester:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/cd4f70d1-9c76-4757-a1d1-8cdcdbb63b68)

Now we should input that into bloodhound. With some reseach we can find some documentation on the privilege that svc-alfresco has.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/782628fe-86db-41a8-93c3-887ee876ab07)

We basically just need to create a user, add him to the "Exchange Windows Permissions", which then he can give himself DCSync Rights/privileges that will allow us to then use that user to perform a DCSync attack.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/3bac2a69-e7a5-4982-9096-cbe4e910f3eb)

Lets add our user:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/bf0f7610-90d2-4dfb-82fa-5c6245f27836)

Now, he just needs to give himself DC-Sync rights, which we can do with powerview:
(NOTE: BloodHound actually ***shows*** you whow to exploit it if u select the help option when u right click on a path.)
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/571e1675-2ddc-4f76-ac4b-13e2bb74e337)

First, since it seems some kind of AV is not letting us run scripts from the disk, we'll need to import it to memory and run it:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/1adc2335-cdd0-4c24-824d-25750c1c0374)

Now that it is running in memory, we need to now give our user "bob" DCSync privileges:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/be50c0c2-6188-434a-95a3-b5f9ee675293)

Now that thats done, we simply can run secretsdump.py, which will remotely do it for us:
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/8eeaf7c1-e478-4d71-99db-71412e9d3a88)

Now we can just PtH, either through Psexec or WinRM.
![image](https://github.com/partyh4t/Cyber-Notes/assets/114421293/f1090b2b-4b6e-4abb-888a-047b23ef3e92)

Pwned.






















