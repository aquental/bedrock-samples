```python
import pandas as pd

# Load the California housing dataset

df = pd.read_csv('data/california_housing.csv')

# TODO: Display dataset info using df.info()

print("Dataset structure and schema:")
df.info()

# TODO: Print the column names using df.columns

print("\nColumn names:", df.columns)

# TODO: Print the data types using df.dtypes

print("\nData types:", df.dtypes)
```

```python
import pandas as pd

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# TODO: Generate statistical summary using df.describe()
# Remember to set pandas to display all columns first!
print("Statistical summary:")
pd.set_option('display.max_columns', None)  # Show all columns
print(df.describe())

# TODO: Check for missing values using df.isnull().sum()
print("\nMissing values:")
print(df.isnull().sum())
```

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# Create a histogram of MedHouseVal with bins=50 and alpha=0.7
plt.hist(df['MedHouseVal'], bins=50, alpha=0.7)
# Add a title 'Distribution of House Values'
plt.title('Distribution of House Values')
# Add x-axis label 'Median House Value'
plt.xlabel('Median House Value')
# Add y-axis label 'Frequency'
plt.ylabel('Frequency')
# Display the plot
plt.show()
```

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')
# Calculate the correlation matrix using df.corr()
correlation_matrix = df.corr()
# Create a heatmap using sns.heatmap() with annot=True, cmap='coolwarm', and center=0
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
# Add a title 'Feature Correlation Matrix'
plt.title('Feature Correlation Matrix')
# Display the plot
plt.tight_layout()
plt.show()
```

```python
import pandas as pd

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# Create the new RoomsPerHousehold feature by dividing AveRooms by AveOccup
df['RoomsPerHousehold'] = df['AveRooms'] / df['AveOccup']

# Display sample rows showing AveRooms, AveOccup, and the new RoomsPerHousehold feature
print(df[['AveRooms', 'AveOccup', 'RoomsPerHousehold']].head())
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# Create a new feature: average number of rooms per household
df['RoomsPerHousehold'] = df['AveRooms'] / df['AveOccup']

# Select relevant features for modeling
feature_columns = [
    'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population',
    'AveOccup', 'Latitude', 'Longitude', 'RoomsPerHousehold'
]

# TODO: Separate features (X) from the target variable (y)
X = df[feature_columns]
y = df['MedHouseVal']
# TODO: Split the data using train_test_split with test_size=0.2 and random_state=42
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# TODO: Print the shape of X_train
# TODO: Print the shape of X_test
# TODO: Print the shape of y_train
# TODO: Print the shape of y_test
print(f"X Training set size: {X_train.shape[0]} samples")
print(f"X Test set size: {X_test.shape[0]} samples")
print(f"Y Training set size: {y_train.shape[0]} samples")
print(f"Y Test set size: {y_test.shape[0]} samples")
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# Create a new feature: average number of rooms per household
df['RoomsPerHousehold'] = df['AveRooms'] / df['AveOccup']

# Select relevant features for modeling
feature_columns = [
    'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population',
    'AveOccup', 'Latitude', 'Longitude', 'RoomsPerHousehold'
]
X = df[feature_columns]
y = df['MedHouseVal']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Select features to cap (all numeric except Latitude and Longitude)
features_to_cap = [
    'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population',
    'AveOccup', 'RoomsPerHousehold'
]

# Dictionary to store capping thresholds
cap_values = {}

# For each feature in features_to_cap, calculate the 95th percentile
for feature in features_to_cap:
    cap_values[feature] = X_train[feature].quantile(0.95)

# Print out each feature and its calculated 95th percentile threshold to verify
for feature, threshold in cap_values.items():
    print(f"Feature: {feature}, 95th Percentile Threshold: {threshold:.4f}")
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the California housing dataset
df = pd.read_csv('data/california_housing.csv')

# Create a new feature: average number of rooms per household
df['RoomsPerHousehold'] = df['AveRooms'] / df['AveOccup']

# Select relevant features for modeling
feature_columns = [
    'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population',
    'AveOccup', 'Latitude', 'Longitude', 'RoomsPerHousehold'
]
X = df[feature_columns]
y = df['MedHouseVal']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Cap numeric features at their 95th percentiles using ONLY training data
features_to_cap = X_train.select_dtypes(include=['float64']).columns.drop(['Latitude', 'Longitude'])

# Calculate capping thresholds from training data only
cap_values = {}
for feature in features_to_cap:
    cap_values[feature] = X_train[feature].quantile(0.95)

# Loop over each feature in features_to_cap
for feature in features_to_cap:
    # Cap X_train[feature] using .clip(upper=cap_values[feature])
    X_train[feature] = X_train[feature].clip(upper=cap_values[feature])
    # Cap X_test[feature] using the same threshold
    X_test[feature] = X_test[feature].clip(upper=cap_values[feature])

# Show summary statistics of X_train after preprocessing
print(X_train.describe())
```
