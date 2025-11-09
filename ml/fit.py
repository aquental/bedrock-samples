import pandas as pd
from sklearn.linear_model import LinearRegression

# Load training data
train_data = pd.read_csv('data/california_housing_train.csv')
X_train = train_data.drop('MedHouseVal', axis=1)
y_train = train_data['MedHouseVal']

print(f"Training with {len(X_train)} samples")
print(f"Features: {list(X_train.columns)}")

# Create the LinearRegression model
model = LinearRegression()

# Fit the model to the training data using X_train and y_train
model.fit(X_train, y_train)

# Print the model's coefficients to verify training worked
print(f"Model coefficients: {model.coef_}")

# Print the model's intercept to verify training worked
print(f"Model intercept: {model.intercept_}")
