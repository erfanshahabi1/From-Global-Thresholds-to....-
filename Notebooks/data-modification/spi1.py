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

for month_num, month_name in months:
    print(f"\n📂 پردازش ماه: {month_name.capitalize()}")

    file_path = os.path.join(base_path, f"{month_num}{month_name}.csv")
    if not os.path.exists(file_path):
        print(f"  ⚠️ فایل یافت نشد: {file_path}")
        continue

    df = pd.read_csv(file_path)

    # اعتبارسنجی
    if "valid_time" not in df.columns or "tp" not in df.columns or "region" not in df.columns:
        print(f"  ⛔ ستون‌های لازم در فایل وجود ندارند.")
        continue

    # اطمینان از فرمت زمانی
    df["valid_time"] = pd.to_datetime(df["valid_time"], errors="coerce")
    df = df.dropna(subset=["valid_time"])
    df = df[df["valid_time"].dt.month == month_num]

    # محاسبه‌ی SPI برای هر مختصات، با فیت گاما بر اساس داده‌های ناحیه
    spi_values = []

    for region_name in df["region"].unique():
        region_df = df[df["region"] == region_name]

        for (lat, lon) in region_df[["latitude", "longitude"]].drop_duplicates().values:
            point_mask = (region_df["latitude"] == lat) & (region_df["longitude"] == lon)
            series = region_df.loc[point_mask, "tp"].values

            if np.count_nonzero(np.isfinite(series)) < 30:
                spi = [np.nan] * len(series)
            else:
                try:
                    shape, loc, scale_param = gamma.fit(series[series > 0], floc=0)
                    cdf = gamma.cdf(series, shape, loc=loc, scale=scale_param)
                    spi = norm.ppf(np.clip(cdf, 1e-6, 1 - 1e-6))
                except:
                    spi = [np.nan] * len(series)

            # اضافه‌کردن نتایج
            spi_values.extend(zip(region_df.loc[point_mask].index, spi))

    # درج نتایج در دیتافریم
    spi_series = pd.Series(np.nan, index=df.index)
    for idx, value in spi_values:
        spi_series.at[idx] = value

    df["spi01"] = spi_series

    # ذخیره فایل خروجی
    df.to_csv(file_path, index=False)
    print(f"  ✅ فایل با SPI-01 ناحیه‌ای ذخیره شد: {file_path}")
