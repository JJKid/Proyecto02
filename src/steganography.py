import os
from PIL import Image

def convertDecimalToBinary(num):
    """ 
    Converts a decimal number to a string with its binary representation of 8 bits

    """
    return '{0:08b}'.format(num)

def convertBinaryToChar(binaryNum):
    """ 
    Converts a string with an 8-bit binary number 
    to a decimal number and then to the char asociated to this decimal number in ASCII

    """
    return chr(int(binaryNum,2))

def convertBinaryToDecimal(num):
    """ 
    Converts a string with an 8-bit binary number to a decimal number
    
    """ 
    return int(num, 2) 

def convertTextToBinary(text):
    """ 
    Converts each character in a string of text to a binary string
    and returns a string with all binary strings joined into one string

    """
    # 
    if type(text) is str:
        return ''.join([convertDecimalToBinary(ord(c)) for c in text])

def hideText():
    """ 
    Hide text from a text file into an PNG image 
    with LSB steganography technique

    Overwrites the last bit of the binary representation of 
    the number asocciated with a color (R,B,G or A) on each pixel
    until the all input text converted to binary (with a delimiter at the end)
    gets saved

    Creates a PNG file with the text hidden, saves it on /out 

    """
    scriptDir = os.path.dirname(__file__)
    defaultImageFileName = "original.png"  
    defaultTextFileName = "input.txt"
    defaultOutputImageFileName = "modified.png"
    imageFileName = input(f"Enter original image file name (with .png extension). Press enter to use default image file: {defaultImageFileName} \n")
    if not imageFileName:
        imageFileName = defaultImageFileName
    imagePath = os.path.join(scriptDir, '../data/', imageFileName)
    image = Image.open(imagePath) 
    print("Image details: ", image.format, image.size, image.mode)

    textFileName = input(f"Enter text file name with text to hide (with .txt extension). Press enter to use default text file: {defaultTextFileName} \n")
    if not textFileName:
        textFileName = defaultTextFileName
    textFilePath = os.path.join(scriptDir, '../data/', textFileName)
    with open(textFilePath, 'r') as textFile:
        text = textFile.read().replace('\n', ' ')

    outputImageFileName = input(f"Enter output image file name (with .png extension). Press enter to use default output text file name: {defaultOutputImageFileName} \n")
    if not outputImageFileName:
        outputImageFileName = defaultOutputImageFileName
    
    textInBinary = convertTextToBinary(text) + '1111111111111110'
    currDigitIndex = 0
    pixelsGrid = image.load()    
    for i in range(image.size[0]):
        for j in range(image.size[1]):  
            r, g, b, a = image.getpixel((i, j))
            if currDigitIndex < len(textInBinary):
                rInbinaryModified = convertDecimalToBinary(r)[:-1] + textInBinary[currDigitIndex]
                r = convertBinaryToDecimal(rInbinaryModified)
                currDigitIndex+=1
            if currDigitIndex < len(textInBinary):
                gInbinaryModified = convertDecimalToBinary(g)[:-1] + textInBinary[currDigitIndex]
                g = convertBinaryToDecimal(gInbinaryModified)
                currDigitIndex+=1
            if currDigitIndex < len(textInBinary):
                bInbinaryModified = convertDecimalToBinary(b)[:-1] + textInBinary[currDigitIndex]
                b = convertBinaryToDecimal(bInbinaryModified)
                currDigitIndex+=1            
            if currDigitIndex < len(textInBinary):
                aInbinaryModified = convertDecimalToBinary(a)[:-1] + textInBinary[currDigitIndex]
                a = convertBinaryToDecimal(aInbinaryModified)
                currDigitIndex+=1
            pixelsGrid[i,j] = (r,g,b,a)

            if currDigitIndex == len(textInBinary):
                break  
        else:
            continue  
        break    
    
    outputImagePath = os.path.join(scriptDir, '../out/', outputImageFileName)
    image.save(outputImagePath)    
    print("Modified image saved on " + outputImagePath)
    
def unveilText():
    """ 
    Unveils hidden text inside a image file by LSB steganography technique
    

    Iterate over each pixel and save the last bit of the binary representation
    of each color and save it into a string which contains all this binary numbers extracted

    Once we found that the last 16 binary digits are equal to the 
    delimiter we stop reading more pixels

    Finally we convert each binary number of length 8 into its char representation 
    and append it to unveiledText string , which is written to output text file

    Creates a text file which contains the unveiled text from image, saves it on /out

    """    
    
    scriptDir = os.path.dirname(__file__)
    defaultOutputImageFileName = "modified.png"
    defaultOutputTextFileName = "output.txt"
    imageFileName = input(f"Enter image file name with hidden text (with .png extension). Press enter to use previous default output image file: {defaultOutputImageFileName} \n")
    if not imageFileName:
        imageFileName = defaultOutputImageFileName
    imagePath = os.path.join(scriptDir, '../out/', imageFileName)
    image = Image.open(imagePath) 
    print("Image details: ", image.format, image.size, image.mode)

    outputTextFileName = input(f"Enter output text file name (with .txt extension). Press enter to use default output text file name: {defaultOutputTextFileName} \n")
    if not outputTextFileName:
        outputTextFileName = defaultOutputTextFileName

    currExtractingBinaryString = ''
    delimiter = '1111111111111110'
    unveiledText = ''
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, a = image.getpixel((i, j))
            currExtractingBinaryString+= convertDecimalToBinary(r)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(g)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(b)[-1]
            currExtractingBinaryString+= convertDecimalToBinary(a)[-1]
            if len(currExtractingBinaryString) >= len(delimiter):
                if currExtractingBinaryString[-16:] == delimiter:
                    break
        else:
            continue  
        break  

    if len(currExtractingBinaryString) % 8 == 0:
        for i in range(0,len(currExtractingBinaryString),8):
            unveiledText+= convertBinaryToChar(currExtractingBinaryString[i: i+8])
    else:
        print("Extracted string is not multiple of 8")    
    
    print("Unveiled text: ", unveiledText[:-2])
    outputTextFilePath = os.path.join(scriptDir, '../out/', outputTextFileName)
    print("Unveiled text saved on " + outputTextFilePath)

    with open(outputTextFilePath, "w") as textFile:
        textFile.write(unveiledText[:-2])

def main():
    optionSelected = input("Type \n 1. h to hide \n 2. u to unveil \n Then press enter \n")
    if optionSelected == "h":
        hideText()
    if optionSelected == "u":
        unveilText()

if __name__ == "__main__":
    main()
