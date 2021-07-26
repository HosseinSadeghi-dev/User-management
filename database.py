import datetime
from sqlite3 import connect
import hash


class EmployeeDatabase:

    @staticmethod
    def insert(f_name, l_name, national_code, birthday, image_src):
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"INSERT INTO employee(F_NAME, L_NAME, NATIONAL_CODE, BIRTHDAY, IMAGE_SRC) "
                              f"VALUES('{f_name}','{l_name}','{national_code}', '{birthday}', '{image_src}')")
            last_id = my_cursor.lastrowid
            my_con.commit()
            my_con.close()
            return True, last_id
        except Exception as e:
            return False, 'error: ' + str(e)

    @staticmethod
    def find_all():
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM employee")
            result = my_cursor.fetchall()
            my_con.close()
            return True, result
        except Exception as e:
            return False, 'error: ' + str(e)

    @staticmethod
    def delete(national_code=None):
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()
            if national_code:
                my_cursor.execute(f"DELETE FROM employee WHERE national_code={national_code}")
            else:
                my_cursor.execute(f"DELETE FROM employee")
            my_con.commit()
            my_con.close()
            return True, 'deleted correctly'
        except Exception as e:
            return False, 'error: ' + str(e)

    @staticmethod
    def update(f_name, l_name, national_code, birthday, image_src, _id):
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"UPDATE employee SET "
                              f"f_name='{f_name}',"
                              f"l_name='{l_name}',"
                              f"national_code='{national_code}',"
                              f"birthday='{birthday}',"
                              f"image_src='{image_src}',"
                              f" WHERE id={_id}")
            my_con.commit()
            my_con.close()
            return True
        except Exception as e:
            print("error:", e)
            return False

    @staticmethod
    def find_by_national_code(national_code):
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()

            sql_select_query = """select * from employee where national_code = ?"""
            my_cursor.execute(sql_select_query, (national_code,))

            record = my_cursor.fetchone()
            if not record:
                raise Exception("Username Or Password might Be Wrong, Check them then try again please !")

            my_con.commit()
            my_con.close()
            return True, record
        except Exception as e:
            return False, 'error: ' + str(e)


class AdminDatabase:

    @staticmethod
    def login(phone_number, password):
        try:
            my_con = connect('database/database.db')
            my_cursor = my_con.cursor()

            sql_select_query = """select * from admin where phone_number = ?"""
            my_cursor.execute(sql_select_query, (phone_number,))

            record = my_cursor.fetchone()
            if not record:
                raise Exception("Username Or Password might Be Wrong, Check them then try again please !")

            row_password = record[2]

            _hash = hash.Hash()
            password = _hash.__encrypt__(password)

            if str(row_password) != str(password):
                raise Exception("Username Or Password might Be Wrong, Check them then try again please !")

            my_con.commit()
            my_con.close()
            return True, f'Welcome to User Management {record[3]}'
        except Exception as e:
            return False, 'error: ' + str(e)
