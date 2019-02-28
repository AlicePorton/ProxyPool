import os
import re
import time

import requests
from bs4 import BeautifulSoup
import crower_table


def get_html(url):
    """
    :param url: 爬取的网址参数，先将爬的内容缓存起来
    :return: 返回一个soup类型
    """
    out_time = time.strftime("%Y%m%d", time.localtime())
    path_url = ''.join(re.findall(r'\w+', url))
    path = 'temp/' + path_url + '-' + out_time
    if not os.path.isfile(path):
        print('writing file')
        content = requests.get(url=url, headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'}).text
        crower_table.write_file_content(path, content)
        return content
    else:
        return crower_table.get_file_content(path)


def get_proxy_ip():
    for x in range(1, 2):
        url = 'http://www.xicidaili.com/nn/{0}'.format(x)
        soup = BeautifulSoup(get_html(url), 'lxml')
        results = crower_table.get_table_content(soup.table)
        test_results = [validate_ip(one['IP地址']+':'+one['端口'], one['类型']) for one in results]
        print(test_results)


def validate_ip(ip, protocol):
    test_url = 'http://baidu.com'
    try:
        proxy_host = {protocol: protocol + "://" + ip}
        html = requests.get(test_url, proxies=proxy_host, timeout=3, headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'})
        if html.status_code == 200:
            print('success',proxy_host)
            return True
        else:
            print('Failed', proxy_host)
            return False
    except Exception:
        return 'error'


get_proxy_ip()