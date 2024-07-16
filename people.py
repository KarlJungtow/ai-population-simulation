import pandas as pd
import openai
import random




def generate_person_excel(num_persons, attributes):
    # Initialize OpenAI client with your API key
    client = openai.OpenAI()
    # Function to generate one person using OpenAI
    def generate_person(seed):
        prompt = (
        f"Generate one person with the following information:"
        f"Salary per Year: A number between {attributes[0], attributes[1]}"
        f"Age: A number between {attributes[2]} and {attributes[3]}"
        f"Years of Education: A realistic number between {attributes[4]} and {attributes[5]}"
        f"Country in which they currently reside: {attributes[6]}"
        f"Use the seed {seed} to ensure varied results."
        f"""Provide the output in csv format with the following keys:
        - Gender
        - Salary
        - Age
        - Years of Education
        - Country
    
        Do not add the attribute name into your answer"""
    )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Please generate a person"}
            ]
        )

        person = str(response.choices[0].message.content)
        return person.replace('\\n', '\n').strip()


    # Initialize an empty list to store generated persons
    persons = []

    # Generate 100 persons
    for i in range(num_persons):
        seed = random.randint(0, 1000000)
        person = generate_person(seed)
        persons.append(person)

    # Convert the list of persons to a DataFrame
    # Parsing each line of generated CSV format data into a list
    data = [p.split(',') for p in persons]
    headers = ['Gender', 'Salary', 'Age', 'Years of Education', 'Country']
    persons_df = pd.DataFrame(data, columns=headers)

    # Save the DataFrame to an Excel file
    persons_df.to_excel('persons_sample.xlsx', index=False)

