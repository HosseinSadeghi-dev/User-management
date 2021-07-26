import cv2
import numpy as np
import math


# helping hsv function
def hsv(img, lower, upper):
    _hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _lower = np.array([lower, 128, 128])
    _upper = np.array([upper, 255, 255])
    return cv2.inRange(_hsv, _lower, _upper)


# pencil sketch
def filter1(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(gray)
    gblur_img = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    dodged_img = cv2.divide(gray, 255 - gblur_img, scale=256)
    final_image = 255 - cv2.divide(255 - dodged_img, 255 - gblur_img, scale=256)
    return final_image


# sepia
def filter2(image):
    image = np.array(image, dtype=np.float64)  # converting to float to prevent loss
    image = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
                                            [0.349, 0.686, 0.168],
                                            [0.393, 0.769, 0.189]]))  # multipying image with special sepia matrix
    image[np.where(image > 255)] = 255
    image = np.array(image, dtype=np.uint8)
    return image


# splash filter
def filter3(image):
    res = np.zeros(image.shape, np.uint8)
    lower = 15
    upper = 30
    mask = hsv(image, lower, upper)
    inv_mask = cv2.bitwise_not(mask)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res1 = cv2.bitwise_and(image, image, mask=mask)
    res2 = cv2.bitwise_and(gray, gray, mask=inv_mask)
    for i in range(3):
        res[:, :, i] = res2
    img = cv2.bitwise_or(res1, res)
    return img


# cartoon
def filter4(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
    dst = cv2.edgePreservingFilter(image, flags=2, sigma_s=64,
                                   sigma_r=0.25)
    cartoon = cv2.bitwise_and(dst, dst, mask=edges2)
    return cartoon


# color sketch
def filter5(image):
    _, dst_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07,
                                    shade_factor=0.05)
    return dst_color


# Emboss
def filter6(image):
    height, width = image.shape[:2]
    y = np.ones((height, width), np.uint8) * 128
    output = np.zeros((height, width), np.uint8)

    kernel1 = np.array([[0, -1, -1],
                        [1, 0, -1],
                        [1, 1, 0]])
    kernel2 = np.array([[-1, -1, 0],
                        [-1, 0, 1],
                        [0, 1, 1]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    output1 = cv2.add(cv2.filter2D(gray, -1, kernel1), y)
    output2 = cv2.add(cv2.filter2D(gray, -1, kernel2), y)
    for i in range(height):
        for j in range(width):
            output[i, j] = max(output1[i, j], output2[i, j])

    return output


# wavy
def filter7(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows, cols = image.shape
    img_output = np.zeros((rows, cols), dtype=image.dtype)

    for i in range(rows):
        for j in range(cols):
            offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
            offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
            if i + offset_y < rows and j + offset_x < cols:
                img_output[i, j] = image[(i + offset_y) % rows, (j + offset_x) % cols]
            else:
                img_output[i, j] = 0
    return img_output


# mexican hat
def filter8(image):
    _filter = np.array(
        [[0, 0, -1, 0, 0],
         [0, -1, -2, -1, 0],
         [-1, -2, 16, -2, -1],
         [0, -1, -2, -1, 0],
         [0, 0, -1, 0, 0]]
    )
    return cv2.filter2D(image, -1, _filter)


# max rgb
def filter9(image):
    (B, G, R) = cv2.split(image)

    m = np.maximum(np.maximum(R, G), B)
    R[R < m] = 0
    G[G < m] = 0
    B[B < m] = 0

    filtered = cv2.merge([B, G, R])
    return filtered


if __name__ == '__main__':
    test_image = cv2.imread('assets/images/test.jpg')
    result = filter9(test_image)
    cv2.imshow('result', result)
    cv2.waitKey(0)
