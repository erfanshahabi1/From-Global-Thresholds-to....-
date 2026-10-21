import os
import xarray as xr
import numpy as np
import pandas as pd

base_path = r"D:\projects\climate\climate\DATA\raw-data\extract-data"

seasons = {
    "spring": [3, 4, 5],
    "summer": [6, 7, 8],
    "autumn": [9, 10, 11],
    "winter": [12, 1, 2],
}

month_names = ['1January', '2February', '3March', '4April', '5May', '6June',
               '7July', '8August', '9September', '10October', '11November', '12December']

monthly_tp = {}

# بارگذاری داده‌های tp از هر ماه
for i, folder in enumerate(month_names, start=1):
    folder_path = os.path.join(base_path, folder)
    if not os.path.isdir(folder_path):
        continue
    for file in os.listdir(folder_path):
        if file.endswith(".nc"):
            file_path = os.path.join(folder_path, file)
            try:
                ds = xr.open_dataset(file_path, decode_times=True, use_cftime=True)
                if 'tp' in ds.variables:
                    tp = ds['tp']
                    time_dim = 'valid_time' if 'valid_time' in tp.dims else 'time'
                    tp = tp.sel({time_dim: slice("1940-01-01", "2025-12-31")})
                    tp = tp.rename({time_dim: 'time'})
                    monthly_tp[i] = tp
                    break
            except:
                continue

# بررسی اینکه همه‌ی ماه‌ها کامل باشند
if len(monthly_tp) != 12:
    print("❌ برخی ماه‌ها یافت نشدند.")
    exit()

# ادغام و مرتب‌سازی داده‌ها
combined_tp = xr.concat([monthly_tp[m] for m in range(1, 13)], dim='time')
combined_tp = combined_tp.sortby('time')

# افزودن مختصات سال و ماه از cftime
combined_tp = combined_tp.assign_coords(
    month=("time", [t.month for t in combined_tp.time.values]),
    year=("time", [t.year for t in combined_tp.time.values])
)

# محاسبه بارش فصلی
seasonal_tp = {}

for season, months in seasons.items():
    if season == 'winter':
        jan_feb = combined_tp.where(combined_tp['month'].isin([1, 2]))
        dec = combined_tp.where(combined_tp['month'] == 12)
        dec = dec.assign_coords(year=dec['year'] + 1)
        season_data = xr.concat([dec, jan_feb], dim='time')
    else:
        season_data = combined_tp.where(combined_tp['month'].isin(months))

    # جمع فقط وقتی هر سه ماه موجودند
    seasonal_sum = season_data.groupby('year').sum(dim='time', skipna=True, min_count=3)
    seasonal_tp[season] = seasonal_sum

# محاسبه SPI برای هر فصل
spi_results = {}

for season, data in seasonal_tp.items():
    ref = data.sel(year=slice(1980, 2010))
    mean_ref = ref.mean(dim='year')
    std_ref = ref.std(dim='year')

    # جلوگیری از تقسیم بر صفر یا انحراف معیار بسیار کوچک
    safe_std_ref = std_ref.copy()
    safe_std_ref = safe_std_ref.where(safe_std_ref > 0.01, 0.01)

    # محاسبه SPI
    spi = (data - mean_ref) / std_ref
    spi.name = f"spi_{season}"

    # پاکسازی مقادیر پرت بسیار بزرگ یا غیرواقعی
    spi = spi.where(np.abs(spi) < 10)

    # ذخیره NetCDF
    out_nc = os.path.join(base_path, f"spi_{season}.nc")
    spi.to_netcdf(out_nc)

    # ذخیره CSV
    df = spi.to_dataframe().reset_index()
    out_csv = os.path.join(base_path, f"spi_{season}.csv")
    df.to_csv(out_csv, index=False)

    print(f"✅ SPI cleaned and saved for {season}")

