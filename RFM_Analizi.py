###############################################################
# Customer Segmentation with RFM
###############################################################

###############################################################
# (Business Problem)
###############################################################

# An e-commerce company wants to segment its customers and
# determine marketing strategies according to these segments.
# Veri Seti: https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

##########################
# Variables
##########################

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

##########################
# importing libaries
##########################
import datetime as dt
import pandas as pd
pip install openpyxl

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


#########################
# Get the data about 2010-2011 years
#########################
df= pd.read_excel('hafta_3\online_retail.xlsx', sheet_name="Year 2010-2011")
df = df.copy()

###############################################################
# Understanding Data Sets
###############################################################

def check_df(dataframe):
    print(f"""
        ##################### Shape #####################\n\n\t{dataframe.shape}\n\n
        ##################### Types #####################\n\n{dataframe.dtypes}\n\n
        ##################### Head #####################\n\n{dataframe.head(3)}\n\n
        ##################### NA #####################\n\n{dataframe.isnull().sum()}\n\n
        ##################### Quantiles #####################\n\n{dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T}\n\n""")

check_df(df)

###############################################################
# Data Preperation
###############################################################

# Is there any nan value? How many missing observations are there??
df.dropna(inplace=True)
df.isnull().values.any()

# How many unique products?
df["Description"].nunique()

# What are the quantities of the products?
df["Description"].value_counts().head()

# Let's list the 5 most ordered products from most to least.
df.groupby("Description").agg({"Quantity": "sum"}).sort_values(("Quantity"), ascending=False).head()

# The 'C' in the invoices shows the canceled transactions. Let's remove the canceled transactions from the dataset.
df = df[~df["Invoice"].str.contains("C", na=False)]
df.head()
df.shape

# Let's create a variable called 'TotalPrice' that represents the total price per invoice.
df["TotalPrice"] = df["Quantity"] * df["Price"]

# The date on which the analysis should be performed.
df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11)

###############################################################
# RFM Metrics
###############################################################

# Recency: the difference between today and the customer's last purchase date, in days
# Frequency: total number of purchases.
# Monetary: total spend by the customer.

rfm= df.groupby("Customer ID").agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                    'Quantity': lambda num: num.nunique(),
                                    'TotalPrice': lambda price: price.sum()})

rfm.columns = ['recency', 'frequency', "monetary"]
rfm = rfm[(rfm['monetary'] > 0)] # condition
rfm.head()

###############################################################
# Calculations RFM Scores and Defining Segments
###############################################################

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# We assign 5 points to the date close to the date of analysis.

rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
# We give 1 point to customers with low shopping frequency.
# NOTE : Monetary is not processed because it is not used in segment definition.

# Defining segments
rfm['rfm_segment'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) # make them categorical
rfm.head()

###############################################################
# Giving a name of RFM scores
###############################################################

    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['rfm_segment'] = rfm['rfm_segment'].replace(seg_map, regex=True)

rfm = rfm[["recency", "frequency", "monetary", "rfm_segment"]] # we take the names above
rfm.head()

###############################################################
# Analyzing the top 3 important segments
###############################################################

rfm[["rfm_segment", "recency", "frequency", "monetary"]].groupby("rfm_segment").agg(["mean", "count"])
rfm[rfm["rfm_segment"] == "cant_loose"].head()
rfm[rfm["rfm_segment"] == "about_to_sleep"].head()
rfm[rfm["rfm_segment"] == "new_customers"].head()
