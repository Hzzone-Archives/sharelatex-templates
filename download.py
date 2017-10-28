import requests
import re
import itertools
import time
import json
import os
import urllib.parse

BASE_URL = "http://cn.sharelatex.com"

'''
local proxy
'''
proxy = '127.0.0.1:1087'

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


class Template(object):
    def __init__(self, category, name, download_url, pic_url):
        self.category = category
        self.name = name
        self.download_url = download_url
        self.pic_url = pic_url

    def __repr__(self):
        return repr((self.name, self.category, self.pic_url, self.download_url))


def get_templates_by_category(TEMPLATE_URL):
    response = None
    while not response:
        try:
            response = requests.get(TEMPLATE_URL, timeout=5, headers=head)
        except:
            try:
                response = requests.get(TEMPLATE_URL, timeout=5, headers=head, proxies={"http": "http://{}".format(proxy)})
            except:
                print("Connection refused by the server.. Waiting for next connection.")
                time.sleep(30)
                continue
    pattern = re.compile(r'<a href="/templates/(.+?)">')
    match_result = re.findall(pattern=pattern, string=str(response.content))
    category_result = [TEMPLATE_URL+"/"+url for url in set(match_result)]
    print("-"*20)
    print("all category complete")
    print(category_result)
    print("all category complete")
    print("-"*20)
    return category_result

def get_templates_concrete_url(TEMPLATE_CATEGORY_URL):
    response = None
    while not response:
        try:
            response = requests.get(TEMPLATE_CATEGORY_URL, timeout=5, headers=head)
        except:
            try:
                response = requests.get(TEMPLATE_CATEGORY_URL, timeout=5, headers=head, proxies={"http": "http://{}".format(proxy)})
            except:
                print("Connection refused by the server.. Waiting for next connection.")
                time.sleep(30)
                continue
    pattern = re.compile(r'<a class="thumbnail" href="(.+?)">')
    match_result = re.findall(pattern=pattern, string=str(response.content))
    all_category_template_result = [BASE_URL + url for url in set(match_result)]
    for template in all_category_template_result:
        temp = template.split("/")
        name = temp[-1]
        name = urllib.parse.unquote(name).replace('-', ' ')
        category = temp[-2]
        save_dir = os.path.join(category, name)
        if os.path.exists(save_dir) and len(os.listdir(save_dir)) == 2:
            all_category_template_result.remove(template)
    print("-"*20)
    print("get template of category complete")
    print(len(all_category_template_result), all_category_template_result)
    print("get template of category complete")
    print("-"*20)
    return all_category_template_result

def get_each_template_info(EACH_TEMPLATE_URL):
    response = None
    while not response:
        try:
            response = requests.get(EACH_TEMPLATE_URL, timeout=5, headers=head)
        except:
            # print("Connection refused by the server.. Waiting for next connection.")
            # time.sleep(30)
            try:
                response = requests.get(EACH_TEMPLATE_URL, timeout=5, headers=head, proxies={"http": "http://{}".format(proxy)})
            except:
                print("Connection refused by the server.. Waiting for next connection.")
                time.sleep(30)
                continue

            # continue
    temp = EACH_TEMPLATE_URL.split("/")
    name = temp[-1]
    name = urllib.parse.unquote(name).replace('-', ' ')
    category = temp[-2]
    pattern = re.compile(r'<div class="col-md-12 template-large-pdf-preview">(.+?)</div>')
    match_result = re.findall(pattern=pattern, string=str(response.content))

    pattern = re.compile(r'<img src="(.+?)"')
    match_result = [re.findall(pattern=pattern, string=str(result)) for result in set(match_result)]
    pic = list(itertools.chain.from_iterable(match_result))[0]
    pattern = re.compile(r'<a class="btn btn-default" href="(.+?)"')
    match_result = re.findall(pattern=pattern, string=str(response.content))
    download_url = BASE_URL + list(set(match_result))[0]
    print(category, name, download_url, pic)
    template = Template(name=name, pic_url=pic, download_url=download_url, category=category)
    category = template.category
    download_url = template.download_url
    name = template.name
    pic = template.pic_url
    if not os.path.exists(category):
        os.mkdir(category)
    save_dir = os.path.join(category, name)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    save_pic_path = os.path.join(save_dir, name+".jpg")
    save_zip_path = os.path.join(save_dir, name+".zip")
    if not os.path.exists(save_pic_path):
        download_file(pic, save_pic_path)
    if not os.path.exists(save_zip_path):
        download_file(download_url, save_zip_path)
    return template

def dump_to_json(target="./template.json"):
    all_category = get_templates_by_category(BASE_URL+"/templates")
    all_templates = [get_templates_concrete_url(each_category) for each_category in all_category]
    all_templates = set(list(itertools.chain.from_iterable(all_templates)))
    all_templates = [get_each_template_info(each_template) for each_template in all_templates]
    s = json.dumps(all_templates, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    with open(target, "w") as f:
        f.write(s)
    print("Template download information has been written to " + target)

def download_file(url, save_path):
    response = None
    while not response:
        try:
            response = requests.get(url, timeout=5, headers=head)
        except:
            # print("Connection refused by the server.. Waiting for next connection.")
            # time.sleep(30)
            try:
                response = requests.get(url, timeout=5, headers=head, proxies={"http": "http://{}".format(proxy)})
            except:
                print("Connection refused by the server.. Waiting for next connection.")
                time.sleep(30)
                continue

    response.raise_for_status()
    save_file = open(save_path, 'wb')
    for chunk in response.iter_content(100000):
        save_file.write(chunk)
    print("Download %s complete!" % save_path)
    save_file.close()

def download():
    dump_to_json()

if __name__ == "__main__":
    download()
