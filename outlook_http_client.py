import requests
import json
import os, sys
import uuid
import re

def print_err(message):
    if(message is not None):
        sys.stderr.write(message+'\n')

class LinkedInCrawler:
    def __init__(self):
        self.token = None


    def get_token(self):
        """
        Extract the session token from the file token.txt
        """
        
        if(self.token is None):
            with open("token.txt","r") as f:
                content = f.read()
                #print(content)
                result = re.compile(".*Bearer ([^\"]+).*").search(content)
                
                if result is not None:
                    self.token = result.group(1)
                else:
                    print_err("Bearer token not found in token.txt")
                    exit()
        
        return self.token

    def query_profile(self,session, email, token):

        authHeader = "Bearer "+token

        #Smtp
        paramsGet = {"AadObjectId":"","Smtp":email,"OlsPersonaId":"","UserPrincipalName":"","RootCorrelationId":str(uuid.uuid4()),"CorrelationId":str(uuid.uuid4()),"ClientCorrelationId":str(uuid.uuid4()),"PersonaDisplayName":"","UserLocale":"en-US","ExternalPageInstance":"00000000-0000-0000-0000-000000000000","PersonaType":"User"}
        headers = {"Authorization":authHeader,"X-ClientFeature":"LivePersonaCard","Accept":"text/plain, application/json, text/json","X-ClientType":"OwaMail","X-HostAppCapabilities":"{}","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0","Connection":"close","X-LPCVersion":"1.20210418.1.0"}
        response = session.get("https://sfnam.loki.delve.office.com/api/v1/linkedin/profiles/full", params=paramsGet, headers=headers)

        #print("Response body: {}".format(response.content))
        
        #resp = json.loads(response.content)
        has_profile = "displayName" in response.text
        print_err(" [+] {}: {}".format(email, "Found" if has_profile else "Not Found"))
        

        if(has_profile):
            person_json = self.extract_person_from_json(response.text)
            print(email+"|"+person_json)
            summary = self.display_summary(response.text)
            if(summary != ""):
                print_err(" [+] Summary: {}".format(summary))

        return has_profile

    def extract_person_from_json(self,response_json):
        data_json = json.loads(response_json)
        if("persons" in data_json and len(data_json['persons']) > 0):
            return json.dumps(data_json["persons"][0])
        else:
            return "{}"
        
    def display_summary(self,response_json):
        data_json = json.loads(response_json)
        if("persons" in data_json and len(data_json['persons']) > 0):
            p = data_json["persons"][0]
            
            displayName = p["displayName"] if "displayName" in p else ""
            headline    = p["headline"]    if "headline" in p else ""
            companyName = p["companyName"] if "companyName" in p else ""
            location    = p["location"]    if "location" in p else ""
            
            return "{}, \"{}\" at \"{}\", \"{}\"".format(displayName,headline,companyName, location)
        else:
            return ""

    def parse_emails(self,file_input,skip_email):
        """
        Loop over the email list and handle errors.
        
        file_input: File with emails listed
        skip_email: The file will be parsed starting from this email (included)
        """
        
        nb_failures = 0
        nb_queries = 0
        skip_found = skip_email == ""

        if(skip_email != ""):
            print_err("Skipping to {}".format(skip_email))

        with open(file_input,"r") as file:

            session = requests.Session()

            i = 0
            for line in file:

                if "," in line:
                    line = line.split(",",2)[1]
                current_email = line.strip()


                if(skip_email != "" and not(skip_found)):
                    if(current_email == skip_email):
                        print_err("Found !")
                        skip_found = True
                    else:
                        continue


                #res = False
                
                token = self.get_token()
                
                if(token is None):
                    print("Missing token")
                    exit(-1)
                
                res = self.query_profile(session, current_email, token)
                nb_queries +=1
                #print_err(" [+] Nb queries {} ".format(nb_queries))
                
                if(res):
                    nb_failures = 0
                else:
                    nb_failures += 1
                    print_err(" [!] Nb failures: {}".format(nb_failures))

                if(nb_failures == 10):
                    print_err("Max failures reached. Exiting..")
                    exit(-2)

                i+=1


if __name__ == "__main__":

    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    #Instruction displayed when no argument are given
    if(len(sys.argv)<2):
        print_err("Missing argument.")
        print_err("python "+os.path.basename(__file__)+" <<file_input>>")
        exit()
    
    file_input = sys.argv[1]
    skip_email = sys.argv[2] if len(sys.argv) >= 3 else ""
    
    LinkedInCrawler().parse_emails(file_input,skip_email)
    
    
    #print("Token: {}".format(LinkedInCrawler().get_token()))

