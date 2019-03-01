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
        content = requests.get(url=url, headers={
            'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'}).text
        crower_table.write_file_content(path, content)
        return content
    else:
        return crower_table.get_file_content(path)


def get_proxy_ip(x, validated=False):
    url = 'http://www.xicidaili.com/nn/{0}'.format(x)
    soup = BeautifulSoup(get_html(url), 'lxml')
    results = crower_table.get_table_content(soup.table)
    test_results = [validate_ip(one, validated) for one in results]
    return {'results': results, 'status': test_results}


def validate_ip(one, validated):
    if validated:
        one['status'] = 'SUCCESS'
        return True
    ip = one['IP地址'] + ':' + one['端口']
    protocol = one['类型']
    test_url = 'http://baidu.com'
    try:
        proxy_host = {protocol: protocol + "://" + ip}
        html = requests.get(test_url, proxies=proxy_host, timeout=3,
                            headers={'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'})
        if html.status_code == 200:
            one['status'] = 'SUCCESS'
            print('success', proxy_host)
            return True
        else:
            one['status'] = 'FAILED'
            print('Failed', proxy_host)
            return False
    except Exception:
        one['status'] = 'ERROR'
        return 'error'





def concat_sql(results, title_dicts):
    statements = ''
    for result in results:
        statements += '("%s", "%s", "%s", "%s"),'% (
            result[title_dicts['IP']], result[title_dicts['PORT']], result[title_dicts['PROTOCOL']],
            result[title_dicts['STATUS']])

    print(statements)
    return 'insert into `pool` (ip, port, protocol, status) VALUES ' + statements[:-1]


# concat_sql(get_proxy_ip(1)["results"], title_dicts)
