import pandas as pd

# Load your CSV file
df = pd.read_csv('new.csv')

# Assuming the column is named 'grade' and has values like '5A', '6B', etc.
# Extract numeric part (grade number)
df['grade_number'] = df['grade'].str.extract(r'(\d+)').astype(int)

# Extract alphabetic part (section letter)
df['section'] = df['grade'].str.extract(r'([A-Za-z])')

# Optional: replace original 'grade' column with number only
df['grade'] = df['grade_number']
df = df.drop(columns=['grade_number'])

# Save or check the result
df.to_csv('your_file_split.csv', index=False)
print(df.head())
