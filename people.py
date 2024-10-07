import pandas as pd
import openai
import random
import re


# Extract peoples information from Stata data.
# var "num" specifies amount. If num is greater than total number of samples, it will stop after the last person
def extract_sample(filename, num):
    if num == 0:
        df = pd.read_excel("Excel-Sheets/persons_sample.xlsx")
        return df
    df = pd.read_excel(filename)

    # Get the unique identifiers from column A
    unique_identifiers = df['unique'].unique()

    # Create a list to store the first rows of each unique identifier
    first_rows = []

    amount = 0
    # Loop through each unique identifier
    for identifier in unique_identifiers:
        # Get the first row with the current unique identifier
        first_row = df[df['unique'] == identifier].iloc[0]

        # Append the first row to the list
        first_rows.append(first_row)
        amount += 1
        if amount >= num:
            break
    # Create a DataFrame from the first rows
    first_rows_df = pd.DataFrame(first_rows)

    first_rows_df = first_rows_df.loc[:, 'unique':'true']
    df_filtered = first_rows_df[['gender', 'profile_gross_household_EU', 'age_group', 'educ_level',
                                 'country', 'Pol_Self_placement']]

    # Return and save the DataFrame for later use
    df_filtered.to_excel("Excel-Sheets/persons_sample.xlsx", index=False)
    return df_filtered, amount

def randomize_age(age_bracket):
    return age_bracket
def clean_answers(text, index, active):
    if not active:
        return text

    if index == 0:
        # Search for the pattern in the text
        match = re.search(r'\d+', text)
        # Check if a match is found
        if match:
            # Return the matched percentage
            return str(match.group(0)) + "%"
        else:
            # Return an appropriate message if no percentage is found
            return text
    elif index == 1:
        text_lower = text.lower()
        if "don't know" in text_lower:
            return "don't know"
        elif "yes" in text_lower:
            return "yes"
        elif "no" in text_lower:
            return "no"
        else:
            return text

    elif index == 2:
        match = re.search(r'\d+', text)
        if match and int(match.group()) < 11:
            return match.group()
        else:
            return text
    else:
        return text


def generate_person_excel(num_persons, attributes):
    if num_persons == 0:
        return

    # Initialize OpenAI client with your API key
    client = openai.OpenAI()

    # Function to generate one person using OpenAI
    def generate_person(seed):
        prompt = (
            f"Generate one person with the following information:\n"
            f"Gender: Either male, female, non-binary\n"
            f"Salary per Year: A number between {attributes[0]} and {attributes[1]}\n"
            f"Age: A number between {attributes[2]} and {attributes[3]}\n"
            f"Years of Education: A realistic number between {attributes[4]} and {attributes[5]}\n"
            f"Country in which they currently reside: {attributes[6]}\n"
            f"Use the seed {seed} to ensure varied results.\n"
            f"Provide the output in CSV format with the following keys:\n"
            f"- Gender\n"
            f"- Salary\n"
            f"- Age\n"
            f"- Years of Education\n"
            f"- Country\n"
            f"Do not add the attribute name into your answer."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        person = response.choices[0].message.content
        return person.replace('\n', '').replace('"', '').replace("`", '').replace("csv", '').strip()

    # Initialize an empty list to store generated persons
    persons = []

    # Generate persons
    for i in range(num_persons):
        seed = random.randint(10000000, 99999999)
        person = generate_person(seed)
        persons.append(person)

    # Convert the list of persons to a DataFrame
    # Parsing each line of generated CSV format data into a list
    data = [p.split(',') for p in persons]
    headers = ['Gender', 'Salary', 'Age', 'Years of Education', 'Country']
    persons_df = pd.DataFrame(data, columns=headers)

    # Save the DataFrame to an Excel file
    persons_df.to_excel('Excel-Sheets/persons_sample.xlsx', index=False)