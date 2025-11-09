import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load training data
train_data = pd.read_csv('data/california_housing_train.csv')
X_train = train_data.drop('MedHouseVal', axis=1)
y_train = train_data['MedHouseVal']

print(f"Training with {len(X_train)} samples")
print(f"Features: {list(X_train.columns)}")

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

print("Model training completed!")

# Use the trained model to make predictions on X_train and store in y_train_pred
y_train_pred = model.predict(X_train)

# Print the shape of y_train_pred to verify it matches the number of training samples
print(f"Shape of predictions array: {y_train_pred.shape}")

# Save the trained model to a file called trained_model.joblib
joblib.dump(model, 'trained_model.joblib')

# Print a confirmation message
print("Model successfully saved to 'trained_model.joblib'")
