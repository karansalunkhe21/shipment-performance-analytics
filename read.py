import pandas as pd

df = pd.read_csv("data/raw/DataCoSupplyChainDataset.csv", encoding="latin-1")

print(df.shape)
print(df.columns.tolist())
print(df.head())