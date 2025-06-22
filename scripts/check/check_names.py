# بشكل مباشر هنقارن بين الاسم في الوصف وبين اسم الشركة عشان نتأكد انه عمل اقتران صح

import pandas as pd

# تحميل الملفات
df = pd.read_csv("outputs/all_data_with_type.csv")
companies = pd.read_csv("outputs/Company_Codes.csv")

# تأكد إن الأعمدة موجودة
assert "int_code" in df.columns
assert "Description" in df.columns
assert "int_code" in companies.columns
assert "name" in companies.columns

# دمج على أساس int_code
merged = df[["int_code", "Description"]].merge(
    companies[["int_code", "name"]],
    on="int_code",
    how="left"
)

# حذف الصفوف اللي int_code فيها فاضي
merged = merged[merged["int_code"].notna() & (merged["int_code"].astype(str).str.strip() != "")]

# حفظ للمراجعة اليدوية
merged.to_csv("outputs/code_description_name_check.csv", index=False, encoding="utf-8-sig")
print("✅ تم إنشاء جدول المراجعة: code_description_name_check.csv")
