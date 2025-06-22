# ملف التحويل الرئيسي

import fitz
import csv
import re
import os

output_csv = "all_data.csv"
folder_path = "../"  # نفس المجلد
file_range = range(28, 29) 

rows = []

for num in file_range:
    filename = f"{num:03}.pdf"
    pdf_path = os.path.join(folder_path, filename)

    if not os.path.exists(pdf_path):
        print(f"File not found: {filename}")
        continue

    doc = fitz.open(pdf_path)
    lines = []
    for page in doc:
        text = page.get_text()
        lines.extend(text.split('\n'))

    lines = lines[14:]  # إزالة أول هيدر

    # وقف عند "رصيد آخر المدة"
    for i, line in enumerate(lines):
        if "رصيد آخر المدة" in line:
            lines = lines[:i]
            break

    # فلترة السطور: تجاهل [سطر فاضي + سطر فيه رقم صفحة + 4 سطور بعده]
    cleaned_lines = []
    i = 0
    while i < len(lines):
        if (
            lines[i].strip() == "" and
            i + 1 < len(lines) and
            re.match(r'^\d+/\d+$', lines[i + 1].strip())
        ):
            # تجاهل هذا السطر + رقم الصفحة + 4 سطور بعده
            i += 6
        else:
            cleaned_lines.append(lines[i].strip())
            i += 1

    # استخراج العمليات
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', line)

        if match:
            date = match.group(0)

            if line != date:
                description = line.replace(date, '').strip()
                value = cleaned_lines[i - 1] if i - 1 >= 0 else ''
                balance = cleaned_lines[i - 2] if i - 2 >= 0 else ''
            else:
                description = cleaned_lines[i - 1] if i - 1 >= 0 else ''
                value = cleaned_lines[i - 2] if i - 2 >= 0 else ''
                balance = cleaned_lines[i - 3] if i - 3 >= 0 else ''

            if all([balance, value, description, date]):
                rows.append([date, description, value, balance])
            else:
                print(f"Skipped entry in {filename} due to missing data")
        i += 1

# حفظ النتيجة
with open(output_csv, "w", newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Description", "Value", "Balance"])
    writer.writerows(rows)

print(f"Extracted {len(rows)} rows from {len(file_range)} files into {output_csv}")
