import pandas as pd


TYPES_ESSAY = {"MBC": 7, "MIC": 4}
t1 = ["MBC"]

t2 = ["MIC"]

t3 = ["MBC", "MIC"]
t4 = ["MIC", "MBC"]

print(t1[0] in TYPES_ESSAY.keys())
print(t2[0] in TYPES_ESSAY.keys())
print([*TYPES_ESSAY.keys()] == sorted(t4))

print(t1[0] in TYPES_ESSAY.keys() or [*TYPES_ESSAY.keys()] == sorted(t1))
print(t4[0] in TYPES_ESSAY.keys() or [*TYPES_ESSAY.keys()] == sorted(t4))

data = {
    'TransactionID': [101, 102, 103, 101, 104, 105, 103],
    'Product': ['Laptop', 'Monitor', 'Keyboard', 'Laptop', 'Mouse', 'Webcam', 'Keyboard'],
    'Price': [1200, 300, 75, 1200, 25, 50, 75]
}

df = pd.DataFrame(data)
err = set(df['TransactionID'])
print(err)
transId = [99, 101, 102, 103, 101, 104, 105, 103, 110]
print(set(transId) - err)