import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Calculate z-scores for each column
z_scores = np.abs((df - df.mean()) / df.std())

# Keep only the rows with all z-scores less than 3
df = df[(z_scores < 3).all(axis=1)]

# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_data.csv', index=False)
