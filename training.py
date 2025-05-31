import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import time
import pickle

# Load the CSV
df = pd.read_csv('pricing_data.csv')
print(df.head())
# Extract relevant columns
df['Year'] = df['Fiscal_Week_ID'].str.split('-').str[0].astype(int)
df['Week'] = df['Fiscal_Week_ID'].str.split('-').str[1].astype(int)
X = df[['Price', 'Competition_Price','Year','Week']]
y = df[['Sales_Amount']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate
start = time.time()
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")
print(time.time()-start)

# Predict on the test set
y_pred = model.predict(X_train)

# Evaluate
start = time.time()
mse = mean_squared_error(y_train, y_pred)
r2 = r2_score(y_train, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")
print(time.time()-start)

with open("pricemodel.py", "wb") as f:
    pickle.dump(model, f)

'''
Mean Squared Error: 11019.780168124393
R² Score: 0.9974690866009057
Time: 0.0022537708282470703
'''