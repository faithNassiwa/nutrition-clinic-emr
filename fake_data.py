import pymysql
from getpass import getpass
from faker import Faker
import random

# Connect to the MySQL database
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user=input('Enter database username: '),
    password=getpass('Enter password: '),
    db='nutrition_db'
)
cur = conn.cursor()

# Create a Faker instance
fake = Faker()

# Generate fake data for the nutritionist table
for i in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_address = fake.email()
    created_at = fake.date_time_between(start_date='-1y', end_date='now')
    updated_at = fake.date_time_between(start_date=created_at, end_date='now')
    query = f"INSERT INTO nutritionist (first_name, last_name, email_address, created_at, updated_at) VALUES ('{first_name}', '{last_name}', '{email_address}', '{created_at}', '{updated_at}')"
    cur.execute(query)
conn.commit()

# Generate fake data for the patient table
genders = ['Male', 'Female', 'Other']
countries = ['USA', 'Canada', 'UK']
for i in range(20):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_address = fake.email()
    gender = random.choice(genders)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
    digits = fake.numerify(text='##########')
    phone_number = f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'
    address_street = fake.street_address()
    address_city = fake.city()
    address_country = random.choice(countries)
    created_at = fake.date_time_between(start_date='-1y', end_date='now')
    updated_at = fake.date_time_between(start_date=created_at, end_date='now')
    query = f"INSERT INTO patient (first_name, last_name, email_address, gender, date_of_birth, phone_number, address_street, address_city, address_country, created_at, updated_at) VALUES ('{first_name}', '{last_name}', '{email_address}', '{gender}', '{date_of_birth}', '{phone_number}', '{address_street}', '{address_city}', '{address_country}', '{created_at}', '{updated_at}')"
    cur.execute(query)
conn.commit()

