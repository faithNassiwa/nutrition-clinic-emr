import pymysql
import sys
from getpass import getpass
from db_objects import *


def menu_options():
    print("Nutritionist's Menu Actions \n")
    print('1.Register Nutritionist')
    print('2.Register Patient Visit')
    print('3.Add Consultation / Diagnosis')
    print('4.Add Follow-up Visit')
    print('5.View at risk patients')


# Database Setup
print('Nutrition Clinic EMR')
print('Nutrition Clinic DB Setup ...... ')

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user=input('Enter database username: '),
        password=getpass('Enter password: '),
        database='nutrition_db')

    menu_options()
    user_menu_option = input("Enter the number for action you want or 0 to exist the system: ")
    menu_option = int(user_menu_option.strip())

    while menu_option != 0:
        if menu_option == 1:
            register_nutritionist(connection=conn)
        if menu_option == 2:
            pass
        print('\n')
        menu_options()
        user_menu_option = input("Enter the number for action you want or 0 to exist the system: ")
        menu_option = int(user_menu_option.strip())
        print('\n')
    conn.close()
    sys.exit('End')

except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))
