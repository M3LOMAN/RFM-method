import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"/C:/Users/Владимир/OneDrive/Документы/rfm/OnlineRetail.csv", encoding="ISO-8859-1")
df.head()

df = df[df['CustomerID'].notna()]
df.head()
df_fix = df.sample(10000, random_state = 42)
df_fix.head()

from datetime import datetime
df_fix["InvoiceDate"] = pd.to_datetime(df_fix['InvoiceDate'], errors='coerce')
df_fix["InvoiceDate"] = df_fix["InvoiceDate"].dt.date
# Create TotalSum colummn
df_fix["TotalSum"] = df_fix["Quantity"] * df_fix["UnitPrice"]
# Create date variable that records recency
import datetime
snapshot_date = max(df_fix.InvoiceDate) + datetime.timedelta(days=1)
# Aggregate data by each customer
customers = df_fix.groupby(['CustomerID']).agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalSum': 'sum'})
# Rename columns
customers.rename(columns = {'InvoiceDate': 'Recency',
                            'InvoiceNo': 'Frequency',
                            'TotalSum': 'MonetaryValue'}, inplace=True)

customers.head()

quantiles = customers[['Recency','Frequency','MonetaryValue']].quantile([.2,.4,.6,.8]).to_dict()

def r_score(x):
    if x <= quantiles['Recency'][.2]:
        return 5
    elif x <= quantiles['Recency'][.4]:
        return 4
    elif x <= quantiles['Recency'][.6]:
        return 3
    elif x<=quantiles['Recency'][.8]:
        return 2
    else:
        return 1

def fm_score(x,y):
    if x<=quantiles[y][.2]:
        return 1
    elif x <= quantiles[y][.4]:
        return 2
    elif x <= quantiles[y][.6]:
        return 3
    elif x<=quantiles[y][.8]:
        return 4
    else:
        return 5

customers['R']=customers['Recency'].apply(lambda x: r_score(x))
customers['F']=customers['Frequency'].apply(lambda x: fm_score(x,'Frequency'))
customers['M']=customers['MonetaryValue'].apply(lambda x:fm_score(x,'MonetaryValue'))
customers['RFM']=customers['R'].map(str)+customers['F'].map(str)+customers['M'].map(str)

customers.head()

segt_map={
    r'[1-2][1-2]':'бездействие',
    r'[1-2][3-4]':'в зоне риска',
    r'[1-2][5]':'нельзя потерять',
    r'[3][1-2]':'засыпающий',
    r'[3][3]':'необходимо внимание',
    r'[3-4][4-5]':'постоянный клиент',
    r'[4][1]':'перспективный клиент',
    r'[5][1]':'недавний клиент',
    r'[4-5][2-3]':'потенциальный клиент',
    r'[5][4-5]':'любимый клиент'
}
customers['Client_type']=customers['R'].map(str)+customers['F'].map(str)
customers['Client_type']=customers['Client_type'].replace(segt_map, regex=True)

print(customers)