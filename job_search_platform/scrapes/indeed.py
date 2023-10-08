import pandas as pd

df = pd.read_json("./scrapes/indeedData.json")
df = df.iloc[0:5]  # limiting the range as this process takes time

print(df)