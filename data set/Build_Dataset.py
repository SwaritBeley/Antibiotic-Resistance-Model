import pandas as pd
filepath_A = 'Antibiotic-Resistance-Model\data set\Data - Table A.csv'
bacteria_df = pd.read_csv(filepath_A)
bacteria_df = bacteria_df.replace({'Yes': 1, 'No': 0})
filepath_B = 'Antibiotic-Resistance-Model\data set\Data - Table B.csv'
antibiotic_df = pd.read_csv(filepath_B)
#print(bacteria_df)
#print(antibiotic_df)

supertable = bacteria_df.merge(antibiotic_df, how='cross')

# # Drop all _y columns
# supertable = supertable.loc[:, ~supertable.columns.str.endswith('_y')]

supertable['cell_wall_factor'] = 0
supertable['efflux_pump_factor'] = 0
supertable['hydrolysis_factor'] = 0
supertable['porin_loss_factor'] = 0
supertable['porin_mutation_factor'] = 0
supertable['pbp_modification_factor'] = 0
supertable['ribosomal_methylation_factor'] = 0
supertable['biofilm_factor'] = 0


# # Rename all _x columns by removing the suffix
# supertable.columns = supertable.columns.str.replace('_x$', '', regex=True)
supertable['Total Vulnerability'] = 0
supertable['Resistance'] = 0



for index, row in supertable.iterrows():
    has_cell_wall = row['has cell wall_x'] * row['has cell wall_y']
    has_multidrug_efflux_pump = row['has multidrug efflux pump_x'] * row['has multidrug efflux pump_y']
    hydrolysis = row['performs hydrolysis'] * row['hydrolysis']
    porin_loss = row['porin loss_x'] * row['porin loss_y']
    porin_mutation = row['porin mutation_x'] * row['porin mutation_y']
    pbp_modification = row['PBP modification_x'] * row['PBP modification_y']
    ribosomal_methylation = row['ribosomal methylation_x'] * row['ribosomal methylation_y']
    biofilm_protection = row['biofilm protection_x'] * row['biofilm protection_y']

    supertable.at[index, 'cell wall factor'] = has_cell_wall
    supertable.at[index, 'multidrug efflux pump factor'] = has_multidrug_efflux_pump
    supertable.at[index, 'hydrolysis factor'] = hydrolysis
    supertable.at[index, 'porin loss factor'] = porin_loss
    supertable.at[index, 'porin mutation factor'] = porin_mutation
    supertable.at[index, 'PBP modification factor'] = pbp_modification
    supertable.at[index, 'ribosomal methylation factor'] = ribosomal_methylation
    supertable.at[index, 'biofilm protection factor'] = biofilm_protection

    total_vulnerability = (
        has_cell_wall
        + has_multidrug_efflux_pump
        + hydrolysis
        + porin_loss
        + porin_mutation
        + pbp_modification
        + ribosomal_methylation
        + biofilm_protection
    )
        
    total_sum = (
        row['has cell wall_y']
        + row['has multidrug efflux pump_y']
        + row['hydrolysis']
        + row['porin loss_y']
        + row['porin mutation_y']
        + row['PBP modification_y']
        + row['ribosomal methylation_y']
        + row['biofilm protection_y']
    )


    supertable.at[index, 'Total Vulnerability'] = total_vulnerability
    supertable.at[index, 'Resistance'] = total_vulnerability / total_sum
    
supertable['Total Vulnerability'] = supertable['Total Vulnerability'].round(1)
supertable['Resistance'] = supertable['Resistance'].round(2)

supertable.to_csv('Antibiotic-Resistance-Model\website\output.csv')