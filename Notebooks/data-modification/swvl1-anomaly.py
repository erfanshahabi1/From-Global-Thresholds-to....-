import os
import pandas as pd
import numpy as np

# 📁 مسیر جدید فایل‌ها
base_path = r"D:\projects\climate\climate\DATA\raw-data\monthly-merged-data\cleaned"

# لیست ماه‌ها با نام فایل منطبق
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

    if 'valid_time' not in df.columns or 'swvl1' not in df.columns or 'region' not in df.columns:
        print("  ⚠️ ستون‌های لازم (valid_time, swvl1, region) یافت نشد.")
        continue

    df['valid_time'] = pd.to_datetime(df['valid_time'], errors='coerce')
    df = df.dropna(subset=['valid_time'])
    df = df[df['valid_time'].dt.month == month_num]

    df["swvl1_anom"] = np.nan
    for region_name, region_df in df.groupby("region"):
        unique_coords = region_df.drop_duplicates(subset=["latitude", "longitude"])
        mean_val = unique_coords["swvl1"].mean()
        std_val = unique_coords["swvl1"].std()

        if std_val == 0 or np.isnan(std_val):
            print(f"  ⚠️ ناحیه {region_name}: انحراف معیار صفر یا NaN.")
            continue

        idx = region_df.index
        df.loc[idx, "swvl1_anom"] = (region_df["swvl1"] - mean_val) / std_val

    df.to_csv(file_path, index=False)
    print(f"  ✅ Z-score ناحیه‌ای برای swvl1 ذخیره شد: {file_path}")
