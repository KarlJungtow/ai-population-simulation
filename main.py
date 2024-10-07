from openai import OpenAI
from people import *
from questions import *

# Initialize OpenAI client
client = OpenAI()

# --------------------------------------------------------------------------------------------------
debug = 1

# Change constants here | If num_persons = 0, existing persons_sample.xlsx will be used
num_persons = 0
num_questions = 1

# When set to true, the text will be parsed and only the desired output will be saved to the Excel
# When set to false, the complete answers will be saved
text_parsing_active = True
# ---------------------------------------------------------------------------------------------------

# Read the personas and questions from Excel files
questions_df = extract_questions("Excel-Sheets/test.xlsx")
persons_df, num_persons = extract_sample("Excel-Sheets/survey-data.xlsx", num_persons)

if debug == 0:

    # List of sub-questions to answer
    to_answer = [
        "From your perspective: How likely is it, that this headline is true? "
        "Answer with a percentage and give your reasoning.",

        "How likely would it be for you to share this headline on social media? "
        "Answer with either yes, no, don't known and give your reasoning.",

        "Assume this headline is true. Which party would benefit from it? "
        "Answer with a number on a scale from 0 for left-wing parties to 10 for right-wing parties and explain why."
    ]

    # List to store results
    results = []

    steps = num_persons * num_questions * 100
    for i in range(0, num_persons):
        # Extract person details
        gender = persons_df.iloc[i, 0]
        if gender == "Not female":
            gender = "male"
        salary = int(persons_df.iloc[i, 1])
        age_bracket = randomize_age(persons_df.iloc[i, 2])
        yoe = persons_df.iloc[i, 3]
        country = persons_df.iloc[i, 4]
        pol_self_placement = persons_df.iloc[i, 5]

        # Create a persona description for the OpenAI prompt
        person = (
            f"Always answer as if you were this person: "
            f"You are a {gender} person from {country}. You are in the age bracket of {age_bracket}. "
            f"Your income ranks {salary} on a scale from one (low income) to ten (very high income). "
            f"In total, your education ranks {yoe} on a scale from one (very low) to ten (very high). "
            f"On a scale from one (far-left) to ten (far-right), you place yourself on a {pol_self_placement} "
            f"regarding your political self placement. "
            f"You take part in a scientific study that examines fake news. You will read a headline and have to "
            f"answer certain questions regarding that headline."
        )

        # Iterate over each question in the questions DataFrame

        for k in range(num_questions):
            seed_index = i * num_questions + k # Index for Progress and seed generation
            percent = seed_index / steps
            print("Progress: " + str(round(percent, 2)) + " %")

            question = str(questions_df.iloc[i * 20 + k, 0])
            responses = []

            index = 0
            # Iterate over each sub-question and get the response from OpenAI
            for sub_question in to_answer:
                new_question = question + sub_question
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": person},
                        {"role": "user", "content": new_question}
                    ],
                    seed=new_seed(seed_index)
                )
                response_text = str(completion.choices[0].message.content)
                responses.append(clean_answers(response_text.replace('\\n', '\n'), index, text_parsing_active))
                index += 1
            # Append the results to the list
            results.append({
                "PersonID": i + 201,
                "Gender": gender,
                "Salary": salary,
                "Age": age_bracket,
                "Years of education": yoe,
                "Country": country,
                "Pol_self_placement": pol_self_placement,
                "Question": question,
                "True/False?": responses[0],
                "Sharing": responses[1],
                "Beneficial": responses[2],
            })

    print("Progress: 100%")
    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results)

    survey_df = pd.read_excel("Excel-Sheets/test.xlsx")
    #df_new_offset = pd.concat([pd.DataFrame([np.nan]), results_df], ignore_index=True)
    combined_df = pd.concat([survey_df, results_df], axis=1)
    # Write the results DataFrame to an Excel file
    combined_df.to_excel('Excel-Sheets/responses_test.xlsx', index=False)
