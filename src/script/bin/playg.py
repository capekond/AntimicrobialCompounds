import pandas as pd

# Data for the DataFrame
data = {
    'TransactionID': [101, 102, 103, 101, 104, 105, 103],
    'Product': ['Laptop', 'Monitor', 'Keyboard', 'Laptop', 'Mouse', 'Webcam', 'Keyboard'],
    'Price': [1200, 300, 75, 1200, 25, 50, 75]
}

# Create the pandas DataFrame
df = pd.DataFrame(data)


print("--- Original DataFrame with Duplicates ---")
print(df)
print("--------------")
print(df['TransactionID'])
print("--------------")
err = set(df['TransactionID'])
print(err)
transId = [99, 101, 102, 103, 101, 104, 105, 103, 110]
print(set(transId) - err)