import pytesseract
from PIL import Image, ImageFilter, ImageEnhance

def recognizecharacters(image):

    imgobj = Image.open(image)
    imgobj = imgobj.convert('L')
    imgobj = imgobj.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(imgobj)
    imgobj = enhancer.enhance(2)
    text = pytesseract.image_to_string(imgobj)
    return text

if __name__ == "__main__":
    print(recognizecharacters("22862.jpeg"))