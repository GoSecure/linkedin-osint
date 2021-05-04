# LinkedIn Email OSINT

This repository host a small proof-of-concept that deanonymize emails.

## How to use

The script can be launched this way. The output was masked on purpose for demonstration.

```
>python3 outlook_http_client.py email_list.txt  > profiles.json 
[+] r*********@fly.virgin.com: Not Found 
[!] Nb failures: 1 
[+] k*********@*********.com: Found 
[+] j*********@*********.com: Not Found 
[!] Nb failures: 2 
[+] v*********@yahoo.com: Not Found 
[!] Nb failures: 3 
[+] d*********@sympatico.ca: Found 
[+] ********@*********.ca: Not Found 
[!] Nb failures: 1 
[+] s*********@*********.com: Found 
[+] *********@gmail.com: Not Found 
[!] Nb failures: 1 
```
