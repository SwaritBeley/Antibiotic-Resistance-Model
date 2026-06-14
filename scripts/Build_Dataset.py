import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



# reads tables into dataframes
filepath_A = BASE_DIR / 'data set' / 'Data - Table A.csv'
bacteria_df = pd.read_csv(filepath_A)
bacteria_df = bacteria_df.replace({'Yes': 1, 'No': 0}) # convert to 0/1 for multiplcation process after
filepath_B = BASE_DIR / 'data set' / 'Data - Table B.csv'
antibiotic_df = pd.read_csv(filepath_B)

# Pairs bacteria rows with antibiotic rows and makes the supertable
supertable = bacteria_df.merge(antibiotic_df, how='cross', suffixes=('_bact', '_abx'))

# Stores all mechanisms listed in bacteria_df
mechanisms = bacteria_df.columns[1:]

# Creates columns and sets them to zero
supertable['Total Vulnerability'] = 0
supertable['Resistance'] = 0

mechanism_factors = {}

# Iterating over each row in the supertable to add resistance values
for index, row in supertable.iterrows():
    
    for mechanism in mechanisms:
        # calculating individual mechanism factors
        mechanism_factors[mechanism] = row[mechanism + '_bact'] * row[mechanism + '_abx']
        supertable.at[index, mechanism + " factor"] = mechanism_factors[mechanism]

    total_vulnerability = sum(mechanism_factors.values())

    # Stores it into a column
    supertable.at[index, 'Total Vulnerability'] = round(total_vulnerability, 1)
    supertable.at[index, 'Resistance'] = round(total_vulnerability / len(mechanisms), 2)

    # Reset values for next iteration
    mechanism_factors.clear()
    
# Rounding the values
supertable['Total Vulnerability'] = supertable['Total Vulnerability'].round(1)
supertable['Resistance'] = supertable['Resistance'].round(2)

# Stores it to supertable.csv for the website to access
supertable.to_csv(BASE_DIR / 'data set' / 'supertable.csv', index=False)