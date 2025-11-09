import pandas as pd

# Load training data
train_data = pd.read_csv('data/california_housing_train.csv')

# Create X_train by dropping the 'MedHouseVal' column from train_data
X_train = train_data.drop('MedHouseVal', axis=1)

# Create y_train with just the 'MedHouseVal' column from train_data
y_train = train_data['MedHouseVal']

# Print the shape of X_train to verify it contains the features
print(f"Training with {len(X_train)} samples")

# Print the shape of y_train to verify it contains the target values
print(f"Features: {list(X_train.columns)}")
