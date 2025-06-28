import os
import pandas as pd
import re
from datetime import datetime

folder = 'csv_files'
output_file = 'comparison_output.txt'

# Get all CSV files with date in filename
files = []
for f in os.listdir(folder):
    match = re.search(r'_(\d{8})\.csv$', f)
    if match:
        date = datetime.strptime(match.group(1), '%Y%m%d')
        files.append((f, date))

files.sort(key=lambda x: x[1])

if len(files) >= 2:
    old_file = os.path.join(folder, files[-2][0])
    new_file = os.path.join(folder, files[-1][0])

    df_old = pd.read_csv(old_file)
    df_new = pd.read_csv(new_file)

    with open(output_file, 'w') as out:
        out.write(f"Comparing {files[-2][0]} with {files[-1][0]}\n")
        changes_found = False

        for i in range(max(len(df_old), len(df_new))):
            for j in range(max(len(df_old.columns), len(df_new.columns))):
                val_old = df_old.iloc[i, j] if i < len(df_old) and j < len(df_old.columns) else None
                val_new = df_new.iloc[i, j] if i < len(df_new) and j < len(df_new.columns) else None
                if val_old != val_new:
                    out.write(f"Row {i+1}, Column {j+1}: '{val_old}' -> '{val_new}'\n")
                    changes_found = True

        if not changes_found:
            out.write("No changes detected.\n")
else:
    with open(output_file, 'w') as out:
        out.write("Not enough files to compare.\n")
