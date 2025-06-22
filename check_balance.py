
# عايزين نتحقق هل البيانات كاملة ولا لا، هنا بنطرح القيمة من الرصيد السابق ونشوف في تطابق مع الرصيد التالي ولا لا

import csv

csv_path = "outputs/all_data.csv"  

TOLERANCE = 0.5  # ← الهامش المسموح به

with open(csv_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    balance = 0.0
    line_number = 1
    all_ok = True

    for row in reader:
        try:
            value = float(row["Value"].replace(',', '').strip())
            expected_balance = balance + value

            actual_balance = float(row["Balance"].replace(',', '').strip())

            # ✅ السماح بالفرق داخل الهامش المحدد
            if abs(expected_balance - actual_balance) > TOLERANCE:
                print(f"❌ Line {line_number}: Expected {expected_balance:.1f}, got {actual_balance:.1f}")
                all_ok = False

            balance = actual_balance
            line_number += 1

        except Exception as e:
            print(f"⚠️ Error in line {line_number}: {e}")
            line_number += 1
            continue

if all_ok:
    print("✅ All balances are within the allowed margin.")
