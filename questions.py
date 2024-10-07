import pandas as pd

def extract_questions(filename):
    questions_df = pd.read_excel(filename)
    return questions_df[['headline']]


def new_seed(index):
    print(index)
    return index
