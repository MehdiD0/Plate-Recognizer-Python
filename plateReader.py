import cv2
import os
from util import *
#from dataBase import *

def readLiscencePlate():
  # Load the image
  image = cv2.imread('./Captures/screen.jpg')


  licensePlateNumber = extract_license_plate_number(image)
  #if allowGoingIn(str(licensePlateNumber)):
    #return True
  #else:
    #return False
  return True