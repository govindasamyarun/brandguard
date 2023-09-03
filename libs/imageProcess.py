import cv2
import pytesseract

class ImageProcess:
    def __init__(self, keyword, image_path) -> None:
        self.keyword = keyword
        self.image_path = image_path

    def analysis(self):
        # Load the image
        image = cv2.imread(self.image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform OCR to extract text from the image
        extracted_text = pytesseract.image_to_string(gray)

        # Check if the word is present in the extracted text
        if self.keyword.lower().replace(' ', '') in extracted_text.lower().replace(' ', ''):
            return True
        else:
            return False