import pandas as pd
import matplotlib.pyplot as plt
from convex_hull import compute_hull_dvcq

print("COVID-19 Convex Hull Analysis")
print("=" * 60)

# Read the CSV file
df = pd.read_csv('Covid_19_Countrywise_timeseries.csv')
print(f"Loaded {len(df)} records from CSV")

# Clean the data - remove rows with missing values
df = df.dropna(subset=['Confirmed', 'Deaths', 'Recovered'])
print(f"After cleaning: {len(df)} records")


# Function to create point sets from two columns
def create_point_set(df, col_x, col_y, name, filter_zeros=True):
    """Create a list of (x, y) points from two DataFrame columns"""
    points = []
    for idx, row in df.iterrows():
        try:
            x = float(row[col_x])
            y = float(row[col_y])

            # Filter out negative or zero values if requested
            if filter_zeros and (x <= 0 and y <= 0):
                continue

            if x >= 0 and y >= 0:  # Keep only non-negative values
                points.append((x, y))
        except (ValueError, TypeError):
            continue

    print(f"\n{name}: {len(points)} points")
    return points


# Create three different datasets
print("\n" + "=" * 60)
print("CREATING DATASETS")
print("=" * 60)

datasets = [
    # Dataset 1: Total Confirmed Cases vs Deaths
    ("Confirmed Cases vs Deaths",
     create_point_set(df, 'Confirmed', 'Deaths', "Dataset 1"),
     'Confirmed Cases', 'Deaths'),

    # Dataset 2: Total Confirmed Cases vs Recovered
    ("Confirmed Cases vs Recovered",
     create_point_set(df, 'Confirmed', 'Recovered', "Dataset 2"),
     'Confirmed Cases', 'Recovered'),

    # Dataset 3: Deaths vs Recovered
    ("Deaths vs Recovered",
     create_point_set(df, 'Deaths', 'Recovered', "Dataset 3"),
     'Deaths', 'Recovered')
]

# Alternative datasets you could use instead:
# - ('New Confirmed', 'New Death') - Daily new cases vs daily deaths
# - ('New Confirmed', 'New Recovered') - Daily new cases vs recoveries
# - ('latitude', 'longitude') - Geographic distribution
# Just replace the datasets list above with these if you prefer

# Create plots
print("\n" + "=" * 60)
print("COMPUTING CONVEX HULLS")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Convex Hull Analysis of COVID-19 Data', fontsize=16, fontweight='bold')

for idx, (title, points, xlabel, ylabel) in enumerate(datasets):
    ax = axes[idx]

    if len(points) < 3:
        ax.text(0.5, 0.5, f'Insufficient data\n({len(points)} points)',
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        continue

    print(f"\n{title}:")
    print(f"  Total points: {len(points)}")

    # Compute convex hull
    hull_points = compute_hull_dvcq(points)
    print(f"  Hull vertices: {len(hull_points)}")
    print(f"  Reduction: {(1 - len(hull_points) / len(points)) * 100:.1f}%")

    # Extract coordinates
    x_coords, y_coords = zip(*points)
    hull_x, hull_y = zip(*hull_points)

    # Close the hull polygon for plotting
    hull_x = list(hull_x) + [hull_x[0]]
    hull_y = list(hull_y) + [hull_y[0]]

    # Plot all points (smaller, semi-transparent)
    ax.scatter(x_coords, y_coords, c='skyblue', s=30, alpha=0.4,
               edgecolors='navy', linewidth=0.3, label=f'All data (n={len(points)})')

    # Plot hull vertices (larger, prominent)
    ax.scatter(hull_x[:-1], hull_y[:-1], c='red', s=120, marker='o',
               edgecolors='darkred', linewidth=2,
               label=f'Hull vertices (h={len(hull_points)})', zorder=5)

    # Draw hull polygon
    ax.plot(hull_x, hull_y, 'r-', linewidth=2.5, alpha=0.8, label='Convex hull', zorder=4)
    ax.fill(hull_x, hull_y, 'red', alpha=0.08, zorder=3)

    # Formatting
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(f'{title}\n({len(hull_points)} of {len(points)} points on hull)',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Format large numbers with commas
    ax.ticklabel_format(style='plain', axis='both')

    # Add some statistics as text
    stats_text = f'Hull ratio: {len(hull_points) / len(points) * 100:.1f}%'
    ax.text(0.98, 0.02, stats_text, transform=ax.transAxes,
            fontsize=9, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('covid_convex_hulls.png', dpi=300, bbox_inches='tight')
print("\n✓ Plot saved as 'covid_convex_hulls.png'")
plt.show()

# Print detailed summary
print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
print(f"\n{'Dataset':<30} {'Total':<8} {'Hull':<8} {'Ratio':<10} {'Reduction':<10}")
print("-" * 70)

for title, points, _, _ in datasets:
    if len(points) >= 3:
        hull = compute_hull_dvcq(points)
        ratio = len(hull) / len(points) * 100
        reduction = (1 - len(hull) / len(points)) * 100
        print(f"{title:<30} {len(points):<8} {len(hull):<8} {ratio:<9.1f}% {reduction:<9.1f}%")

# Additional analysis - find the most extreme points
print("\n" + "=" * 60)
print("EXTREME POINTS ANALYSIS")
print("=" * 60)

# Get the first dataset for detailed analysis
title, points, xlabel, ylabel = datasets[0]
if len(points) >= 3:
    hull = compute_hull_dvcq(points)

    # Find the extreme points
    max_x = max(hull, key=lambda p: p[0])
    max_y = max(hull, key=lambda p: p[1])
    min_x = min(hull, key=lambda p: p[0])
    min_y = min(hull, key=lambda p: p[1])

    print(f"\nFor '{title}':")
    print(f"  Highest {xlabel}: {max_x[0]:,.0f} (with {max_x[1]:,.0f} {ylabel})")
    print(f"  Highest {ylabel}: {max_y[1]:,.0f} (with {max_y[0]:,.0f} {xlabel})")
    print(f"  Lowest {xlabel}: {min_x[0]:,.0f} (with {min_x[1]:,.0f} {ylabel})")
    print(f"  Lowest {ylabel}: {min_y[1]:,.0f} (with {min_y[0]:,.0f} {xlabel})")

print("\n" + "=" * 60)
print("Analysis complete!")
print("=" * 60)