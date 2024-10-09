import pandas as pd
import numpy as np
# from sklearn.metrics import euclidean_distances
from people import extract_sample

num_persons = 0
population_df, num_persons = extract_sample("Excel-Sheets/survey-data.xlsx", num_persons)

# Reverse mappings
gender_reverse_mapping = {1: 'Female', 2: 'Not female'}
country_reverse_mapping = {1: '[1] Germany', 2: '[2] Ireland', 3: '[3] Poland', 4: '[4] Spain'}
age_group_reverse_mapping = {1: '[1] 18-24', 2: '[2] 25-34', 3: '[3] 35-44', 4: '[4] 45-54', 5: '[5] +55'}


population_df['gender'] = population_df['gender'].map({'Female': 1, 'Not female': 2})
population_df['country'] = population_df['country'].map({'[1] Germany': 1, '[2] Ireland': 2, '[3] Poland': 3, '[4] Spain': 4})
population_df['age_group'] = population_df['age_group'].map({'[1] 18-24': 1, '[2] 25-34': 2, '[3] 35-44': 3, '[4] 45-54': 4, '[5] +55': 5})



# Step 2: Convert categorical data into numerical for comparison
population_encoded = pd.get_dummies(population_df)


print(population_encoded.mean(axis=0, skipna=True))
print(population_encoded.var(axis=0, skipna=True))


# Step 3: Calculate the mean and variance of the population
population_mean = population_df.mean()
population_variance = population_df.var()

# Step 4: Generate 1000 random samples of size 100
sample_size = 100
n_samples = 10000
best_sample_index = -1
lowest_total_squared_variance_deviation = float('inf')

# Sampling and finding the best representative sample
for i in range(n_samples):
    # Random sample from population
    sample_df = population_df.sample(n=sample_size, random_state=np.random.randint(0, 10000))

    # Calculate variance of the sample
    sample_variance = sample_df.var()

    # Calculate the squared deviation for each attribute and sum them
    squared_deviation = (sample_variance - population_variance) ** 2
    total_squared_deviation = squared_deviation.sum()

    # Track the sample with the lowest total squared variance deviation
    if total_squared_deviation < lowest_total_squared_variance_deviation:
        lowest_total_squared_variance_deviation = total_squared_deviation
        best_sample_index = i
        best_sample_df = sample_df

# Step 8: The best sample is stored in `best_sample_df`
print(f"Best sample index: {best_sample_index}")
print(best_sample_df.mean(axis=0, skipna=True))
print(best_sample_df.var(axis=0, skipna=True))

best_sample_df['gender'] = best_sample_df['gender'].replace(gender_reverse_mapping)
best_sample_df['country'] = best_sample_df['country'].replace(country_reverse_mapping)
best_sample_df['age_group'] = best_sample_df['age_group'].replace(age_group_reverse_mapping)

best_sample_df.to_excel("Excel-Sheets/best-sample.xlsx")
