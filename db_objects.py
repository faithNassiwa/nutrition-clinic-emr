import pymysql
import pandas as pd
import warnings

warnings.simplefilter("ignore")
pd.set_option('display.max_columns', None)


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def register_nutritionist(connection):
    try:
        first_name = input("Enter Nutritionist's First Name (required): ")
        last_name = input("Enter Nutritionist's Last Name (required): ")
        email_address = input("Enter Nutritionist's Email Address (required): ")
        args = (first_name, last_name, email_address)
        cur = connection.cursor()
        row = cur.callproc('create_nutritionist', args)
        connection.commit()
        cur.close()
        print(">> Successfully registered {} {}".format(row[1], row[2]))
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None


def delete_nutritionist(connection):
    del_nutritionist_email_address = input("Enter Nutritionist's Email Address that you want delete: ")
    upd_nutritionist_email_address = input("Enter Nutritionist's Email Address that will take over their consultations and follow-ups: ")
    cur = connection.cursor()
    nutritionist_id = None
    cur.callproc('find_nutritionist', (del_nutritionist_email_address, nutritionist_id))
    connection.commit()
    cur.execute("SELECT @_find_nutritionist_1")
    del_nutritionist_id = cur.fetchone()[0]
    cur.callproc('find_nutritionist', (upd_nutritionist_email_address, nutritionist_id))
    connection.commit()
    cur.execute("SELECT @_find_nutritionist_1")
    upd_nutritionist_id = cur.fetchone()[0]
    row = cur.callproc('delete_nutritionist', (del_nutritionist_id, upd_nutritionist_id))
    connection.commit()
    cur.close()
    print('Deleted nutritionist id {} and replaced with nutritionist id {} '.format(row[0], row[1]))
    return None

def register_patient(connection):
    try:
        first_name = input("Enter Patient's First Name (required): ")
        last_name = input("Enter Patient's Last Name (required): ")
        email_address = input("Enter Patient's Email Address: ")
        gender = input("Enter Patient's Gender ('Male', 'Female', 'Other') (required): ")
        date_of_birth = input("Enter Patient's date of birth (YYYY-MM-DD) (required): ")
        phone_number = input("Enter Patient's Phone Number: ")
        address_street = input("Enter Patient's address street: ")
        address_city = input("Enter Patient's address city: ")
        address_country = input("Enter Patient's address country: ")
        patient_id = None
        args = (first_name, last_name, email_address, gender, date_of_birth, phone_number, address_street,
                address_city, address_country, patient_id)
        cur = connection.cursor()
        row = cur.callproc('create_patient', args)
        connection.commit()
        cur.execute("SELECT @_create_patient_9")
        patient_id = cur.fetchone()[0]
        cur.close()
        print(">> Successfully registered {} {} with patient id {}".format(row[0], row[1], patient_id))
        return patient_id
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None

def update_patient_address(connection):
    print('*** Search for patient record you want to update  ***')
    patient_first_name = input("Enter Patient's first name (required): ")
    patient_last_name = input("Enter Patient's last name (required): ")
    patient_date_of_birth = input("Enter Patient's date of birth (YYYY-MM-DD) (required): ")
    find_patient_args = (patient_first_name, patient_last_name, patient_date_of_birth)
    cur = connection.cursor()
    cur.callproc('find_patient', find_patient_args)
    results = cur.fetchall()
    patients_df = pd.DataFrame(results, columns=[col[0] for col in cur.description])
    print(patients_df)
    if len(patients_df) > 0:
        print(patients_df)
        patient_id = input("Enter Patient's id from list above (required): ")
        address_street = input("Enter Patient's new address street (required): ")
        address_city = input("Enter Patient's new address city (required): ")
        address_country = input("Enter Patient's new address country (required): ")
        row = cur.callproc('update_patient_address', (patient_id, address_street, address_city, address_country))
        connection.commit()
        cur.close()
        print('Updated patient id {} address details'.format(row[0]))
    else:
        print('Patient does not exist, first register the patient.')
    return None


def register_diagnosis(connection):
    try:
        name = input("Enter the diagnosis name: ")
        description = input("Enter the diagnosis description: ")
        diagnosis_id = None
        args = (name, description, diagnosis_id)
        cur = connection.cursor()
        row = cur.callproc('create_diagnosis', args)
        connection.commit()
        cur.execute("SELECT @_create_diagnosis_2")
        diagnosis_id = cur.fetchone()[0]
        cur.close()
        print(">> Successfully registered {} {} with diagnosis id {}".format(row[0], row[1], diagnosis_id))
        return diagnosis_id
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None


def add_patient_consultation(connection):
    try:
        nutritionist_email_address = input("Enter Nutritionist's Email Address: ")
        print('*** Search for patient record  ***')
        patient_first_name = input("Enter Patient's first name (required): ")
        patient_last_name = input("Enter Patient's last name (required): ")
        patient_date_of_birth = input("Enter Patient's date of birth (YYYY-MM-DD) (required): ")
        find_patient_args = (patient_first_name, patient_last_name, patient_date_of_birth)
        cur = connection.cursor()
        cur.callproc('find_patient', find_patient_args)
        results = cur.fetchall()
        patients_df = pd.DataFrame(results, columns=[col[0] for col in cur.description])
        print(patients_df)
        if len(patients_df) > 0:
            print(patients_df)
            patient_id = input("Enter Patient's id from list above (required): ")
        else:
            print('Patient does not exist, first register the patient.')
            patient_id = register_patient(connection)

        current_weight = float(input("Enter Patient's current weight in Kgs (required): "))
        current_height = float(input("Enter Patient's current height in meters (required): "))
        current_waist_circumference = float(input("Enter Patient's current waist circumference in meters: "))
        current_hip_circumference = float(input("Enter Patient's current hip circumference in meters: "))
        waist_hip_ratio = current_waist_circumference / current_hip_circumference
        current_body_mass_index = calculate_bmi(current_weight, current_height)
        medical_history = input("Enter Patient's Medical History: ")
        family_history = input("Enter Patient's Family History: ")
        physical_activity_note = input("Enter Patient's Physical Activity: ")
        physical_activity_minutes = int(input("Enter Patient's weekly Physical Activity Rate in Minutes (required): "))
        biochemical_notes = input("Enter Patient's Biochemical Notes: ")
        dietary_notes = input("Enter Patient's Dietary Notes: ")
        goal_notes = input("Enter Patient's Goal Notes: ")
        target_weight = int(input("Enter Patient's target weight in kgs: "))
        target_weight_date = input("Enter Patient's target weight date in format YYYY-MM-DD: ")
        daily_target_calories = int(input("Enter Patient's daily target calories: "))
        daily_target_physical_activity_minutes = int(input("Enter Patient's daily target physical activity minutes: "))
        consultation_id = None
        consultation_args = (nutritionist_email_address,  patient_id, current_weight, current_height, current_waist_circumference,
                             current_hip_circumference, waist_hip_ratio, current_body_mass_index, medical_history,
                             family_history, physical_activity_note, physical_activity_minutes, biochemical_notes,
                             dietary_notes, goal_notes, target_weight, target_weight_date, daily_target_calories,
                             daily_target_physical_activity_minutes, consultation_id)
        cur.callproc('create_consultation', consultation_args)
        connection.commit()
        cur.execute("SELECT @_create_consultation_19")
        consultation_id = cur.fetchone()[0]
        print(">> Successfully added the consultation for patient {}".format(patient_id))
        diagnoses_input = int(input("Do you want to add diagnoses? Enter 1 if yes or 0 if no: "))
        while diagnoses_input != 0:
            diagnosis_name = input("Enter name of diagnosis: ")
            cur.callproc('find_diagnosis', (diagnosis_name,))
            results = cur.fetchall()
            diagnoses_df = pd.DataFrame(results, columns=[i[0] for i in cur.description])
            if len(diagnoses_df) > 0:
                print(diagnoses_df)
                diagnoses_id = input("Enter Diagnosis's id from list above (required): ")
            else:
                print('Diagnosis does not exist, first register the diagnosis.')
                diagnoses_id = register_diagnosis(connection)
            diagnosis_category = input("Enter name of diagnosis category ('Clinical', 'Laboratory', 'Other'): ")
            consultation_diagnosis_args = (diagnoses_id, consultation_id, diagnosis_category)
            row = cur.callproc('create_consultation_diagnosis', consultation_diagnosis_args)
            connection.commit()
            print(">> Added diagnosis id {} to consultation id {}".format(row[0], row[1]))
            diagnoses_input = int(input("Do you want to add another diagnosis? Enter 1 if yes or 0 if no: "))
        cur.close()
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None


def add_patient_consultation_follow_up(connection):
    consultation_id = None
    patient_id = None
    try:
        print('*** Search for patient record  ***')
        patient_first_name = input("Enter Patient's first name (required): ")
        patient_last_name = input("Enter Patient's last name (required): ")
        patient_date_of_birth = input("Enter Patient's date of birth (YYYY-MM-DD) (required): ")
        find_patient_args = (patient_first_name, patient_last_name, patient_date_of_birth)
        cur = connection.cursor()
        cur.callproc('find_patient', find_patient_args)
        results = cur.fetchall()
        patients_df = pd.DataFrame(results, columns=[col[0] for col in cur.description])
        if len(patients_df) > 0:
            print(patients_df)
            patient_id = input("Enter Patient's id from list above (required): ")
            nutritionist_email_address = input("Enter Nutritionist's Email Address (required): ")
            nutritionist_id = None
            cur.callproc('find_nutritionist', (nutritionist_email_address, nutritionist_id))
            connection.commit()
            cur.execute("SELECT @_find_nutritionist_1")
            nutritionist_id = cur.fetchone()[0]
            cur.callproc('find_consultation', find_patient_args)
            results = cur.fetchall()
            consultations_df = pd.DataFrame(results, columns=[i[0] for i in cur.description])
            if len(consultations_df) > 0:
                print(consultations_df)
                consultation_id = input("Enter consultation id from list above (required): ")
            weight_reading = float(input("Enter patient's weight reading from today (required):  "))
            height_reading = float(input("Enter patient's height from consultation list (required): "))
            body_mass_index = calculate_bmi(weight_reading, height_reading)
            physical_activity_minutes = float(input("Enter patient's physical activity minutes per week (required): "))
            nutrition_notes = input("Enter patient's nutrition notes: ")
            intervention_notes = input("Enter any intervention notes: ")
            goal_notes = input("Enter patient's goals till next follow-up: ")
            follow_up_visit_id = None
            follow_up_visit_args = (weight_reading, body_mass_index, physical_activity_minutes, nutrition_notes,
                                    intervention_notes, goal_notes, nutritionist_id, patient_id, consultation_id,
                                    follow_up_visit_id)
            cur.callproc('create_follow_up_visit', follow_up_visit_args)
            connection.commit()
            cur.execute("SELECT @_create_follow_up_visit_9")
            follow_up_visit_id = cur.fetchone()[0]
            print(" Added patient's follow_up visit id {}".format(follow_up_visit_id))
        else:
            print('Patient does not exist, follow-up visit can only be made by registered patients.')
        cur.close()
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
    return None


def view_quick_stats(connection):
    patient_seen_at_consultation_q = """select num_patients_seen_consultations(%s, %s)"""
    patient_seen_at_follow_up_visits_q = """select num_patients_seen_follow_up_visits(%s, %s)"""
    start_date = input("Enter report start date in format (YYYY-MM-DD): ")
    end_date = input("Enter report end date in format (YYYY-MM-DD) (if this date is needed in the report increase it by 1 day): ")
    stats = {}
    cur = connection.cursor()
    cur.execute(patient_seen_at_consultation_q, (start_date, end_date))
    patient_seen_at_consultation = cur.fetchone()[0]
    if patient_seen_at_consultation:
        stats['Patients Seen at Consultation'] = patient_seen_at_consultation
    else:
        stats['Patients Seen at Consultation'] = 0
    cur.execute(patient_seen_at_follow_up_visits_q, (start_date, end_date))
    patient_seen_at_follow_up_visits = cur.fetchone()[0]
    if patient_seen_at_follow_up_visits:
        stats['Patients Seen at Follow-up Visits'] = patient_seen_at_follow_up_visits
    else:
        stats['Patients Seen at Follow-up Visits'] = 0
    df = pd.DataFrame.from_dict(stats, orient='index', columns=['Number of Patients'])
    print(df)
    return None


def view_consultations_diagnoses(connection):
    query = """select * from patient_consultations where consultation_date between %s and %s"""
    start_date = input("Enter report start date in format (YYYY-MM-DD): ")
    end_date = input("Enter report end date in format (YYYY-MM-DD): ")
    cur = connection.cursor()
    cur.execute(query, (start_date, end_date))
    results = cur.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in cur.description])
    print(df)
    return None



