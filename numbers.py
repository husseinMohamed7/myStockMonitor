# import pandas as pd

# # حمل البيانات
# df = pd.read_csv("codes/upload_to_suprest/Final.csv")

# # الأعمدة اللي المفروض تكون أرقام
# numeric_cols = ["Value", "Balance", "Quantity"]

# # نتأكد إنها كلها قابلة للتحويل إلى float
# for col in numeric_cols:
#     try:
#         # نحاول نحولها بعد إزالة الفواصل
#         df[col] = df[col].astype(str).str.replace(",", "").astype(float)
#         print(f"✅ Column '{col}' is clean and numeric.")
#     except Exception as e:
#         print(f"❌ Column '{col}' has issues: {e}")


import pandas as pd

# تحميل الملفات
main_df = pd.read_csv("final_output.csv")
stocks_df = pd.read_csv("outputs/Company_Codes.csv")

# التأكد من أن الكمية عددية حتى نقدر نقسم
main_df["Quantity"] = pd.to_numeric(main_df["Quantity"], errors="coerce")
main_df["Value"] = pd.to_numeric(main_df["Value"].astype(str).str.replace(",", ""), errors="coerce")

# إنشاء عمود pricePerShare
main_df["pricePerShare"] = main_df["Value"] / main_df["Quantity"]

# إنشاء عمود cashFlow يساوي القيمة زي ما هي (موجب أو سالب)
main_df["cashFlow"] = main_df["Value"]

# جلب أسماء الأسهم بناءً على int_code
main_df = main_df.merge(stocks_df, on="int_code", how="left")

# حفظ الملف النهائي بتنسيق CSV UTF-8

print("✅ تم إنشاء الملف final_output.csv بنجاح.")
main_df["Date"] = pd.to_datetime(main_df["Date"], dayfirst=True)
main_df.to_csv("final_output.csv", index=False, encoding="utf-8-sig")
