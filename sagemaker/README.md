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
print(df.describe())

# TODO: Check for missing values using df.isnull().sum()
print("\nMissing values:")
print(df.isnull().sum())
```
