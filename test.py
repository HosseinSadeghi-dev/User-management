import cv2
from time import sleep
import os
from database import AdminDatabase, EmployeeDatabase
import functions
import filter


def take_screenshot():
    face_cascade = cv2.CascadeClassifier('assets/haarcascades/haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    feed_type = '0'

    while True:
        # unable to open camera
        if not video_capture.isOpened():
            print('Webcam Error, wait 5 seconds')
            sleep(5)
            pass

        # Capture
        _, org_frame = video_capture.read()
        frame = org_frame

        gray = cv2.cvtColor(org_frame, cv2.COLOR_BGR2GRAY)

        key = cv2.waitKey(1)

        # quit
        if key == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            return False, 'webcam closed unexpected'

        if key == ord('0') or feed_type == '0':
            feed_type = '0'
            frame = org_frame

        if key == ord('1') or feed_type == '1':
            feed_type = '1'
            frame = filter.filter1(org_frame)

        if key == ord('2') or feed_type == '2':
            feed_type = '2'
            frame = filter.filter2(org_frame)

        if key == ord('3') or feed_type == '3':
            feed_type = '3'
            frame = filter.filter3(org_frame)

        if key == ord('4') or feed_type == '4':
            feed_type = '4'
            frame = filter.filter4(org_frame)

        if key == ord('5') or feed_type == '5':
            feed_type = '5'
            frame = filter.filter5(org_frame)

        if key == ord('6') or feed_type == '6':
            feed_type = '6'
            frame = filter.filter6(org_frame)

        if key == ord('7') or feed_type == '7':
            feed_type = '7'
            frame = filter.filter7(org_frame)

        if key == ord('8') or feed_type == '8':
            feed_type = '8'
            frame = filter.filter8(org_frame)

        if key == ord('9') or feed_type == '9':
            feed_type = '9'
            frame = filter.filter9(org_frame)

        # take screenshot
        if key == ord('s'):
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            x, y, w, h = faces[0]
            face_frame = frame[y: y + h, x: x + w]
            video_capture.release()
            cv2.destroyAllWindows()
            return functions.save_image(face_frame)

        # Display the resulting frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size_scale = 0.5
        font_color = (0, 0, 0)
        cv2.putText(frame, 'q To Quit', (10, 30), font, font_size_scale, font_color, 2, cv2.LINE_AA)
        cv2.putText(frame, 's To Save and Upload', (10, 60), font, font_size_scale, font_color, 2, cv2.LINE_AA)
        cv2.putText(frame, '1 - 9 To change filter', (10, 90), font, font_size_scale, font_color, 2, cv2.LINE_AA)
        cv2.putText(frame, '0 To normal filter', (10, 120), font, font_size_scale, font_color, 2, cv2.LINE_AA)

        cv2.imshow('Video', frame)


def show_users():
    status, result = EmployeeDatabase.find_all()
    if status:
        for row in result:
            # print("Id: ", row[0])
            print("First Name: ", row[1])
            print("Last Name: ", row[2])
            print("National Code: ", row[3])
            print("Birthday: ", row[4])
            print("\n ------------------------- \n")

        print("1- show one of the users detail \n"
              "2- create a new user \n"
              "3- edit a user \n"
              "4- delete a user \n"
              "5- delete ALL users \n"
              "6- exit \n\n")
        choice = int(input('your choice: '))

        if choice < 1 or choice > 6:
            print('please choose valid option')
            input('press enter to proceed...')
            functions.clear()
            show_users()
        else:
            if choice == 1:
                show_user()
            elif choice == 2:
                functions.clear()
                new_user()
            elif choice == 3:
                functions.clear()
                update_user()
            elif choice == 4:
                functions.clear()
                delete_user()
            elif choice == 5:
                functions.clear()
                delete_users()
            elif choice == 6:
                exit()
    else:
        print(result)
        input('press enter to proceed...')
        functions.clear()
        show_users()


def show_user():
    pass


def delete_user():
    national_code = input("Please enter user's national_code: ")
    status, result = EmployeeDatabase.delete(national_code)


def delete_users():
    pass


def update_user():
    pass


def new_user():
    f_name = input('Please enter first name: ')
    l_name = input('Please enter last name: ')
    national_code = input('Please enter national code: ')
    birthday = input('Please enter birthday: ')
    status, image_result = take_screenshot()

    if status:
        cv2.imshow('result', cv2.imread(image_result))
        cv2.waitKey(0)
        status, result = EmployeeDatabase.insert(f_name, l_name, national_code, birthday, image_result)
        print('new user added successfully \n')
        input('press enter to proceed...')
        functions.clear()
        show_users()
    else:
        print(image_result)
        input('press enter to proceed...')
        functions.clear()
        new_user()


def login():
    phone_number = input('Please enter admin phone number: ')
    password = input('Please enter admin password: ')
    status, result = AdminDatabase.login(phone_number, password)
    print(result)
    input('press enter to proceed...')
    if status:
        functions.clear()
        show_users()
    else:
        functions.clear()
        login()


if __name__ == '__main__':
    functions.clear()
    login()
