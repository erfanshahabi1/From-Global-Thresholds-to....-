import os
import pandas as pd
import numpy as np

# 📁 مسیر فایل‌ها
base_path = r"D:\projects\climate\climate\DATA\raw-data\monthly-merged-data\cleaned"

# لیست ماه‌ها
months = [
    (1, "JANUARY"), (2, "FEBRUARY"), (3, "MARCH"), (4, "APRIL"),
    (5, "MAY"), (6, "JUNE"), (7, "JULY"), (8, "AUGUST"),
    (9, "SEPTEMBER"), (10, "OCTOBER"), (11, "NOVEMBER"), (12, "DECEMBER")
]

for month_num, month_name in months:
    print(f"\n📂 پردازش فایل: {month_name}")

    file_name = f"{month_num}{month_name}.csv"
    file_path = os.path.join(base_path, file_name)

    if not os.path.exists(file_path):
        print(f"  ⚠️ فایل یافت نشد: {file_path}")
        continue

    df = pd.read_csv(file_path)

    if 'valid_time' not in df.columns or 'tp' not in df.columns or 'region' not in df.columns:
        print("  ⛔ ستون‌های لازم یافت نشدند.")
        continue

    # 🕒 فیلتر رکوردهای مربوط به ماه مورد نظر
    df['valid_time'] = pd.to_datetime(df['valid_time'], errors='coerce')
    df = df.dropna(subset=['valid_time'])
    df = df[df['valid_time'].dt.month == month_num]

    # 🧮 محاسبه Z-Score ناحیه‌ای با حذف نقاط تکراری در آمارگیری
    df["tp_anom"] = np.nan
    for region_name, region_df in df.groupby("region"):
        unique_points = region_df.drop_duplicates(subset=["latitude", "longitude"])
        mean_val = unique_points["tp"].mean()
        std_val = unique_points["tp"].std()

        if std_val == 0 or np.isnan(std_val):
            print(f"  ⚠️ ناحیه {region_name}: std صفر یا NaN.")
            continue

        idx = region_df.index
        df.loc[idx, "tp_anom"] = (region_df["tp"] - mean_val) / std_val

    # 💾 ذخیره خروجی
    df.to_csv(file_path, index=False)
    print(f"  ✅ Z-score ناحیه‌ای برای tp ذخیره شد: {file_path}")
