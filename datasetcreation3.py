#  Created by Thomas Avare on 07/05/2023 19:11

import pandas as pd
from numpy import split, random, arange

from datasetcreation import a_or_an

def random_index(nb, size):
    """
    split in two arrays two separates sets that include each index to max
    :param nb: number of index
    :param size: size of the first array
    :return: two arrays, one of len "size" and one of "nb - size"
    """
    index = arange(nb)
    random.shuffle(index)

    return index[:size]


if __name__ == "__main__":
    waste_df = pd.read_excel('waste2.xlsx')
    templates_df = pd.read_csv('waste-templates.csv')
    phrases, other_phrases, classe = [], [], []

    for _, row in waste_df.iterrows():
        indexes = random_index(templates_df.size, int(templates_df.size * 0.8))
        for temp in range(templates_df.size):
            for i in [a_or_an(row["Object"]), 'this', 'my']:
                str = templates_df.template[temp].replace("[a/an/my/this]", i).replace("[object]", row["Object"].lower())
                if temp in indexes:
                    phrases.append([str, row["Class"], row["Class_id"]])
                else :
                    other_phrases.append([str, row["Class"], row["Class_id"]])

    phrases_df = pd.DataFrame(phrases, columns=["Phrase", "Class", "Class_index"])
    other_phrases = pd.DataFrame(other_phrases, columns=["Phrase", "Class", "Class_index"])

    # train, validate, test = split(phrases_df.sample(frac=1, random_state=42),
    #                               [int(.6 * len(phrases_df)), int(.8 * len(phrases_df))])

    train, test = split(phrases_df.sample(frac=1, random_state=42),
                                  [int(.8 * len(phrases_df))])

    # print(len(train), len(test), len(validate))

    tot = len(train) + len(test)
    print("size train:", len(train), "->", len(train) / tot)
    print("size test:", len(test), "->", len(test) / tot)
    print("other: ", len(other_phrases))

    train.to_json("train2.json")
    test.to_json("test2.json")
    # validate.to_json("validation2.json")

    train.to_csv("train2.csv")
    test.to_csv("test2.csv")
    other_phrases.to_csv("unseen_phrases.csv")
    # validate.to_csv("validation2.csv")
