import os
from PIL import Image
class Steganography:
    def __init__(self, image):
        self.image = image

def convertDecimalToBinary(num):
    return '{0:08b}'.format(num)

def convertBinaryToChar(binaryNum):
    print(binaryNum, len(binaryNum), int(binaryNum,2))
    return chr(int(binaryNum,2))

def convertBinaryToDecimal(num): 
    return int(num, 2) 

def convertTextToBinary(text):
    # Convert each character in the string of text
    # to a binary string
    # Return all binary strings joined into one string
    for c in text:
        print(c, convertDecimalToBinary(ord(c)))
    if type(text) is str:
        return ''.join([convertDecimalToBinary(ord(c)) for c in text])

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
    textInBinary = convertTextToBinary(text) + '1111111111111110'
    print("Text in binary", len(textInBinary), textInBinary)
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
    listofbinaries = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):  
            r, g, b, a = image.getpixel((i, j))
            if currDigitIndex < len(textInBinary):
                rInbinaryModified = convertDecimalToBinary(r)[:-1] + textInBinary[currDigitIndex]
                r = convertBinaryToDecimal(rInbinaryModified)
                currDigitIndex+=1
            if currDigitIndex < len(textInBinary):
                bInbinaryModified = convertDecimalToBinary(b)[:-1] + textInBinary[currDigitIndex]
                b = convertBinaryToDecimal(bInbinaryModified)
                currDigitIndex+=1
            if currDigitIndex < len(textInBinary):
                gInbinaryModified = convertDecimalToBinary(g)[:-1] + textInBinary[currDigitIndex]
                g = convertBinaryToDecimal(gInbinaryModified)
                currDigitIndex+=1
            if currDigitIndex < len(textInBinary):
                aInbinaryModified = convertDecimalToBinary(a)[:-1] + textInBinary[currDigitIndex]
                a = convertBinaryToDecimal(aInbinaryModified)
                currDigitIndex+=1
            listofbinaries.append((rInbinaryModified, bInbinaryModified, gInbinaryModified, aInbinaryModified))
            pixelMap[i,j] = (r,g,b,a)
            print(currDigitIndex)
            if currDigitIndex == len(textInBinary):
                print(" Break Ultimo indice", currDigitIndex, i,j)
                break  
        else:
            # Continue to next i iteration if inner for loop finish 
            continue  
        break    
    
    sequence_of_pixels = image.getdata()
    list_of_pixels = list(sequence_of_pixels)
    print(listofbinaries)
    print("mensaje en binario", textInBinary)
    outputImagePath = os.path.join(scriptDir, '../data/', "modifiedImage.png")
    image.save(outputImagePath)
    image.show()
    
    
    
def unveilText():
    # Iterate over each pixel 
    # Extract up to 4 LSB and save it into a currExtractingBinaryString
    # Once we found that the last 16 binary digits are equal to the 
    # delimiter we stop reading more pixels
    # For each string of binary chars of length == 8 in currExtractingBinaryString,
    # we convert it into its char representation and append it to unveiledText string
    
    # We save the unveiledText string to an output text file 
    imageFileName = input("Enter image file name with hidden text\n")
    scriptDir = os.path.dirname(__file__)
    imagePath = os.path.join(scriptDir, '../data/', imageFileName)
    image = Image.open(imagePath) 
    print(image.format, image.size, image.mode)
    textFileName = input("Enter text file name \n")
    print(textFileName)
    pixelMap = image.load()

    sequence_of_pixels = image.getdata()
    list_of_pixels = list(sequence_of_pixels)

    currExtractingBinaryString = ''
    delimiter = '1111111111111110'
    unveiledText = ''
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, a = image.getpixel((i, j))
            print((convertDecimalToBinary(r),convertDecimalToBinary(g),convertDecimalToBinary(b),convertDecimalToBinary(a)))
            currExtractingBinaryString+= convertDecimalToBinary(r)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(g)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(b)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(a)[-1]
            print((convertDecimalToBinary(r)[-1],convertDecimalToBinary(g)[-1],convertDecimalToBinary(b)[-1],convertDecimalToBinary(a)[-1]))
            if len(currExtractingBinaryString) >= len(delimiter):
                if currExtractingBinaryString[-16:] == delimiter:
                    print("Delimiter found", len(currExtractingBinaryString) , currExtractingBinaryString)
                    break
        else:
            # Continue to next i iteration if inner for loop finish 
            continue  
        break  

    print("Binary extracted text", currExtractingBinaryString, len(currExtractingBinaryString) )
    if len(currExtractingBinaryString) % 8 == 0:
        for i in range(0,len(currExtractingBinaryString),8):
            unveiledText+= convertBinaryToChar(currExtractingBinaryString[i: i+8])
    else:
        print("Extracted string is not multiple of 8")    
    
    print("Unveiled text", unveiledText[:-2])

def main():
    optionSelected = input("Seleccione la opcion deseada \n h para ocultar \n u para develar \n")
    if optionSelected == "h":
        hideText()
    if optionSelected == "u":
        unveilText()
    


if __name__ == "__main__":
    main()
