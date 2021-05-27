# LinkedIn Email OSINT

This repository host a small proof-of-concept that deanonymize emails.

## How to use

The script can be launched this way. The output was masked on purpose for demonstration.

```
>python outlook_http_client.py samples_demo.txt > profiles_demo.json
 [+] *******@yahoo.com: Not Found
 [!] Nb failures: 1
 [+] *******@gmail.com: Found
 [+] Summary: Paul *******, "Attorney and Counsel" at "*******", "Waltham, Massachusetts, United States"
 [+] *******@hotmail.com: Found
 [+] Summary: David *******, "Engineering Specialist*******" at "*******", "Greater McAllen Area"
 [+] *******@libero.it: Found
 [+] Summary: antonio *******, "******* Professional" at "*******", "Naples, Campania, Italy"
 [+] *******@hotmail.com: Not Found
 [!] Nb failures: 1
 [+] *******@soton.ac.uk: Found
 [+] Summary: Tom *******, "Student *******" at "", "Southampton, England, United Kingdom"
 [+] *******@yahoo.com: Found
 [+] Summary: Madhukar *******, "Financial Crimes*******" at "*******", "New York City Metropolitan Area"
 [+] *******@inmovement.org: Not Found
 [!] Nb failures: 1
 [+] *******@hotmail.com: Found
 [+] Summary: Shaun *******, "Strategic *******" at "*******", "Bismarck, North Dakota, United States"
```

The `stdout` will include the complete LinkedIn profile in a JSON format.

The output json include the following fields:
 - companyName
 - displayName
 - headline
 - id
 - linkedInUrl
 - location
 - photoUrl
 - positions
 - schools
 - summary

Their are few other _less interesting_ fields:

 - locale
 - connectionCount
 - connectionDegree
 - connectionStatus
 - newsMentions
 - reportProfileUrl
 - skillEndorsements
 - skills
