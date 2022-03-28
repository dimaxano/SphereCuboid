import cv2
import numpy as np

if __name__ == "__main__":
    img = cv2.imread("./cuboid-sphere.png", 0)
    
    img = cv2.medianBlur(img, 5)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 300,
                            param1=20, param2=80, minRadius=0, maxRadius=0)
    
    circles = np.uint16(np.around(circles))
    radius = circles[0, 0, 2]

    print(f"Circle area: {np.pi * radius ** 2}")