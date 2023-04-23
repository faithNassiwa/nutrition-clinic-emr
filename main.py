import pymysql
import sys
from getpass import getpass
from db_objects import *


def menu_options():
    print("Nutritionist's Menu Actions \n")
    print('1.Register Nutritionist')
    print('10.Delete Nutritionist')
    print('2.Register Patient')
    print('20.Update Patient')
    print('3.Add Consultation and Diagnosis')
    print('4.Add Follow-up Visit')
    print('5.View quick stats for given period of time')
    print('6.View consultation details for given period of time')


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
        if menu_option == 10:
            delete_nutritionist(connection=conn)
        if menu_option == 2:
            register_patient(connection=conn)
        if menu_option == 20:
            update_patient_address(connection=conn)
        if menu_option == 3:
            add_patient_consultation(connection=conn)
        if menu_option == 4:
            add_patient_consultation_follow_up(connection=conn)
        if menu_option == 5:
            view_quick_stats(connection=conn)
        if menu_option == 6:
            view_consultations_diagnoses(connection=conn)
        print('\n')
        menu_options()
        user_menu_option = input("Enter the number for action you want or 0 to exist the system: ")
        menu_option = int(user_menu_option.strip())
        print('\n')
    conn.close()
    sys.exit('End')

except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))


