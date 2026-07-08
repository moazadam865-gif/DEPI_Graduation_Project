import pandas as pd

print("Loading files...")
# تم تصحيح مسارات الملفات هنا لتقرأ الملفات الصحيحة
orders = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_orders_dataset.csv')
items = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_order_items_dataset.csv')
customers = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_customers_dataset.csv')
payments = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_order_payments_dataset.csv')
reviews = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_order_reviews_dataset.csv')
products = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_products_dataset.csv')
sellers = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_sellers_dataset.csv')
translation = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\product_category_name_translation.csv')
geo = pd.read_csv(r'D:\DBI\Final progect\Brazilian E-Commerce Public Dataset by Olist\olist_geolocation_dataset.csv')

for df in [orders, items, customers, payments, reviews, products, sellers, translation, geo]:
    df.drop_duplicates(inplace=True)

geo_clean = geo.drop_duplicates(subset=['geolocation_zip_code_prefix']).copy()

print("Merging tables...")

df_merged = pd.merge(orders, items, on='order_id', how='inner')
df_merged = pd.merge(df_merged, payments, on='order_id', how='left')
df_merged = pd.merge(df_merged, reviews, on='order_id', how='left')
df_merged = pd.merge(df_merged, customers, on='customer_id', how='inner')
df_merged = pd.merge(df_merged, products, on='product_id', how='left')
df_merged = pd.merge(df_merged, translation, on='product_category_name', how='left')
df_merged = pd.merge(df_merged, sellers, on='seller_id', how='left')

df_merged = pd.merge(df_merged, geo_clean, 
                     left_on='customer_zip_code_prefix', 
                     right_on='geolocation_zip_code_prefix', 
                     how='left')
df_merged.rename(columns={'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'}, inplace=True)
df_merged.drop('geolocation_zip_code_prefix', axis=1, inplace=True)

df_merged = pd.merge(df_merged, geo_clean, 
                     left_on='seller_zip_code_prefix', 
                     right_on='geolocation_zip_code_prefix', 
                     how='left', suffixes=('', '_seller_geo')) 
df_merged.rename(columns={'geolocation_lat': 'seller_lat', 'geolocation_lng': 'seller_lng'}, inplace=True)
df_merged.drop('geolocation_zip_code_prefix', axis=1, inplace=True)

df_final = df_merged.drop_duplicates()

print("\nAll 9 files merged successfully without duplicates!")
print("Dimensions of the final merged table (rows, columns):", df_final.shape)

df_final.to_csv('Olist_Master_Dataset.csv', index=False, encoding='utf-8')
print("File saved successfully as 'Olist_Master_Dataset.csv' in the same folder!")