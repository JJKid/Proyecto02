import os
from PIL import Image
class Steganography:
    def __init__(self, image):
        self.image = image

def convertDecimalToBinary(num):
    return bin(num).replace("0b", "")

def convertBinaryToDecimal(num): 
    return int(num, 2) 

def convertTextToBinary(text):
    # Convert each character in the string of text
    # to a binary string
    # Return all binary strings joined into one string
    if type(text) is str:
        return ''.join([format(ord(c), 'b') for c in text])

def hideText():
    imageFileName = input("Enter image file name \n")
    # read image
    scriptDir = os.path.dirname(__file__)
    imagePath = os.path.join(scriptDir, '../data/', imageFileName)
    image = Image.open(imagePath) 
    print(image.format, image.size, image.mode)

    textFileName = input("Enter text file name \n")
    textFilePath = os.path.join(scriptDir, '../data/', textFileName)
    with open(textFilePath, 'r') as file:
        text = file.read().replace('\n', ' ')
    # save text into string variable
    print("Text file name", text)
    print(len(text), type(convertTextToBinary(text)), convertTextToBinary(text))
    textInBinary = convertTextToBinary(text) + '111111111110'
    currDigitIndex = 0
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    pixelMap = image.load()
    testPixel = pixelMap[50,50]
    print("testPixel", testPixel)
    rInBinary = convertDecimalToBinary(testPixel[0])
    rInbinaryModified = rInBinary[:-1] + '1'
    # Test if last character is different before doing an overwrite on LSB
    print("r in binary" , rInBinary)
    print("r modified in binary" , rInbinaryModified)
    print("r back to decimal", convertBinaryToDecimal(rInBinary))
    print("r modified back to decimal", convertBinaryToDecimal(rInbinaryModified))

    for i in range(image.size[0]):    # for every col:
        for j in range(image.size[1]):  
            r, g, b, a = image.getpixel((i, j))
            # For every row
            # pixelMap[i,j] = (r,g,b,a)
            #if currDigitIndex < len(textInBinary):
            #    r = convertDecimalToBinary(r)
            #else:
            #    break

            # set the colour accordingly


    image.save("modifiedImage.png")
    image.show()

    
    
def unveilText():
    print("hi")

def main():
    optionSelected = input("Seleccione la opcion deseada \n h para ocultar \n u para develar \n")
    if optionSelected == "h":
        hideText()


if __name__ == "__main__":
    main()
