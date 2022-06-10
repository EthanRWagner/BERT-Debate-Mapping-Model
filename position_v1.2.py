# Author:         Ethan Wagner
# File Name:      position.py
# Date:           17 April 2022

# Objective: Use the BERT NLP model to train a neural network to identify whether a given statement is an affirmative or negative position to the topic.

from bert_serving.client import BertClient
import pandas as pd
import numpy as np
import time
from typing import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

#Start up for BERT server: bert-serving-start -model_dir cased_L-12_H-768_A-12/ -num_worker=2

# Create Data Set
def make_training_set() -> list:
    
    training_set = [[], []]
    # training_set.append([])
    # training_set.append([])
    csv_data = pd.read_excel('Final Argument Position Data.xlsx')
    #print("<", csv_data["Topic"].iloc[0], "> ", csv_data["Statement"].iloc[0], " : ", csv_data["Truth Value"].iloc[0])
    for i in range(len(csv_data)):
        key = "<" + csv_data["Topic"].iloc[i] + "> " + csv_data["Statement"].iloc[i]
        training_set[0].append(key)
        training_set[1].append(csv_data["Truth Value"].iloc[i])

    return training_set

## Pre-training done on BERT not done by user
# Mutli-headed Attention
# Feed Forward
# Positional Embedding


# Classification Layer

def main() -> None:

    #Parameters
    # test_size = 0.25

    #start time
    start_time = time.time()

    # Start client connection
    bert = BertClient(check_length=False)

    #Formulated and usable set for splitting into training and validation sets
    full_set = make_training_set()

    #Split into training and validation sets (lists), encode training set
    '''
    X_tr : training input
    y_tr : training labels
    X_val : validation input
    y_val : validation labels
    '''
    # print(type(full_set[0]))
    # print(type(full_set[1]))
    # exit(0)
    # print(full_set[0][0])
    # print(full_set.items().tolist())
    X_tr, X_val, y_tr, y_val = train_test_split(full_set[0], full_set[1], test_size=0.20, random_state=42)
    X_tr_bert = bert.encode(X_tr)
    X_val_bert = bert.encode(X_val)

    # print(len(X_tr_bert[0]))
    # exit(0)

    #Logistic Regression 
    '''
    NOTES:
    '''
    model_bert = LogisticRegression(max_iter=1000)
    
    #training the model
    model_bert = model_bert.fit(X_tr_bert, y_tr)

    #prediction model
    pred_bert = model_bert.predict(X_val_bert)

    #Print Results
    print("\n---Results---")
    print("\nAccuracy Score: {:.2f}%".format(100*accuracy_score(y_val, pred_bert)))
    print("Executuion Time: {:.2f}s\n\n".format((time.time() - start_time)))

if __name__ == "__main__":
    main()