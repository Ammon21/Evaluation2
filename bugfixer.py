import pandas as pd
df = pd.read_csv("eval.csv")
print(df.Teacher.value_counts())