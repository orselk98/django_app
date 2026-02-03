import pandas as pd




my_dict = {
    "Subject": ["Math", "Science", "English", "History"],
    "Duration": [60, 45, 30, 50],
}
df=pd.DataFrame(my_dict)

print(df["Subject"])
print(df["Duration"])