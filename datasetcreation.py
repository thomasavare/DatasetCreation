#  Created by Thomas Avare on 07/05/2023 19:11

import pandas as pd
from numpy import split

waste_df = pd.read_excel('waste.xlsx')
templates_df = pd.read_csv('waste-templates.csv')
phrases, classe = [], []


def a_or_an(str):
    if str[0] in 'aeiouy':
        return "an"
    return "a"


for temp in templates_df.template:
    for _, row in waste_df.iterrows():
        for i in [a_or_an(row["Object"]), 'this', 'my']:
            str = temp.replace("[a/an/my/this]", i).replace("[object]", row["Object"].lower())
            phrases.append([str, row["Class"], row["Class_id"]])

phrases_df = pd.DataFrame(phrases, columns=["Phrase", "Class", "Class_index"])
#print(phrases_df)

train, validate, test = split(phrases_df.sample(frac=1, random_state=42), [int(.6*len(phrases_df)), int(.8*len(phrases_df))])

print(len(train)+len(test)+len(validate))


train.to_json("train.json")
test.to_json("test.json")
validate.to_json("validation.json")

train.to_csv("train.csv")
test.to_csv("test.csv")
validate.to_csv("validation.csv")

print(phrases_df.Class.sort_values().drop_duplicates().reset_index()["Class"].to_dict())


