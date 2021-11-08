import sys
sys.path.append('..')

import json
from utils import DataProcessor
import pandas as pd
from nltk.stem import WordNetLemmatizer

record = DataProcessor._read_jsonl("../data/dev.jsonl")
df = pd.DataFrame(record)

df['prediction'] = open("../output/predictions_dev.lst").read().split()
lemmatizer = WordNetLemmatizer()
# accuracy by concreteness
concreteness_lookup = pd.read_csv("/home/cuichenx/Courses/11-711/psycoling_covariates/original_concreteness.csv",
                                  index_col='Word').to_dict()['Conc.M']
df['option1_conc'] = df['option1'].apply(lambda x: concreteness_lookup.get(lemmatizer.lemmatize(x), -1))
df['option2_conc'] = df['option2'].apply(lambda x: concreteness_lookup.get(lemmatizer.lemmatize(x), -1))

def decide(x):
    a, b = x['option1_conc'], x['option2_conc']
    if a == b:
        return 0
    if a > b:
        return 1
    else:
        return 2

df['prediction_conc'] = df.apply(decide, axis=1)
df_nonname = df[df['prediction_conc']>0]
print("answer matches with conc prediction")
print((df_nonname['answer'].astype(int) == df_nonname['prediction_conc']).value_counts())

print("model prediction matches with conc prediction")
print((df_nonname['prediction'].astype(int) == df_nonname['prediction_conc']).value_counts())

stop = 'here'



# which answer occurs first
# answer_occurs_first = []
# for (i, row) in df.iterrows():
#     option1, option2 = row['option1'].lower(), row['option2'].lower()
#     sentence = row['sentence'].lower()
#     answer = row['answer']
#     answer_occurs_first.append(int(
#         answer=='1' and sentence.index(option1) < sentence.index(option2) or
#         answer=='2' and sentence.index(option1) > sentence.index(option2)
#     ))
# df['answer_occurs_first'] = answer_occurs_first

# df.to_csv("../output/dev_preds.csv")
