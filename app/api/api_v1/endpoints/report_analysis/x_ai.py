
import numpy as np
import joblib




def preprocess_data(bureau,balance,creditlimit):
    del bureau['Credit Score']
    label = {
        "TransUnion" : 2,
        "Experian" : 1,
        "Equifax" : 0
    }
    if bureau["Bureau"] in label:
        bureau["Bureau"] = label[bureau["Bureau"]]

    try:
        bureau['credit_ratio'] = (balance / creditlimit)
    except:
        bureau['credit_ratio'] = 0

    # Convert the dictionary values to a NumPy array
    return np.array(list(bureau.values()), dtype=object)

import pandas as pd

def weights(bureau,X):
    weight = {}
    explainer = joblib.load('shap_explainer.pkl')
    
    # Reshape example_data_point into a matrix with one row
    bureau = bureau.reshape(1, -1)

    # Generate SHAP values for the example data point
    shap_values = explainer(bureau)

    for key, value in zip(X, shap_values.values[0]):
        weight[key] = value
    
    return weight

def x_ai(trns, exp, equif):
    print(" entered xAI")
    trns_weight = {}
    exp_weight = {}
    equif_weight = {}
    features = list(trns.keys())
    features.remove('Credit Score')
    features.append('credit ratio')
    
    balance = int(trns['Total Balances']) + int(exp['Total Balances']) + int(equif['Total Balances'])
    credit = int(trns['Credit Limit']) + int(exp['Credit Limit']) + int(equif['Credit Limit'])

    processed_trns = preprocess_data(trns,balance,credit)
    processed_exp = preprocess_data(exp,balance,credit)
    processed_equif = preprocess_data(equif,balance,credit)
    print("weigts")
    if processed_trns[0] != '':
        trns_weight = weights(processed_trns,features)
    print("weigts1")
    if processed_exp[0] != '':
        exp_weight = weights(processed_exp,features)
    print("weigts2")
    if processed_equif[0] != '':
        equif_weight = weights(processed_equif,features)
    print("weigts3")
    print("left xAI")
    return trns_weight, exp_weight, equif_weight
