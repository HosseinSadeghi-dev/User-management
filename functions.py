import random
import string
import os
import cv2


def save_image(image):
    try:
        path = 'assets/images/workers/'
        image_name = random_string()
        full_path = path + image_name + '.jpg'
        cv2.imwrite(full_path, image)
        return True, full_path
    except Exception as e:
        return False, 'error: ' + str(e)


def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def clear():
    # os.system('cls||clear')
    os.system('cls' if os.name == 'nt' else 'clear')
