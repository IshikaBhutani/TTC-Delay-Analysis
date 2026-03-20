import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

os.makedirs("outputs/charts", exist_ok=True)

df = pd.read_csv("data/clean/ttc_all_clean.csv")
# Fix ordering
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

# ── 1. TOP 10 ROUTES BY DELAY FREQUENCY (Bus only) ───────────────────────────
bus = df[df['transit_type'] == 'Bus']
top_routes = (bus.groupby('route')['min_delay']
                 .count()
                 .sort_values(ascending=False)
                 .head(10)
                 .reset_index())
top_routes.columns = ['route', 'delay_count']

plt.figure(figsize=(10, 5))
plt.bar(top_routes['route'].astype(str), top_routes['delay_count'], color='#c0392b')
plt.title('Top 10 Bus Routes by Delay Frequency (2023–2024)', fontsize=14)
plt.xlabel('Route Number')
plt.ylabel('Number of Delays')
plt.tight_layout()
plt.savefig('outputs/charts/01_top_routes.png', dpi=150)
plt.close()
print("Chart 1 done")

# ── 2. DELAYS BY HOUR OF DAY ──────────────────────────────────────────────────
hourly = (df.groupby('hour')['min_delay']
            .count()
            .reset_index())
hourly.columns = ['hour', 'delay_count']

plt.figure(figsize=(10, 5))
plt.plot(hourly['hour'], hourly['delay_count'], marker='o', color='#2980b9', linewidth=2)
plt.fill_between(hourly['hour'], hourly['delay_count'], alpha=0.2, color='#2980b9')
plt.title('Delays by Hour of Day – All Transit Types (2023–2024)', fontsize=14)
plt.xlabel('Hour of Day (0 = midnight)')
plt.ylabel('Number of Delays')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig('outputs/charts/02_delays_by_hour.png', dpi=150)
plt.close()
print("Chart 2 done")

# ── 3. DELAYS BY DAY OF WEEK ──────────────────────────────────────────────────
daily = (df.groupby('day_of_week')['min_delay']
           .count()
           .reindex(day_order)
           .reset_index())
daily.columns = ['day', 'delay_count']

plt.figure(figsize=(10, 5))
plt.bar(daily['day'], daily['delay_count'], color='#8e44ad')
plt.title('Delays by Day of Week – All Transit Types (2023–2024)', fontsize=14)
plt.xlabel('Day')
plt.ylabel('Number of Delays')
plt.tight_layout()
plt.savefig('outputs/charts/03_delays_by_day.png', dpi=150)
plt.close()
print("Chart 3 done")

# ── 4. TOP DELAY CAUSES ───────────────────────────────────────────────────────
causes = (df[df['transit_type'] != 'Subway']   # subway uses codes not plain text
            .groupby('incident')['min_delay']
            .count()
            .sort_values(ascending=False)
            .head(10)
            .reset_index())
causes.columns = ['incident', 'count']

plt.figure(figsize=(10, 5))
plt.barh(causes['incident'][::-1], causes['count'][::-1], color='#27ae60')
plt.title('Top 10 Delay Causes – Bus & Streetcar (2023–2024)', fontsize=14)
plt.xlabel('Number of Delays')
plt.tight_layout()
plt.savefig('outputs/charts/04_delay_causes.png', dpi=150)
plt.close()
print("Chart 4 done")

# ── 5. MONTHLY TREND ──────────────────────────────────────────────────────────
monthly = (df.groupby(['year', 'month'])['min_delay']
             .count()
             .reset_index())
monthly.columns = ['year', 'month', 'delay_count']
monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
monthly = monthly.sort_values(['year', 'month'])

plt.figure(figsize=(12, 5))
for yr, grp in monthly.groupby('year'):
    plt.plot(grp['month'], grp['delay_count'], marker='o', label=str(yr), linewidth=2)
plt.title('Monthly Delay Trend – 2023 vs 2024', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Delays')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('outputs/charts/05_monthly_trend.png', dpi=150)
plt.close()
print("Chart 5 done")

# ── 6. DELAYS BY TRANSIT TYPE ─────────────────────────────────────────────────
by_type = (df.groupby('transit_type')['min_delay']
             .agg(['count', 'mean'])
             .reset_index())
by_type.columns = ['transit_type', 'total_delays', 'avg_delay_min']

plt.figure(figsize=(7, 5))
plt.bar(by_type['transit_type'], by_type['total_delays'],
        color=['#e74c3c','#3498db','#f39c12'])
plt.title('Total Delays by Transit Type (2023–2024)', fontsize=14)
plt.ylabel('Number of Delays')
plt.tight_layout()
plt.savefig('outputs/charts/06_by_transit_type.png', dpi=150)
plt.close()
print("Chart 6 done")

# ── PRINT KEY STATS FOR YOUR README ──────────────────────────────────────────
print("\n========= KEY FINDINGS =========")
print(f"Total delay records: {len(df):,}")
print(f"\nTop 3 bus routes:\n{top_routes.head(3).to_string(index=False)}")
print(f"\nWorst hour: {hourly.loc[hourly['delay_count'].idxmax(), 'hour']}:00")
print(f"Worst day: {daily.loc[daily['delay_count'].idxmax(), 'day']}")
print(f"\nTop 3 causes:\n{causes.head(3).to_string(index=False)}")
print(f"\nAvg delay by type:\n{by_type[['transit_type','avg_delay_min']].to_string(index=False)}")