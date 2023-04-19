import pymysql


def register_nutritionist(connection):
    try:
        first_name = input("Enter Nutritionist's First Name: ")
        last_name = input("Enter Nutritionist's Last Name: ")
        email_address = input("Enter Nutritionist's Email Address: ")
        args = (first_name, last_name, email_address)
        cur = connection.cursor()
        row = cur.callproc('create_nutritionist', args)
        connection.commit()
        cur.close()
        print(">> Successfully registered {} {}".format(row[1], row[2]))
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None





