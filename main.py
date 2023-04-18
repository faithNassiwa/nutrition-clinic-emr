import pymysql
import sys
from getpass import getpass

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user=input('Enter database username: '),
        password=getpass('Enter password: '),
        database='nutrition_db')

except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))
