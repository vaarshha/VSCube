from PIL import Image
from pytesseract import pytesseract


def read_image(path, path_to_tesseract='C:\\Program Files\\Tesseract-OCR'):
    # Defining paths to tesseract.exe
    #pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    # and the image we would be using
    image_path = path
    pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR'
    # Opening the image & storing it in an image object
    img = Image.open(image_path)

    # Providing the tesseract executable
    # location to pytesseract library

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)

    # Displaying the extracted text
    return text[:-1]



