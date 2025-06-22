# أثناء معالجة الpdf
# بعرض كل السطور عشان اعرف شكلها ازاي واقدر اتعامل معاها

import fitz

pdf_path = "../last.pdf"
doc = fitz.open(pdf_path)

lines = []
for page in doc:
    text = page.get_text()
    lines.extend(text.split('\n'))

# نطبع السطور من بعد الهيدر
for i in range(0, min(len(lines), 2000)):
    print(f"{i}: {lines[i]}")
