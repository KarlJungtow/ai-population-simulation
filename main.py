import pandas as pd
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Read the personas and questions from Excel files
persons_df = pd.read_excel('persons_sample.xlsx')
questions_df = pd.read_excel('questions.xlsx')

# Create a copy of the persons DataFrame and add a unique ID to each person
persons_details = persons_df.copy()
persons_details['PersonID'] = range(1, len(persons_df) + 1)

# List of sub-questions to answer
to_answer = [
    " Question: From your perspective: How likely is it, that this headline is true? Answer with a percentage, nothing else.",
    " Question: How likely would it be for you to share this headline on social media? Answer with either yes, no, don't know",
    " Question: Assume this headline is true. Which party would benefit from it? Answer with just a number on a scale from 0 for left-wing parties to 10 for right-wing parties"
]

# List to store results
results = []

# Iterate over each person in the DataFrame
num_persons = 3 #persons_df.shape[0]
for i in range(num_persons):
    percent = i / num_persons * 100
    print(str(round(percent, 2)) + " %")

    # Extract person details
    person_id = persons_details.iloc[i]['PersonID']
    gender = persons_df.iloc[i, 0]
    salary = persons_df.iloc[i, 1]
    age = persons_df.iloc[i, 2]
    yoe = persons_df.iloc[i, 3]
    country = persons_df.iloc[i, 4]

    # Create a persona description for the OpenAI prompt
    person = (
        f"Always answer as if you were this person: "
        f"You are a {gender} person from {country}. You are {age} years old "
        f"and earn a yearly salary of {salary} euros. In total, you received {yoe} years of education. "
        f"You take part in a scientific study that examines fake news. You will read a headline and have to "
        f"answer certain questions regarding that headline."
    )

    # Iterate over each question in the questions DataFrame
    num_questions = 1 #questions_df.shape[0]

    for k in range(num_questions):
        question = str(questions_df.iloc[k, 1])
        responses = []

        # Iterate over each sub-question and get the response from OpenAI
        for sub_question in to_answer:
            new_question = question + sub_question
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": person},
                    {"role": "user", "content": new_question}
                ]
            )
            response_text = str(completion.choices[0].message.content)
            responses.append(response_text.replace('\\n', '\n'))
        # Append the results to the list
        results.append({
            "PersonID": person_id,
            "Gender": gender,
            "Salary": salary,
            "Age": age,
            "Years of education": yoe,
            "Country": country,
            "Question": question,
            "True/False?": responses[0],
            "Sharing": responses[1],
            "Beneficial": responses[2],
        })

print("100.0 %")

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Write the results DataFrame to an Excel file
results_df.to_excel('responses_test.xlsx', index=False)
