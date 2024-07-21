import pandas as pd
from openai import OpenAI
from people import generate_person_excel

# Initialize OpenAI client
client = OpenAI()

# Read the personas and questions from Excel files
persons_df = pd.read_excel('Excel-Sheets/persons_sample.xlsx')
questions_df = pd.read_excel('Excel-Sheets/questions.xlsx')


#--------------------------------------------------------------------------------------------------
#Change constants here
num_persons = 0
num_questions = 1

# l/u = lower bound, then upper bound
# attributes must follow the order of Salary (l/u), Age (l/u), Years of Education (l/u), Country
attributes = ["10000", "20000", "20", "40", "8", "16", "Germany"]
#---------------------------------------------------------------------------------------------------


generate_person_excel(num_persons, attributes)

# List of sub-questions to answer
to_answer = [
    " Question: From your perspective: How likely is it, that this headline is true? Answer with a percentage, nothing else.",
    " Question: How likely would it be for you to share this headline on social media? Answer with either yes, no, don't know",
    " Question: Assume this headline is true. Which party would benefit from it? Answer with only a number on a scale from 0 for left-wing parties to 10 for right-wing parties"
]

# List to store results
results = []

# Iterate over each person in the DataFrame
if num_persons == 0:
    num_persons = persons_df.shape[0]
for i in range(num_persons):
    # Extract person details
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


    for k in range(1, num_questions+1):
        percent = (i * num_questions + k) / (num_persons * num_questions) * 100
        print(str(round(percent, 2)) + " %")

        if round(percent, 2) == 20.0:
            print("20!")

        question = str(questions_df.iloc[k, 1])
        responses = []

        # Iterate over each sub-question and get the response from OpenAI
        for sub_question in to_answer:
            new_question = question + sub_question
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": person},
                    {"role": "user", "content": new_question}
                ]
            )
            response_text = str(completion.choices[0].message.content)
            responses.append(response_text.replace('\\n', '\n'))
        # Append the results to the list
        results.append({
            "PersonID": i+1,
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

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Write the results DataFrame to an Excel file
results_df.to_excel('Excel-Sheets/responses_test.xlsx', index=False)

