import requests
import re
import itertools
import json
import os
import urllib.parse
import threading
import time
import random

BASE_URL = "http://cn.sharelatex.com"

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def get_response(URL):
    response = None
    while not response:
        proxy_url = "http://127.0.0.1:8000/"
        r = requests.get(proxy_url)
        ip_ports = json.loads(r.text)
        proxy = random.choice(ip_ports)
        ip = proxy[0]
        port = proxy[1]
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        try_time = 3
        for i in range(try_time):
            try:
                response = requests.get(URL, timeout=5, headers=head
                                        , proxies=proxies)
                if response:
                    break
            except:
                print("%s has been blocked %sth. Try another!" % (str(proxy), i))
                time.sleep(1)
                if try_time-1 == i:
                    requests.get("%sdelete?ip=%s" % (proxy_url, ip))
                    print("delete invalid proxy ip %s" % ip)
    return response

'''
get the teamplate url of kinds of category from sharelatex.com/templates
'''
def get_templates_by_category(TEMPLATE_URL):
    response = get_response(TEMPLATE_URL)
    pattern = re.compile(r'<a href="/templates/(.+?)">')
    match_result = re.findall(pattern=pattern, string=str(response.content))
    category_result = [TEMPLATE_URL+"/"+url for url in set(match_result)]
    print("all category complete")
    print("-"*20)
    return category_result

def get_templates_concrete_url(TEMPLATE_CATEGORY_URL):
    response = get_response(TEMPLATE_CATEGORY_URL)
    pattern = re.compile(r'<a class="thumbnail" href="(.+?)">')
    match_result = re.findall(pattern=pattern, string=str(response.content))
    all_category_template_result = [BASE_URL + url for url in set(match_result)]
    for template in all_category_template_result:
        temp = template.split("/")
        name = temp[-1]
        name = urllib.parse.unquote(name).replace('-', ' ')
        category = temp[-2]
        path = os.path.join("templates", category)
        if not os.path.exists(path):
            os.mkdir(path)
        save_dir = os.path.join(path, name)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        if len(os.listdir(save_dir)) == 2:
            all_category_template_result.remove(template)
            print("Template has already been downloaded: %s" % template)
    print("get template of %s complete" % category)
    print("-"*20)
    return all_category_template_result

def get_each_template_info(EACH_TEMPLATE_URL):
    temp = EACH_TEMPLATE_URL.split("/")
    name = temp[-1]
    name = urllib.parse.unquote(name).replace('-', ' ')
    category = temp[-2]
    category_dir = os.path.join("templates", category)
    template_save_dir = os.path.join(category_dir, name)
    if not os.path.exists(category_dir):
        os.mkdir(category_dir)
    is_template_save_dir_exists = os.path.exists(template_save_dir)
    if not is_template_save_dir_exists:
        os.mkdir(template_save_dir)
        if len(os.listdir(template_save_dir)) < 2:
            response = get_response(EACH_TEMPLATE_URL)
            pattern = re.compile(r'<div class="col-md-12 template-large-pdf-preview">(.+?)</div>')
            match_result = re.findall(pattern=pattern, string=str(response.content))

            pattern = re.compile(r'<img src="(.+?)"')
            match_result = [re.findall(pattern=pattern, string=str(result)) for result in set(match_result)]
            pic = list(itertools.chain.from_iterable(match_result))[0]
            pattern = re.compile(r'<a class="btn btn-default" href="(.+?)"')
            match_result = re.findall(pattern=pattern, string=str(response.content))
            download_url = BASE_URL + list(set(match_result))[0]
            save_pic_path = os.path.join(template_save_dir, name + ".jpg")
            save_zip_path = os.path.join(template_save_dir, name + ".zip")
            if not os.path.exists(save_pic_path):
                print("to download %s" % save_pic_path)
                download_file(pic, save_pic_path)
            else:
                print("%s has been downloaded already" % save_pic_path)
            if not os.path.exists(save_zip_path):
                print("to download %s" % save_zip_path)
                download_file(download_url, save_zip_path)
            else:
                print("%s has been downloaded already" % save_zip_path)
        else:
            print("%s has been already downloaded" % template_save_dir)


def download():
    all_category = get_templates_by_category(BASE_URL+"/templates")
    for each_category in all_category:
        all_templates = set(get_templates_concrete_url(each_category))
        threads = [threading.Thread(target=get_each_template_info, args=(each_template,)) for each_template in all_templates]
        for t in threads:
            t.start()
    time.sleep(10000)
    print("all templates has been downloaded!")

def download_file(url, save_path):
    response = get_response(url)

    response.raise_for_status()
    save_file = open(save_path, 'wb')
    for chunk in response.iter_content(100000):
        save_file.write(chunk)
    print("Download %s complete!" % save_path)
    save_file.close()

if __name__ == "__main__":
    download()
