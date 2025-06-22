# import pandas as pd
# import re


# main_df = pd.read_csv("final_output.csv")

# # دالة لاستخراج pricePerShare والكمية من الوصف
# def extract_price_qty(desc):
#     match = re.search(r"([\d.]+)@([\d,]+)\(", desc)
#     if match:
#         price = float(match.group(1))
#         qty = int(match.group(2).replace(",", ""))  # لو فيه فواصل
#         return price, qty
#     return None, None

# # تطبيق الدالة
# main_df[["pricePerShare", "Quantity_extracted"]] = main_df["Description"].apply(
#     lambda x: pd.Series(extract_price_qty(x))
# )

# # لو عمود Quantity الأصلي ناقص نملأه بالقيم المستخرجة
# main_df["Quantity"] = main_df["Quantity"].fillna(main_df["Quantity_extracted"])
# main_df.drop(columns=["Quantity_extracted"], inplace=True)


# main_df.to_csv("final_output.csv", index=False, encoding="utf-8-sig")


import pandas as pd

df = pd.read_csv("transactions.csv")

def get_direction_by_sign(value):
    if pd.isna(value):
        return "Neutral"
    elif value > 0:
        return "Inflow"
    elif value < 0:
        return "Outflow"
    else:
        return "Neutral"

df["Direction"] = df["CashFlow"].apply(get_direction_by_sign)

df.to_csv("transactions.csv", index=False, encoding="utf-8-sig")
