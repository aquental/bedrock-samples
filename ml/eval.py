import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load test data
test_data = pd.read_csv('data/california_housing_test.csv')
X_test = test_data.drop('MedHouseVal', axis=1)
y_test = test_data['MedHouseVal']

# Load the trained model
model = joblib.load('trained_model.joblib')

# Make predictions
y_pred = model.predict(X_test)


# Set up the figure with size (10, 8)
plt.figure(figsize=(10, 8))
# Create a scatter plot of y_test vs y_pred with alpha=0.5
plt.scatter(y_test, y_pred, alpha=0.5)
# Add the red dashed reference line from min to max values with line width 2
plt.plot([y_test.min(), y_test.max()], [
         y_test.min(), y_test.max()], 'r--', lw=2)
# Add x-axis label 'Actual Values'
plt.xlabel('Actual Values')
# Add y-axis label 'Predicted Values'
plt.ylabel('Predicted Values')
# Add title 'Predictions vs Actual Values'
plt.title('Predictions vs Actual Values')
# Add grid with alpha=0.3
plt.grid(True, alpha=0.3)
# Show the plot
plt.show()
