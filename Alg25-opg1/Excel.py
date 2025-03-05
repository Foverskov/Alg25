import pandas as pd
import os

# Define the paths
csv_file = 'out.csv'
excel_output = 'sorting_results.xlsx'

# Read the CSV data
data = pd.read_csv(csv_file)

# Create an Excel writer
with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
    # Write the full data to sheet1
    data.to_excel(writer, sheet_name='Raw Data', index=False)
    
    # Create a pivot table for each list type
    for list_type in data['listtype'].unique():
        # Filter data for this list type
        type_data = data[data['listtype'] == list_type]
        
        # Create a pivot table
        pivot_table = type_data.pivot_table(
            index='size',
            columns='sorttype', 
            values='time',
            aggfunc='mean'
        ).reset_index()
        
        # Format the sheet name (capitalize and remove spaces)
        sheet_name = list_type.capitalize().replace(' ', '_')
        
        # Write to Excel with the list type as sheet name
        pivot_table.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Create a summary sheet
    summary = data.groupby(['listtype', 'sorttype'])['time'].mean().unstack()
    summary.to_excel(writer, sheet_name='Summary')
    
    # Add some formatting
    workbook = writer.book
    
    # Format for numbers (4 decimal places)
    number_format = workbook.add_format({'num_format': '0.0000'})
    
    # Apply formatting to each sheet
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        
        # Auto-adjust column width
        for col_num, col in enumerate(data.columns):
            max_width = max(data[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(col_num, col_num, max_width)
        
        # Set number format for time columns
        if sheet_name != 'Summary':
            for col_num in range(2, len(data.columns)):
                worksheet.set_column(col_num, col_num, None, number_format)

print(f"Excel file has been created: {os.path.abspath(excel_output)}")