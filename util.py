import re
import cv2
import easyocr

# Calling the Reader from easyocr
reader = easyocr.Reader(['en'])


def string_to_number(string):
    # Create a dictionary of letters and their corresponding numbers.
    letter_to_number = {
        "A": "4",
        "B": "8",
        "E": "3",
        "G": "6",
        "I": "1",
        "O": "0",
        "R": "2",
        "C": "6",
        "T": "1",
        "M": "11",
        "/": "1",
    }

    # Convert the string to uppercase.
    string = str(string).upper()
    # Removing spaces
    string = string.replace(" ", "")

    # Convert each letter in the string to its corresponding number.
    number_string = ""
    for letter in string:
        if letter in letter_to_number:
            number_string += letter_to_number[letter]
        else:
            number_string += letter

    # Return the string of numbers.
    return number_string


def correctFormat(plate_number):
    plate_number = str(plate_number)
    if plate_number.__len__() >= 6 and plate_number.__len__() < 12:
        return True
    else:
        return False


def extract_license_plate_number(img):
    # Read the image and convert it to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (1, 1), 0)
    # Apply thresholding to the image
    _, thres = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
    # Read the text from the thresholded image
    result = reader.readtext(thres)
    cv2.imwrite(thres,'./Captures/thres.jpg')
    # Get the number of lines in the text
    num_lines = len(result)

    if num_lines == 0:
        return "No text detected. License plate number could not be extracted."

    # Initialize the license plate number as an empty string
    licensePlateNumber = ""
    # Initialize the score of the license plate number to 0
    licensePlateScore = 0
    # Iterate over the lines of text and concatenate them to the license plate number and calculate the score
    for number in reversed(range(0, num_lines)):
        licensePlateNumber += result[number][1]
        licensePlateScore += result[number][2]
    # Calculating the score of the license plate number
    licensePlateScore /= num_lines
    licensePlateScore *= 100
    licensePlateScore = int(licensePlateScore)
    # Convert the license plate number to a string of numbers
    licensePlateNumber = string_to_number(licensePlateNumber)
    # Print the license plate number
    if correctFormat(licensePlateNumber):
        return licensePlateNumber
    else:
        return "ERROR"
