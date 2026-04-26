import pandas as pd

# reads tables into dataframes
filepath_A = '.\data set\Data - Table A.csv'
bacteria_df = pd.read_csv(filepath_A)
bacteria_df = bacteria_df.replace({'Yes': 1, 'No': 0}) # convert to 0/1 for multiplcation process after
filepath_B = '.\data set\Data - Table B.csv'
antibiotic_df = pd.read_csv(filepath_B)

# Pairs bacteria rows with antibiotic rows
supertable = bacteria_df.merge(antibiotic_df, how='cross')

# Stores all mechanisms listed in bacteria_df
mechanisms = bacteria_df.columns[1:]

# Creates columns and sets them to zero
supertable['Total Vulnerability'] = 0
supertable['Resistance'] = 0

mechanism_factors = {}

# Iterating over each row in the supertable to add resistance values
for index, row in supertable.iterrows():
    total_sum = 0
    
    for mechanism in mechanisms:
        # calculating individual mechanism factors
        mechanism_factors[mechanism] = row[mechanism + '_x'] * row[mechanism + '_y']
        supertable.at[index, mechanism + " factor"] = mechanism_factors[mechanism]

        # Used for calculating total resistance
        total_sum += row[mechanism + '_y']

    total_vulnerability = sum(mechanism_factors.values())

    # Stores it into a column
    supertable.at[index, 'Total Vulnerability'] = round(total_vulnerability, 1)
    supertable.at[index, 'Resistance'] = round(total_vulnerability / len(mechanisms), 2)

    # Rounding the values
    supertable['Total Vulnerability'] = supertable['Total Vulnerability'].round(1)
    supertable['Resistance'] = supertable['Resistance'].round(2)

    # Reset values for next iteration
    mechanism_factors.clear()
    
# Stores it to output.csv for the website to access
supertable.to_csv('.\website\data\output.csv')