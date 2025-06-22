# استخدمت ده في البداية لتحويل نص نسخته من موقع البورصة المصرية لجدول

import csv

with open('file.csv', 'r', encoding='utf-8') as infile:
    lines = [line.strip() for line in infile if line.strip()]

# افترض إن كل اسم يليه كود، فهنقسمهم اتنينات
rows = [(lines[i], lines[i+1]) for i in range(0, len(lines), 2)]

# نكتبهم في ملف CSV
with open('Final.csv', 'w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Company Name', 'Company Code'])
    writer.writerows(rows)

print("✅ تم التحويل إلى output.csv")

