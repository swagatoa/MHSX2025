import pandas as pd
import numpy as np
import pickle

# Load the saved model
with open("pricemodel.py", "rb") as f:
    model = pickle.load(f)



def run_inference(price, competition, year, week):
    new_data = {
        "Price": price,
        "Competition_Price": competition,
        "Year": year,
        "Week": week
    }
    # Create a DataFrame from new data
    X_new = pd.DataFrame(new_data)

    # Predict sales amount
    predicted_sales = model.predict(X_new)
    return predicted_sales

feature_names = ['Price', 'Competition_Price','Year','Week']


if __name__ == "__main__":

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        for name, importance in zip(feature_names, importances):
            print(f"{name}: {importance}")
    else:
        print("Model does not support feature importances.")