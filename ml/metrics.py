import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

# Make predictions on training data
y_train_pred = model.predict(X_train)

# Calculate Mean Squared Error using mean_squared_error function
mse = mean_squared_error(y_train, y_train_pred)

# Calculate R-squared score using r2_score function
r2 = r2_score(y_train, y_train_pred)

# Display the evaluation metrics
print(f"Mean Squared Error: {mse:.4f}")
print(f"R-squared Score: {r2:.4f}")
