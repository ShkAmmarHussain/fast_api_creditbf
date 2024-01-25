import shap
import numpy as np
import pandas as pd
# from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
# from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib



def train_model():
    # Load the Credit Report dataset
    # data = load_boston()
    data = pd.read_csv('Final_data.csv')
    #Calculate Credit Ratio
    data = data.loc[~(data['Credit Limit'] == 0)] # Dropping all rows with credit limit 0
    data['credit_ratio'] = (data['Total Balances'] / data['Credit Limit'])

    #Split into input and target
    X = data.drop(labels='Credit Score',axis=1)
    y = data['Credit Score'].to_frame()
    y = y.values.ravel()


    # Define categorical features for Label Encoding
    categorical_features = ['Bureau']

    # Apply Label Encoding to categorical features
    label_encoders = {}
    for feature in categorical_features:
        label_encoders[feature] = LabelEncoder()
        X[feature] = label_encoders[feature].fit_transform(X[feature])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train an RandomForest Regression model
    random_forest_model = RandomForestRegressor(random_state=42)
    random_forest_model.fit(X_train, y_train)

    # # Saving model 
    # xgb_model.save_model('my_model.json')

    ## Create a SHAP explainer
    explainer = shap.Explainer(random_forest_model,feature_names=X_train.columns)

    # Save the SHAP explainer to a file
    joblib.dump(explainer, 'shap_explainer.pkl')

    # import pickle

    # with open('filename.pkl', 'wb') as f:
    #     pickle.dump(xgb_model, f)



train_model()