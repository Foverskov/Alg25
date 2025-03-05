import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the CSV data
data = pd.read_csv('out.csv')

# Create separate tables for each list type
list_types = data['listtype'].unique()

for list_type in list_types:
    # Filter data for this list type
    type_data = data[data['listtype'] == list_type]
    
    # Convert to a more usable format: pivot the data
    pivot_data = type_data.pivot_table(index='size', columns='sorttype', values='time', aggfunc='mean').reset_index()
    
    # Format the data for display
    table_data = pivot_data.copy()
    # Format time values to 4 decimal places
    for col in table_data.columns:
        if col != 'size':
            table_data[col] = table_data[col].map(lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A")
    
    # Create a figure with appropriate size
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table
    table = ax.table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        cellLoc='center',
        loc='center',
        colColours=['#f2f2f2'] * len(table_data.columns)
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    # Add a title
    plt.title(f'Sorting Algorithm Performance - {list_type.capitalize()} Lists (Time in seconds)', fontsize=16, pad=20)
    
    # Save the table
    plt.tight_layout()
    plt.savefig(f'sorting_performance_{list_type}_table.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a figure with 3 subplots (one for each list type)
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

for i, list_type in enumerate(list_types):
    # Filter data for this list type
    type_data = data[data['listtype'] == list_type]
    
    # Convert to a more usable format: pivot the data
    pivot_data = type_data.pivot_table(index='size', columns='sorttype', values='time', aggfunc='mean')
    
    # Plot the data
    for algorithm in pivot_data.columns:
        axes[i].plot(pivot_data.index, pivot_data[algorithm], marker='o', linewidth=2, label=algorithm)
    
    # Set logarithmic scales for better visualization
    axes[i].set_xscale('log')
    axes[i].set_yscale('log')
    
    # Add title and labels
    axes[i].set_title(f'{list_type.capitalize()} Lists', fontsize=14)
    axes[i].set_xlabel('Array Size (n)', fontsize=12)
    axes[i].set_ylabel('Execution Time (seconds)', fontsize=12)
    axes[i].grid(True, which="both", ls="--", alpha=0.7)
    
    # Add legend
    axes[i].legend(fontsize=12)

plt.tight_layout()
plt.savefig('sorting_performance_all_types.png', dpi=300)
plt.close()

# Also create a summary table comparing all list types
# Create a multi-level summary table
summary_data = []

# Define size categories
size_categories = [
    ('Small', data[data['size'] == 1000]),
    ('Medium', data[(data['size'] >= 10000) & (data['size'] <= 50000)]),
    ('Large', data[data['size'] >= 100000])
]

# Build the summary dataframe
summary_rows = []
for size_name, size_data in size_categories:
    for list_type in list_types:
        type_data = size_data[size_data['listtype'] == list_type]
        for sort_type in ['Insertion', 'Merge', 'Quick']:
            if sort_type in type_data['sorttype'].values:
                avg_time = type_data[type_data['sorttype'] == sort_type]['time'].mean()
                summary_rows.append({
                    'Size Category': size_name,
                    'List Type': list_type.capitalize(),
                    'Sort Algorithm': sort_type,
                    'Average Time': avg_time,  # Keep as numeric
                    'Average Time (s)': f"{avg_time:.4f}" if pd.notnull(avg_time) else "N/A"  # Formatted version
                })

summary_df = pd.DataFrame(summary_rows)

# Create a prettier summary table
plt.figure(figsize=(14, 10))
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Create the table - using a more structured format but with the formatted column
table_data = summary_df.pivot_table(
    index=['Size Category', 'List Type'],
    columns='Sort Algorithm',
    values='Average Time',  # Use the numeric column for pivoting
    aggfunc='mean'
).reset_index()

# Format the numeric values after pivoting
for col in table_data.columns:
    if col not in ['Size Category', 'List Type']:
        table_data[col] = table_data[col].map(lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A")

# Flatten the multi-index for display
flat_index = []
for row in table_data.itertuples(index=False):
    if len(flat_index) > 0 and row[0] == flat_index[-1][0]:  # Same size category
        flat_index.append(('', row[1]))  # Empty string for size category
    else:
        flat_index.append((row[0], row[1]))  # Both size and list type

cell_text = table_data.iloc[:, 2:].values
col_labels = table_data.columns[2:]
row_labels = [f"{size} - {list_type}" for size, list_type in flat_index]

# Create the table
summary_table = plt.table(
    cellText=cell_text,
    rowLabels=row_labels,
    colLabels=col_labels,
    loc='center',
    cellLoc='center',
    colWidths=[0.2] * len(col_labels)
)

# Style the table
summary_table.auto_set_font_size(False)
summary_table.set_fontsize(12)
summary_table.scale(1.5, 1.5)

plt.title('Sorting Algorithm Performance by List Type and Size Category', fontsize=16, y=0.9)
plt.tight_layout()
plt.savefig('sorting_performance_by_type_summary.png', dpi=300, bbox_inches='tight')
plt.close()

print("All visualizations have been created successfully!")