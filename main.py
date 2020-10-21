# A STUDENT MANAGEMENT SYSTEM
# GOALS - 1) KEEP RECORDS OF STUDENTS FEES.
#         2) KEEP RECORDS OF ALL THE STUDENTS.
#         3) GET DETAILS OF ALL STUDENTS.
#         4) GET DETAILS OF A PARTICULAR STUDENT.
#         5) UPDATE STUDENT RECORDS.
import datetime
import sys
import time

from tqdm import tqdm

from database import Database

# config : dict -> this contains the configuration for database.
config = {'dbconfig': {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'faisal@2403',
    'database': 'SMS'
}}


def loading_effect(description: str):
    # THE EFFECT THAT WILL SHOW THE DESIGN FOR SOME TIME DELAY SO THAT IT LOOKS THAT SOMETHING IS
    # REALLY HAPPEN -> User's source of entertainment.
    for _ in tqdm(range(100), desc=description, ascii=False, ncols=75):
        time.sleep(0.01)


def new_data():
    # --> THIS IS THE FUNCTION THAT WILL DEAL WITH USER DATA INPUT INTO DATABASE
    # A LIST HAS BEEN ASSIGNED WITH ALL THE PARAMETERS THAT HAS TO BE TAKEN .
    # NOW A DICT IS KEPT SO THAT WHEN  LOOP RUNS AND TAKES INOUT FOR ALL THE DATA ,
    # SOME VARIABLE CAN STORE THAT DATA,ie : INSERT DATA INTO DATABASE.
    # THE THE PARAMETERS BEING ENTERED BY USER IS VERIFIED BY USER ONCE BEFORE
    # PUTTING THE WHOLE MESS INTO DATABASE.
    # STUDENT'S ID AND FEES HAS BEEN THEN ASSIGNED AFTER CONFIRMATION AND BEFORE PUTTING
    # IT INTO DATABASE.

    studentdetails = ['Student_Name', 'DOB', 'Gender', 'Class', 'School', 'Father_Name', 'Mother_Name', 'Address',
                      'Contact_Number']
    studentdetailsdict = {}
    print('ENTER STUDENT DETAILS - ')
    for data in studentdetails:
        studentdetailsdict[data] = input(f'Enter {data}     : ')
    studentdetailsdict['Admission_Date'] = datetime.date.today()

    print('---------------- PLEASE CHECK THE DETAILS(STUDENTS) ------------------ ')
    for key, value in studentdetailsdict.items():
        print(f'{key}        : {value}')
    print('-----------------------------------------------------------------------')
    confirm = input('PRESS [Y] TO CONFIRM, ENTER ANY OTHER KEY TO RE-ENTER : ')
    if confirm == 'Y' or confirm == 'y':
        print('DETAILS CONFIRMED')
        studentdetailsdict['Fee'] = input('Enter Fee : Rs ')
        studentdetailsdict['Student_ID'] = studentdetailsdict['Student_Name'][0:2] \
                                           + studentdetailsdict['Contact_Number'][::3]

        # FOR ALL THE DATA ENTERED BY USER IS BEING STORED INTO THE DATABASE SMS
        # AND IN THE TABLE 'Student_Details'.

        with Database(config['dbconfig']) as cursor:
            _SQL = """insert into student_details
                    (Student_ID, Student_Name, DOB, Gender, Class, School, Fee, Admission_Date, 
                    Father_Name, Mother_Name, Address, Contact_Number)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (studentdetailsdict['Student_ID'],
                                  studentdetailsdict['Student_Name'],
                                  studentdetailsdict['DOB'],
                                  studentdetailsdict['Gender'],
                                  studentdetailsdict['Class'],
                                  studentdetailsdict['School'],
                                  studentdetailsdict['Fee'],
                                  studentdetailsdict['Admission_Date'],
                                  studentdetailsdict['Father_Name'],
                                  studentdetailsdict['Mother_Name'],
                                  studentdetailsdict['Address'],
                                  studentdetailsdict['Contact_Number']))
            _SQL = ("select * from student_details where Student_Name = '%s';" % studentdetailsdict['Student_Name'])
            cursor.execute(_SQL)

            # THIS PROVIDE THE STUDENT ID FOR FUTURE REFERENCE FOR FEE PAYMENTS AND ALL.

            for _ in cursor:
                print(f'STUDENT UNIQUE ID : {_[0]}')
        loading_effect('SAVING DATA .....')
        print('Data Saved.')

        # AFTER DOING EVERYTHING USER MAY NEED TO FILL UP OTHER DATA, OR MORE DATA ,
        # SO THERE IS A CONFIRMATION ABOUT IT.

        continuation = input('Make Another Entry ? Press [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            new_data()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    else:
        new_data()
    return None


def fee():
    # OUR fee() FUNCTION THAT HANDLES EVERYTHING WHICH US RELATED TI FEE.
    # USER HAS TO CHOOSE ANY ONE AND THEN THE FUNCTION WILL PROCEED ACCORDING TO IT,

    fee_choice = int(input('1) PAYMENT INPUT.\n'
                           '2) VIEW PAYMENT INFO OF STUDENT.\n'
                           '3) VIEW ALL PAYMENT INFO.\n'
                           'Enter Your Choice : \n'))
    if fee_choice == 1:

        # WHEN USER CHOOSES 1 AS AN INPUT HE MAKES THE CHOICE OF ENTERING FEE DETAILS, WHEN SOMEONE PAYS.
        # IT IS INITIATED WITH THE HELP OF Student_ID GENERATED AT THE END OF THE REGISTRATION OF STUDENT.
        # DATABASE IS INITIATED TO SEARCH FOR THE THE DATA ENTERED BY USERS INTO THE DATABASE.
        # THE DETAIL ARE THEN KEPT IN FROM OF USR AS PER CONFIRMATION.

        student_ID = input('STUDENT ID : ')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("SELECT * FROM STUDENT_DETAILS WHERE Student_ID = '%s';" % student_ID)
            cursor.execute(_SQL)
            for _ in cursor:
                print(f'NAME : {_[1]} MONTHLY FEE : {_[6]}')
            detaillist = ['Amount_Paid', 'Month']
            dictfee = {}
            for det in detaillist:
                dictfee[det] = input(f'ENTER {det}  : ')
            dictfee['Remaining'] = str(int(_[6]) - int(dictfee['Amount_Paid']))
            dictfee['Payment_Date'] = datetime.date.today()
            print(f'-----------------------------------------------------------------------\n'
                  f'MAKING A PAYMENT UPDATE -> CHECK ONCE \n'
                  f'Name        : {_[1]}\n'
                  f'MONTHLY FEE : {_[6]}\n'
                  f"AMOUNT PAID : {dictfee['Amount_Paid']}\n"
                  f"MONTH       : {dictfee['Month']}\n"
                  f'-----------------------------------------------------------------------\n')

            # AFTER DOING EVERYTHING USER NEED TO CONFIRM ENTERED DATA.
            # SO THERE IS A CONFIRMATION ABOUT IT. AFTER IT,
            # DATA HAS BEEN THEN STORED INTO DATABASE.
            # IF THE USER INPUTS ANY CONFORMATION VALUE OTHER THAN 'Y' THE WHOLE
            # FEE FUNCTION WILL START AGAIN, CONSIDERING THAT USER MAY HAVE ENTERED SOME
            # WRONG DATA

            confirm = input('PRESS [Y] TO CONFIRM, ENTER ANY OTHER KEY TO RE-ENTER : ')
            if confirm == 'Y' or confirm == 'y':
                print('DETAILS CONFIRMED')
                with Database(config['dbconfig']) as cursor:
                    _SQL = """INSERT INTO FEEDETAILS 
                    (Student_ID, Student_Name, Payment_Date, Month, Amount_Paid, Remaining) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(_SQL, (student_ID,
                                          _[1],
                                          dictfee['Payment_Date'],
                                          dictfee['Month'],
                                          dictfee['Amount_Paid'],
                                          dictfee['Remaining']))
                loading_effect('SAVING DATA .....')
                print('Data Saved.')
                continuation = input('Make Another Entry ? Press [Y] to continue, and any other key to exit : ')
                if continuation == 'Y' or continuation == 'y':
                    fee()
                else:
                    loading_effect('CLOSING PROGRAM.....')
                    print('CLOSED !')
                    sys.exit()
            else:
                fee()
    elif fee_choice == 2:

        # WHEN USER INPUT IS 2 THEN USER IS CHOOSING TO ALL THE FEE PAYMENTS MADE BY A STUDENT
        # DATA WILL BE RETRIEVED FROM DATABASE USING THE STUDENT ID
        # AND THERE IS ALSO CONTINUATION IF USER WANTS T VIEW FEE DETAILS FOR OTHER STUDENTS.

        student_ID = input('STUDENT ID : ')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("SELECT * FROM FEEDETAILS WHERE Student_ID = '%s';" % student_ID)
            cursor.execute(_SQL)
            counter = 1
            loading_effect('LOADING DATA .....')
            for _ in cursor:
                print(f'--------------------------------------------\n'
                      f'DATA --->  {counter}\n'
                      f'NAME         : {_[1]}\nPAYMENT DATE : {_[2]}\n'
                      f'MONTH        : {_[3]}\nAMOUNT PAID  : {_[4]}\n'
                      f'REMAINING    : {_[5]}'
                      f'--------------------------------------------\n')
                counter += 1
                continuation = input('VIEW ANOTHER DATA ? Press [Y] to continue, and any other key to exit : ')
                if continuation == 'Y' or continuation == 'y':
                    fee()
                else:
                    loading_effect('CLOSING PROGRAM.....')
                    print('CLOSED !')
                    sys.exit()

    elif fee_choice == 3:

        # WHEN USER INPUT IS 3, USER IS CHOOSING TO WATCH ALL THE FEE PAID DATA, FROM THE DATABASE.
        # ALL DATA WILL BE RETRIEVED AND WILL BE PRINTED.
        # USER CAN START THIS FUNCTION WHEN ASKED TO CONTINUE BY ENTERING Y, OR CAN EXIT PROGRAM BY ENTERING
        # ANY OTHER INPUT EXCEPT Y/y.

        loading_effect('LOADING DATA .....')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("SELECT * FROM FEEDETAILS")
            cursor.execute(_SQL)
            counter = 1
            for _ in cursor:
                print(f'--------------------------------------------\n'
                      f'DATA --->  {counter}\n'
                      f'NAME         : {_[1]}\nPAYMENT DATE : {_[2]}\n'
                      f'MONTH        : {_[3]}\nAMOUNT PAID  : {_[4]}\n'
                      f'REMAINING    : {_[5]}\n'
                      f'--------------------------------------------\n')
                counter += 1
        continuation = input('VIEW ANOTHER DATA ? Press [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            fee()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    else:
        print('<----- WRONG CHOICE ENTERED ----->\n'
              'PLEASE ENTER AGAIN.')
        fee()


def view_data():
    # --> FOR GETTING BACK THE DATA FROM DATA BASE OR VIEWING DATA, FOUR CATEGORIES HAVE BEEN SET
    # FOR VIEWING DATA, ACCORDING TO NEED.

    data_view_choice = int(input('1) VIEW ALL DATA.\n'
                                 '2) VIEW DATA FOR A PARTICULAR STUDENT.\n'
                                 '3) VIEW DATA ACCORDING TO CLASS.\n'
                                 '4) VIEW DATA ACCORDING TO FEES.\n'
                                 'ENTER YOUR CHOICE : '))
    if data_view_choice == 1:

        # WHEN USER IS SELECTING THIS, USER IS OPTING TO VIEW ALL DATA STORED INTO DATABASE.
        # CONTINUATION IS THERE IF USER WANTS TO VIEW OTHER DATA.
        # OR USER CAN EXIT BY ENTERING ANYTHING EXCEPT Y/y WHEN ASKED FOR CONTINUATION.

        loading_effect('LOADING DATA...')
        print('PRINTING DATA ...')
        with Database(config['dbconfig']) as cursor:
            _SQL = "SELECT * FROM STUDENT_DETAILS"
            cursor.execute(_SQL)
            counter = 1
            for _ in cursor:
                print(f'----------------------------------------------------------------\n'
                      f'STUDENT {counter}\n'
                      f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                      f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                      f'CLASS           :   {_[4]}\nSCHOOL          :   {_[5]}\n'
                      f'FEE             :   {_[6]}\nADMISSION DATE  :   {_[7]}\n'
                      f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                      f'ADDRESS         :   {_[10]}\nCONTACT         :   {_[11]}\n'
                      f''
                      f'----------------------------------------------------------------\n')
                counter += 1
        continuation = input('View other data ? [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            view_data()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    elif data_view_choice == 2:

        # WHEN USER OPTS THIS OPTION, USER WILL GET DATA OF A PARTICULAR STUDENT SEARCHED BY STUDENT ID.
        # SAME AS PREVIOUS CHOICE THERE IS ALSO OPTION OF CONTINUATION.

        student_id = input('Enter Student ID :  ')
        loading_effect('LOADING DATA......')
        print('PRINTING DATA...')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("select * from student_details where Student_ID = '%s';" % student_id)
            cursor.execute(_SQL)
            for _ in cursor:
                print(f'----------------------------------------------------------------\n'
                      f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                      f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                      f'CLASS           :   {_[4]}\nSCHOOL          :   {_[5]}\n'
                      f'FEE             :   {_[6]}\nADMISSION DATE  :   {_[7]}\n'
                      f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                      f'ADDRESS         :   {_[10]}\nCONTACT         :   {_[11]}\n'
                      f''
                      f'----------------------------------------------------------------\n')
        continuation = input('View other data ? [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            view_data()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    elif data_view_choice == 3:

        # WHEN USER OPTS THIS OPTION, USER WILL GET DATA OF A PARTICULAR CLASS..
        # SAME AS PREVIOUS CHOICE THERE IS ALSO OPTION OF CONTINUATION.

        Class = input('Enter CLASS :  ')
        loading_effect('LOADING DATA......')
        print('PRINTING DATA...')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("select * from student_details where Class = '%s';" % Class)
            cursor.execute(_SQL)
            for _ in cursor:
                print(f'----------------------------------------------------------------\n'
                      f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                      f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                      f'SCHOOL          :   {_[5]}\n'
                      f'FEE             :   {_[6]}\nADMISSION DATE  :   {_[7]}\n'
                      f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                      f'ADDRESS         :   {_[10]}\nCONTACT         :   {_[11]}\n'
                      f''
                      f'----------------------------------------------------------------\n')
        continuation = input('View other data ? [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            view_data()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    elif data_view_choice == 4:

        # WHEN USER OPTS THIS OPTION, USER WILL GET DATA OF STUDENTS WHO HAVE SIMILAR FEE.
        # SAME AS PREVIOUS CHOICE THERE IS ALSO OPTION OF CONTINUATION.

        Fee = input('Enter Fee :  ')
        loading_effect('LOADING DATA......')
        print('PRINTING DATA...')
        with Database(config['dbconfig']) as cursor:
            _SQL = ("select * from student_details where Fee = '%s';" % Fee)
            cursor.execute(_SQL)
            counter = 1
            for _ in cursor:
                print(f'----------------------------------------------------------------\n'
                      f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                      f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                      f'SCHOOL          :   {_[5]}\n'
                      f'ADMISSION DATE  :   {_[7]}\n'
                      f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                      f'ADDRESS         :   {_[10]}\nCONTACT         :   {_[11]}\n'
                      f''
                      f'----------------------------------------------------------------\n')
                counter += 1
        continuation = input('View other data ? [Y] to continue, and any other key to exit : ')
        if continuation == 'Y' or continuation == 'y':
            view_data()
        else:
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()
    else:
        print('<----- WRONG CHOICE ENTERED ----->\n'
              'PLEASE ENTER AGAIN.')
        view_data()


def update_fun(student_id, updated_data, _SQL1):
    # Function for handling different SQL queries for updating.

    with Database(config['dbconfig']) as cursor:
        _SQL = _SQL1
        val = (updated_data, student_id)
        cursor.execute(_SQL, val)
    loading_effect('UPDATING DATA.......')
    print('Data Updated.')
    with Database(config['dbconfig']) as cursor:
        _SQL = ("SELECT * FROM STUDENT_DETAILS WHERE Student_ID ='%s'" %student_id)
        cursor.execute(_SQL)
        for _ in cursor:
            print(f'---------------UPDATED DATA------------------'
                  f'---------------------------------------------\n'
                  f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                  f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                  f'CLASS           :   {_[4]}\nSCHOOL          :   {_[5]}\n'
                  f'FEE             :   {_[6]}\nADMISSION DATE  :   {_[7]}\n'
                  f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                  f'ADDRESS         :   {_[10]}\nCONTACT        :   {_[11]}\n'
                  f'---------------------------------------------\n')
        print('UPDATED DATA SAVED .')


def update_data():
    # Function to update the students details.

    print('UPDATING WINDOW -- ')
    studentId = input('Enter Student ID : ')
    print('STUDENT DETAILS UPDATION')
    updateOptions = ['Address', 'Contact Number', 'Class', 'School', 'Fee']
    counter = 1
    print('WHAT DO YOU WANT TO UPDATE : ')
    for _ in updateOptions:
        print(f'{counter}) {_}')
        counter += 1
    update_choice = int(input('Enter your choice : '))
    if update_choice == 1:

        # FOR ADDRESS UPDATE
        updated_data = input('Enter Address : ')
        _SQL1 = ("UPDATE STUDENT_DETAILS SET Address = %s WHERE Student_ID = %s")
        update_fun(studentId, updated_data, _SQL1)
        confirmation_update()
    elif update_choice == 2:

        # FOR CONTACT UPDATE
        updated_data = input('Enter Contact Number : ')
        _SQL1 = ("UPDATE STUDENT_DETAILS SET Contact_Number = %s WHERE Student_ID = %s")
        update_fun(studentId, updated_data, _SQL1)
        confirmation_update()
    elif update_choice == 3:

        # FOR CLASS
        updated_data = input('Enter Class : ')
        _SQL1 = ("UPDATE STUDENT_DETAILS SET Class = %s WHERE Student_ID = %s")
        update_fun(studentId, updated_data, _SQL1)
        confirmation_update()
    elif update_choice == 4:

        # FOR SCHOOL
        updated_data = input('Enter School : ')
        _SQL1 = ("UPDATE STUDENT_DETAILS SET School = %s WHERE Student_ID = %s")
        update_fun(studentId, updated_data, _SQL1)
        confirmation_update()
    elif update_choice == 5:

        # FOR FEE
        updated_data = input('Enter Fee : ')
        _SQL1 = ("UPDATE STUDENT_DETAILS SET Fee = %s WHERE Student_ID = %s")
        update_fun(studentId, updated_data, _SQL1)
        confirmation_update()
    else:
        print('------------ ERROR INPUT -----------\n'
              'ENTER AGAIN.')
        update_data()


def confirmation_update():
    continuation = input('Make Another UPDATE ? Press [Y] to continue, and any other key to exit : ')
    if continuation == 'Y' or continuation == 'y':
        update_data()
    else:
        loading_effect('CLOSING PROGRAM.....')
        print('CLOSED !')
        sys.exit()


def delete_data():
    studentId = input('Enter Student ID : ')

    # Database Code will go here
    # Students details should be printed.

    with Database(config['dbconfig']) as cursor:
        _SQL = ("SELECT * FROM STUDENT_DETAILS WHERE Student_ID = '%s';" % studentId)
        cursor.execute(_SQL)
        for _ in cursor:
            print(f'----------------------------------------------------------------\n'
                  f'STUDENT ID      :   {_[0]}\nNAME            :   {_[1]}\n'
                  f'D.O.B           :   {_[2]}\nGENDER          :   {_[3]}\n'
                  f'CLASS           :   {_[4]}\nSCHOOL          :   {_[5]}\n'
                  f'FEE             :   {_[6]}\nADMISSION DATE  :   {_[7]}\n'
                  f"FATHER'S NAME   :   {_[8]}\nMOTHER'S NAME   :   {_[9]}\n"
                  f'ADDRESS         :   {_[10]}\nCONTACT         :   {_[11]}\n'
                  f'----------------------------------------------------------------\n')

            # THIS CONTINUATION WILL MAKE SURE THAT THE DATA RETRIEVED FROM DATABASE IS CORRECT

    continuation = input('CONFIRM DATA - Press [Y] to CONFIRM, and any other key to exit : ')
    if continuation == 'Y' or continuation == 'y':
        with Database(config['dbconfig']) as cursor:
            _SQL = ("DELETE FROM STUDENT_DETAILS WHERE Student_ID = '%s'" %studentId)
            cursor.execute(_SQL)
        loading_effect('DELETING DATA....')
        print('DATA DELETED')
    else:
        loading_effect('CLOSING PROGRAM.....')
        print('CLOSED !')
        sys.exit()

    continuation = input('DELETE Another ? Press [Y] to continue, and any other key to exit : ')
    if continuation == 'Y' or continuation == 'y':
        delete_data()
    else:
        loading_effect('CLOSING PROGRAM.....')
        print('CLOSED !')
        sys.exit()


def admin():
    # WORKING CORRECT --> AUTHENTICATION CODE
    adminAuthentication = {'username': ['Faisal', 'Farida', 'Nusrat'], 'password': '@admin123@'}
    username = input('Admin    : ')
    password = input('Password : ')
    admins = adminAuthentication['username']
    for _ in admins:
        if username in admins and password == adminAuthentication['password']:
            loading_effect(' CHECKING ACCESS ')
            print(f'WELCOME {username}')
            return True
        else:
            print('<-- ERROR -->')
            loading_effect('CLOSING PROGRAM.....')
            print('CLOSED !')
            sys.exit()


def run_pro():
    if admin() is True:
        print('\n1) INSERT NEW DATA.'
              '\n2) FEES.'
              '\n3) CHECK DATA.'
              '\n4) UPDATE DATA.'
              '\n5) DELETE DATA.')
        choice = int(input('YOUR CHOICE : '))
        if choice == 1:
            new_data()
        elif choice == 2:
            fee()
        elif choice == 3:
            view_data()
        elif choice == 4:
            update_data()
        elif choice == 5:
            delete_data()
        else:
            print('< -- RESTART PROGRAM SOME ERROR OCCURRED -- >')
            sys.exit()


if __name__ == '__main__':
    run_pro()
