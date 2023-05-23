#  Created by Thomas Avare on 07/05/2023 19:11

import pandas as pd
from numpy import split, random

from datasetcreation import a_or_an

if __name__ == "__main__":
    waste_df = pd.read_excel('waste2.xlsx')
    templates_df = pd.read_csv('waste-templates.csv')
    phrases, classe = [], []

    for temp in random.choice(templates_df.template, templates_df.size // 2):
        for _, row in waste_df.iterrows():
            for i in [a_or_an(row["Object"]), 'this', 'my']:
                str = temp.replace("[a/an/my/this]", i).replace("[object]", row["Object"].lower())
                phrases.append([str, row["Class"], row["Class_id"]])

    phrases_df = pd.DataFrame(phrases, columns=["Phrase", "Class", "Class_index"])

    # train, validate, test = split(phrases_df.sample(frac=1, random_state=42),
    #                               [int(.6 * len(phrases_df)), int(.8 * len(phrases_df))])

    train, test = split(phrases_df.sample(frac=1, random_state=42),
                                  [int(.8 * len(phrases_df))])

    # print(len(train), len(test), len(validate))

    tot = len(train) + len(test)
    print("size train:", len(train), "->", len(train) / tot)
    print("size test:", len(test), "->", len(test) / tot)

    train.to_json("train2.json")
    test.to_json("test2.json")
    # validate.to_json("validation2.json")

    train.to_csv("train2.csv")
    test.to_csv("test2.csv")
    # validate.to_csv("validation2.csv")
