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

    if 'valid_time' not in df.columns or 'ssrd' not in df.columns or 'region' not in df.columns:
        print("  ⚠️ ستون‌های لازم (valid_time, ssrd, region) یافت نشد.")
        continue

    # تبدیل زمان و فیلتر ماه درست
    df['valid_time'] = pd.to_datetime(df['valid_time'], errors='coerce')
    df = df.dropna(subset=['valid_time'])
    df = df[df['valid_time'].dt.month == month_num]

    # آماده‌سازی ستون آنومالی
    df["ssrd-anom"] = np.nan

    # اجرای ناحیه به ناحیه
    for region_name in df["region"].unique():
        region_df = df[df["region"] == region_name]

        # فقط یک بار از هر مختصات استفاده می‌کنیم برای آمار منطقه
        unique_points = region_df.drop_duplicates(subset=["latitude", "longitude"])
        mean_val = unique_points["ssrd"].mean()
        std_val = unique_points["ssrd"].std()

        if std_val == 0 or np.isnan(std_val):
            print(f"  ⚠️ ناحیه {region_name}: انحراف معیار صفر یا NaN.")
            continue

        # اعمال Z-score فقط بر ردیف‌های همان region
        idx = region_df.index
        df.loc[idx, "ssrd-anom"] = (region_df["ssrd"] - mean_val) / std_val

    # ذخیره فایل نهایی
    df.to_csv(file_path, index=False)
    print(f"  ✅ Z-score ناحیه‌ای ذخیره شد: {file_path}")
