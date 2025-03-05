import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV data
data = pd.read_csv('out.csv')

# Convert to a more usable format: pivot the data
pivot_data = data.pivot_table(index='size', columns='type', values='time', aggfunc='mean')

# Create a figure with appropriate size
plt.figure(figsize=(12, 8))

# Plot the data
for algorithm in ['Insertion', 'Merge', 'Quick']:
    if algorithm in pivot_data.columns:
        plt.plot(pivot_data.index, pivot_data[algorithm], marker='o', linewidth=2, label=algorithm)

# Set logarithmic scales for better visualization
plt.xscale('log')
plt.yscale('log')

# Add title and labels
plt.title('Sorting Algorithm Performance Comparison', fontsize=16)
plt.xlabel('Array Size (n)', fontsize=14)
plt.ylabel('Execution Time (seconds)', fontsize=14)
plt.grid(True, which="both", ls="--", alpha=0.7)

# Add legend
plt.legend(fontsize=12)

# Annotate some key points
for algorithm in ['Merge', 'Quick']:
    if algorithm in pivot_data.columns:
        last_point = pivot_data[algorithm].iloc[-1]
        plt.annotate(f"{algorithm}: {last_point:.3f}s", 
                    xy=(pivot_data.index[-1], last_point),
                    xytext=(0, 10), textcoords='offset points',
                    ha='center')

# Add complexity reference lines
x = np.array(pivot_data.index)
plt.plot(x, 1e-7 * x * np.log(x), '--', alpha=0.5, color='gray', label='O(n log n)')
plt.plot(x, 1e-10 * x**2, '--', alpha=0.5, color='black', label='O(n²)')

plt.tight_layout()
plt.savefig('sorting_performance.png', dpi=300)
plt.show()