import json
import pandas as pd

# Load the JSON data
with open('profit.json') as f:
  data = json.load(f)

# Define a dictionary to map month numbers to Polish month names
month_names = {
  1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec',
  7: 'Lipiec', 8: 'Sierpień', 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
}

# Initialize an empty DataFrame
df = pd.DataFrame()

# Iterate over each set in the 'stats_data' list
for stats in data['stats_data']:
  # Replace month numbers with Polish month names
  months = [month_names[month] for month in stats['months']]

  # Replace dots with commas in numbers
  data_values = [str(num).replace('.', ',') for num in stats['data']]

  # Create a DataFrame from the 'months' and 'data' lists
  temp_df = pd.DataFrame({
    f"{stats['name']}_months": months,
    f"{stats['name']}_data": data_values
  })

  # If df is empty, copy temp_df to df
  if df.empty:
    df = temp_df
  else:
    # Otherwise, merge df and temp_df on the months column
    df = pd.merge(df, temp_df, left_on=f"{data['stats_data'][0]['name']}_months", right_on=f"{stats['name']}_months")

# Drop duplicate month columns
df = df.loc[:,~df.columns.duplicated()]

# Write the DataFrame to a CSV file
df.to_csv("output.csv", index=False)