
import pandas as pd

clean = True
if clean:
    # Load the Excel file
    df = pd.read_excel('sample-survey-data.xlsx')

    # Select only columns A and C by their labels or index (if A and C are, for example, 'Column1' and 'Column3')
    df_filtered = df[['unique', 'question', 'country', 'gender', 'age_group', 'educ_level', 'Pol_Self_placement',
                      'profile_gross_household_EU', 'probability', 'social_', 'true', 'headline']]

    # Save the filtered data to a new Excel file
    df_filtered.to_excel('test.xlsx', index=False)

    print("Filtered Excel file saved successfully!")
else:
    # df = pd.read_stata("Excel-Sheets/survey-data.dta")
    df = pd.read_excel("Excel-Sheets/survey-data.xlsx")
    new_df = df.iloc[:100, :]

    new_df.to_excel("sample-survey-data.xlsx")
