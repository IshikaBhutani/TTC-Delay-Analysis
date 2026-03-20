import pandas as pd
import os

os.makedirs("data/clean", exist_ok=True)

def clean_bus(filepath, year):
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['hour'] = pd.to_datetime(df['time'].astype(str), format='%H:%M', errors='coerce').dt.hour
    df = df[(df['min_delay'] > 0) & (df['min_delay'] < 300)]  # remove zeros & outliers
    df = df.dropna(subset=['route', 'incident', 'min_delay'])
    df['transit_type'] = 'Bus'
    df['year'] = year
    return df

bus = pd.concat([
    clean_bus("data/raw/ttc-bus-delay-data-2023.xlsx", 2023),
    clean_bus("data/raw/ttc-bus-delay-data-2024.xlsx", 2024)
], ignore_index=True)

bus.to_csv("data/clean/bus_clean.csv", index=False)
print(f"Bus rows after cleaning: {len(bus)}")


# ── SUBWAY ────────────────────────────────────────────────────────────────────
def clean_subway(filepath, year):
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['hour'] = pd.to_datetime(df['time'].astype(str), format='%H:%M', errors='coerce').dt.hour
    df = df[(df['min_delay'] > 0) & (df['min_delay'] < 300)]
    df = df.dropna(subset=['station', 'min_delay'])
    df.rename(columns={'station': 'location', 'line': 'route', 'code': 'incident'}, inplace=True)
    df['transit_type'] = 'Subway'
    df['year'] = year
    return df

subway = pd.concat([
    clean_subway("data/raw/ttc-subway-delay-data-2023.xlsx", 2023),
    clean_subway("data/raw/ttc-subway-delay-data-2024.xlsx", 2024)
], ignore_index=True)

subway.to_csv("data/clean/subway_clean.csv", index=False)
print(f"Subway rows after cleaning: {len(subway)}")

# ── STREETCAR ─────────────────────────────────────────────────────────────────
def clean_streetcar(filepath, year):
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['hour'] = pd.to_datetime(df['time'].astype(str), format='%H:%M', errors='coerce').dt.hour
    df = df[(df['min_delay'] > 0) & (df['min_delay'] < 300)]
    df = df.dropna(subset=['line', 'incident', 'min_delay'])
    df.rename(columns={'line': 'route'}, inplace=True)
    df['transit_type'] = 'Streetcar'
    df['year'] = year
    return df

streetcar = pd.concat([
    clean_streetcar("data/raw/ttc-streetcar-delay-data-2023.xlsx", 2023),
    clean_streetcar("data/raw/ttc-streetcar-delay-data-2024.xlsx", 2024)
], ignore_index=True)

streetcar.to_csv("data/clean/streetcar_clean.csv", index=False)
print(f"Streetcar rows after cleaning: {len(streetcar)}")


# ── COMBINED MASTER FILE ──────────────────────────────────────────────────────
master = pd.concat([bus, subway, streetcar], ignore_index=True)
master.to_csv("data/clean/ttc_all_clean.csv", index=False)
print(f"\nTotal master rows: {len(master)}")
print("Done! Files saved to data/clean/")