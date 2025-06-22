# بعرف هنا ايه مش مكتوب قصاده int_code

import pandas as pd

# تحميل الملف بعد التعديل
df = pd.read_csv("outputs/all_data_with_type.csv")

# استخراج صفوف فيها Buy أو Sell لكن int_code فاضي
missing_codes = df[
    df["Type"].isin(["Buy", "Sell"]) &
    (df["int_code"].isna() | (df["int_code"].astype(str).str.strip() == ""))
]

# عرض أول 10 صفوف منهم
print(missing_codes.head(10))

# حفظهم في ملف للمراجعة
missing_codes.to_csv("outputs/buy_sell_missing_codes.csv", index=False, encoding="utf-8-sig")

print(f"✅ عدد صفقات Buy/Sell اللي int_code فيها فاضي: {len(missing_codes)}")
