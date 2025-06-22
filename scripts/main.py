import pandas as pd
import re
from rapidfuzz import process, fuzz  

# تحميل البيانات
df = pd.read_csv("outputs/History.csv")
companies = pd.read_csv("outputs/Company_Codes.csv")

# تحضير الأعمدة
df["Type"] = ""
df["int_code"] = ""
df["Quantity"] = ""

# تجهيز قائمة الأسماء النظيفة
company_map = {
    name.strip().lower(): code.strip()
    for name, code in zip(companies["name"], companies["int_code"])
}
company_names = list(company_map.keys())  # أسماء الشركات فقط

# استخراج عدد الأسهم من (@العدد)
def extract_quantity(desc):
    match = re.search(r'@([\d,]+)', str(desc))
    if match:
        try:
            return int(match.group(1).replace(',', ''))
        except ValueError:
            return ""
    return ""


# قائمة الكلمات المفتاحية
keywords_map = {
    "رسوم": "Fee",
    "Fee": "Fee",
    "مصروفات": "Fee",
    "ايداع": "Deposit",
    "تحفيز": "Bonus",
    "Incentive": "Bonus",
    "تحويل": "Withdrawal"
}

# دالة مطابقة غامضة للاسم
def fuzzy_find_code(desc):
    result = process.extractOne(desc.lower(), company_names, scorer=fuzz.token_set_ratio)
    if result and result[1] >= 60:  # لو التشابه ≥ 90%
        matched_name = result[0]
        return company_map[matched_name]
    return ""

# تطبيق التصنيف
for i, row in df.iterrows():
    desc = str(row["Description"])

    # توزيعات أرباح
    if "Dividends" in desc:
        df.at[i, "Type"] = "Dividend"
        match = re.search(r'EGS\w{9}', desc)
        df.at[i, "int_code"] = match.group(0) if match else ""
        continue

    # كلمات مفتاحية
    for keyword, type_value in keywords_map.items():
        if keyword in desc:
            df.at[i, "Type"] = type_value
            break

    # شراء
    if "شراء" in desc:
        df.at[i, "Type"] = "Buy"
        df.at[i, "Quantity"] = extract_quantity(desc)
        found = False
        for name in company_map:
            if name in desc:
                df.at[i, "int_code"] = company_map[name]
                found = True
                break
        if not found:
            df.at[i, "int_code"] = fuzzy_find_code(desc)

    # بيع
    elif "بيع" in desc:
        df.at[i, "Type"] = "Sell"
        df.at[i, "Quantity"] = extract_quantity(desc)
        found = False
        for name in company_map:
            if name in desc:
                df.at[i, "int_code"] = company_map[name]
                found = True
                break
        if not found:
            df.at[i, "int_code"] = fuzzy_find_code(desc)

# حفظ الملف
df.to_csv("outputs/all_data_with_type.csv", index=False, encoding="utf-8-sig")
print("✅ تم إضافة fuzzy match وربط الشركات بنجاح.")
