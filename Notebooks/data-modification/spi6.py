import os
import pandas as pd
import numpy as np
from scipy.stats import gamma, norm
import warnings

# مسیر داده‌های CSV ناحیه‌بندی‌شده (cleaned)
base_path = r"D:\projects\climate\climate\DATA\raw-data\monthly-merged-data\cleaned"

# لیست ماه‌ها
months = [
    (1, "JANUARY"), (2, "FEBRUARY"), (3, "MARCH"), (4, "APRIL"),
    (5, "MAY"), (6, "JUNE"), (7, "JULY"), (8, "AUGUST"),
    (9, "SEPTEMBER"), (10, "OCTOBER"), (11, "NOVEMBER"), (12, "DECEMBER")
]

# نادیده‌گرفتن هشدارها برای فیت ناموفق
warnings.filterwarnings("ignore")

# 🔢 تعداد ماه‌های تجمعی برای SPI-06
window_size = 6

for month_num, month_name in months:
    print(f"\n📂 پردازش ماه: {month_name.capitalize()}")

    file_path = os.path.join(base_path, f"{month_num}{month_name}.csv")
    if not os.path.exists(file_path):
        print(f"  ⚠️ فایل یافت نشد: {file_path}")
        continue

    df = pd.read_csv(file_path)

    # بررسی وجود ستون‌های ضروری
    if "valid_time" not in df.columns or "tp" not in df.columns or "region" not in df.columns:
        print(f"  ⛔ ستون‌های لازم در فایل وجود ندارند.")
        continue

    # تبدیل و فیلتر زمان
    df["valid_time"] = pd.to_datetime(df["valid_time"], errors="coerce")
    df = df.dropna(subset=["valid_time"])
    df = df[df["valid_time"].dt.month == month_num]

    # مرتب‌سازی داده‌ها برای محاسبه دقیق rolling
    df = df.sort_values(by=["region", "latitude", "longitude", "valid_time"])

    spi_values = []

    for region_name in df["region"].unique():
        region_df = df[df["region"] == region_name]

        for (lat, lon), group in region_df.groupby(["latitude", "longitude"]):
            group = group.sort_values("valid_time")
            rolling_tp = group["tp"].rolling(window=window_size, min_periods=window_size).sum()

            if rolling_tp.isna().sum() > len(rolling_tp) - 30:
                spi = [np.nan] * len(group)
            else:
                try:
                    valid_values = rolling_tp.dropna()
                    shape, loc, scale_param = gamma.fit(valid_values[valid_values > 0], floc=0)
                    cdf = gamma.cdf(rolling_tp, shape, loc=loc, scale=scale_param)
                    spi = norm.ppf(np.clip(cdf, 1e-6, 1 - 1e-6))
                except:
                    spi = [np.nan] * len(group)

            spi_values.extend(zip(group.index, spi))

    # درج نتایج
    spi_series = pd.Series(np.nan, index=df.index)
    for idx, val in spi_values:
        spi_series.at[idx] = val

    df["spi06"] = spi_series

    # ذخیره‌سازی فایل خروجی
    df.to_csv(file_path, index=False)
    print(f"  ✅ فایل با SPI-06 ناحیه‌ای ذخیره شد: {file_path}")
