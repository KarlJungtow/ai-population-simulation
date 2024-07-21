import pandas as pd
import openai
import random

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
            model="gpt-4-turbo",
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
        seed = random.randint(0, 1000000)
        person = generate_person(seed)
        persons.append(person)

    # Convert the list of persons to a DataFrame
    # Parsing each line of generated CSV format data into a list
    data = [p.split(',') for p in persons]
    headers = ['Gender', 'Salary', 'Age', 'Years of Education', 'Country']
    persons_df = pd.DataFrame(data, columns=headers)

    # Save the DataFrame to an Excel file
    persons_df.to_excel('Excel-Sheets/persons_sample.xlsx', index=False)
