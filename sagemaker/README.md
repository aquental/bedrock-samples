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
