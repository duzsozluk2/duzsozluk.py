import requests
from bs4 import BeautifulSoup

def find_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('form')

def submit_form(form, url, value):
    action = form.get('action')
    post_url = url + action
    method = form.get('method')
    inputs = form.find_all('input')
    data = {}

    for input in inputs:
        if input.get('type') == 'text' or input.get('type') == 'search':
            data[input.get('name')] = value
        else:
            data[input.get('name')] = input.get('value')

    if method == 'post':
        return requests.post(post_url, data=data)
    else:
        return requests.get(post_url, params=data)

def sqli_test(url):
    forms = find_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        is_vulnerable = False
        for c in "\"'":
            response = submit_form(form, url, c)
            if "error" not in response.text.lower():
                is_vulnerable = True
                print(f"[!] SQL Injection vulnerability detected on {url}")
                print(f"[*] Form details:")
                print(form)
                break
        if not is_vulnerable:
            print(f"[-] No SQL Injection vulnerability detected on {url}")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    sqli_test(target_url)
