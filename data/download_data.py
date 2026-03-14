"""
Download and extract Shenzhen air quality data from quotsoft.net
Data source: China National Environmental Monitoring Centre
"""
import urllib.request
import csv
import io
import os
from datetime import datetime, timedelta

OUTPUT_DIR = "/home/node/.openclaw/workspace/gba-air-quality-analysis/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# We'll download city-level daily data and extract Shenzhen
# Date range: 2019-01-01 to 2024-12-31
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 12, 31)

# Collect all Shenzhen data
all_rows = []
current_date = start_date
failed_dates = []
total_days = (end_date - start_date).days + 1

print(f"Downloading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Total days to download: {total_days}")

day_count = 0
while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    url = f"https://quotsoft.net/air/data/china_cities_{date_str}.csv"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
            reader = csv.reader(io.StringIO(content))
            header = next(reader)
            
            # Find Shenzhen column index
            if '深圳' in header:
                sz_idx = header.index('深圳')
            else:
                failed_dates.append((date_str, "No Shenzhen column"))
                current_date += timedelta(days=1)
                day_count += 1
                continue
            
            for row in reader:
                if len(row) > sz_idx and row[sz_idx]:
                    all_rows.append({
                        'date': row[0],
                        'hour': row[1],
                        'type': row[2],
                        'value': row[sz_idx]
                    })
    except Exception as e:
        failed_dates.append((date_str, str(e)))
    
    day_count += 1
    if day_count % 100 == 0:
        print(f"  Progress: {day_count}/{total_days} days downloaded...")
    
    current_date += timedelta(days=1)

print(f"\nDownload complete! Total rows: {len(all_rows)}")
print(f"Failed dates: {len(failed_dates)}")
if failed_dates[:5]:
    print(f"  First few failures: {failed_dates[:5]}")

# Pivot the data: one row per (date, hour) with columns for each pollutant type
from collections import defaultdict

pivoted = defaultdict(dict)
types_seen = set()

for row in all_rows:
    key = (row['date'], row['hour'])
    pivoted[key][row['type']] = row['value']
    types_seen.add(row['type'])

print(f"\nData types found: {sorted(types_seen)}")

# Write to CSV - use daily averages (24h values) for simplicity
# Types we want: AQI, PM2.5, PM2.5_24h, PM10, PM10_24h, SO2, NO2, O3, CO
desired_types = ['AQI', 'PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'O3_8h', 'CO']

output_file = os.path.join(OUTPUT_DIR, "shenzhen_air_quality_2019_2024.csv")
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'hour'] + desired_types)
    
    for (date, hour) in sorted(pivoted.keys()):
        row_data = pivoted[(date, hour)]
        values = [row_data.get(t, '') for t in desired_types]
        writer.writerow([date, hour] + values)

print(f"\nSaved to: {output_file}")

# Also create a daily average file
daily_data = defaultdict(lambda: defaultdict(list))
for (date, hour), row_data in pivoted.items():
    for t in desired_types:
        if t in row_data and row_data[t]:
            try:
                daily_data[date][t].append(float(row_data[t]))
            except ValueError:
                pass

daily_output = os.path.join(OUTPUT_DIR, "shenzhen_daily_avg_2019_2024.csv")
with open(daily_output, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date'] + [f'{t}_avg' for t in desired_types])
    
    for date in sorted(daily_data.keys()):
        avgs = []
        for t in desired_types:
            vals = daily_data[date].get(t, [])
            if vals:
                avgs.append(f"{sum(vals)/len(vals):.1f}")
            else:
                avgs.append('')
        writer.writerow([date] + avgs)

print(f"Daily averages saved to: {daily_output}")

# Quick stats
import statistics
dates = sorted(daily_data.keys())
print(f"\nDate range: {dates[0]} to {dates[-1]}")
print(f"Total days with data: {len(dates)}")

for t in ['PM2.5', 'AQI', 'NO2', 'O3']:
    all_vals = []
    for d in dates:
        all_vals.extend(daily_data[d].get(t, []))
    if all_vals:
        print(f"  {t}: mean={statistics.mean(all_vals):.1f}, median={statistics.median(all_vals):.1f}, min={min(all_vals):.0f}, max={max(all_vals):.0f}")
