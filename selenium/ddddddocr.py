import ddddocr

ocr = ddddocr.DdddOcr()

image = open(r"C:\Users\Administrator\Desktop\imgcode.jpg", "rb").read()
result = ocr.classification(image)
print(result)