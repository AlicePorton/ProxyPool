import pymysql.cursors

test_data = {'国家': '', 'IP': '192.168.6.22', 'PORT': '8088', 'status': 'SUCCESS', 'protocol': 'http'}
connection = pymysql.connect(host='localhost',
                             user='proxypool',
                             password='Proxypool123.',
                             db='proxypoolDB')

try:
    with connection.cursor() as cursor:
        ip = test_data['IP']
        protocol = test_data['protocol']
        port = test_data['PORT']
        status = test_data['status']
        sql = 'insert into `proxypool` (ip, port, protocol, status) VALUE (\'%s\', \'%s\', \'%s\')' % (ip, port, protocol,)
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
