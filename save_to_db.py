import pymysql.cursors
from download import get_proxy_ip, concat_sql

title_dicts = {
    "IP": "IP地址",
    "PORT": "端口",
    "STATUS": "status",
    "PROTOCOL": '类型'
}
sql = concat_sql(get_proxy_ip(1, validated=True)['results'], title_dicts)
connection = pymysql.connect(host='localhost',
                             user='proxypool',
                             password='Proxypool123.',
                             db='proxypoolDB')
try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
finally:
    connection.close()


