import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

def load_json_dates(filepath):
    print(f"Loading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    dates = []
    for item in data.get('data', []):
        d_str = item.get('PublicationDate')
        if d_str and d_str != "-":
            try:
                # Expecting YYYY-MM-DD
                dates.append(pd.to_datetime(d_str))
            except:
                pass
    return dates

def load_csv_dates(filepath):
    print(f"Loading {filepath}...")
    # The header is split across two lines in a tricky way.
    # We'll skip the first two lines and define column names manually based on our preview.
    cols = ["Title", "Link", "Author", "Tags", "PublicationDate"]
    try:
        df = pd.read_csv(filepath, skiprows=2, names=cols, encoding='utf-8')
        # Publication date in CSV looks like "28-Aug-2025"
        df['PublicationDate'] = pd.to_datetime(df['PublicationDate'], errors='coerce')
        return df['PublicationDate'].dropna().tolist()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def main():
    json_path = 'writeup.json'
    csv_path = 'writeups.csv'
    
    all_dates = []
    
    if os.path.exists(json_path):
        json_dates = load_json_dates(json_path)
        print(f"Loaded {len(json_dates)} records from JSON.")
        all_dates.extend(json_dates)
    
    if os.path.exists(csv_path):
        csv_dates = load_csv_dates(csv_path)
        print(f"Loaded {len(csv_dates)} records from CSV.")
        all_dates.extend(csv_dates)
    
    if not all_dates:
        print("No dates found to model.")
        return

    # Create a DataFrame for easy aggregation
    df = pd.DataFrame({'date': all_dates})
    df['count'] = 1
    
    # Sort and set index
    df = df.sort_values('date')
    df.set_index('date', inplace=True)
    
    # Resample by Month
    monthly_counts = df.resample('ME').count() # 'ME' for Month End
    
    # Plotting with Premium Aesthetics
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
    
    ax.fill_between(monthly_counts.index, monthly_counts['count'], color='#00d4ff', alpha=0.3)
    ax.plot(monthly_counts.index, monthly_counts['count'], color='#00d4ff', linewidth=2, marker='o', markersize=4, label='Writeups per Month')
    
    # Formatting
    ax.set_title('Security Writeup Volume Over Time', fontsize=20, pad=20, fontweight='bold', color='white')
    ax.set_xlabel('Timeline', fontsize=12, labelpad=15)
    ax.set_ylabel('Number of Writeups', fontsize=12, labelpad=15)
    
    # Grid and Spines
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Date formatting on X-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    plt.legend(frameon=False, fontsize=10)
    plt.tight_layout()
    
    output_file = 'writeup_trend.png'
    plt.savefig(output_file)
    print(f"Graph saved as {output_file}")
    
    # Save raw data as X,Y (Date, Count)
    data_file = 'writeup_data_xy.csv'
    monthly_counts.rename(columns={'count': 'y'}).to_csv(data_file, index_label='x')
    print(f"Data points saved as {data_file}")
    
    # Also show stats
    total = len(all_dates)
    start_date = monthly_counts.index.min().strftime('%Y-%m')
    end_date = monthly_counts.index.max().strftime('%Y-%m')
    print(f"Model Summary: {total} total writeups analyzed from {start_date} to {end_date}.")

if __name__ == "__main__":
    main()
