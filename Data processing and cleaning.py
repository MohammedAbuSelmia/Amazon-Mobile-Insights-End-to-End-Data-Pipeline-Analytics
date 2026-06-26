
import pandas as pd
from sqlalchemy import create_engine,types
import sqlalchemy as sql
import numpy as np

##--Now I want to configure the connection settings in sql

server_name = 'DESKTOP-S0OHOAK'  
database_name = 'Amazon_Mobile_Insights'   
connection_string = f'mssql+pyodbc://{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
engine= create_engine(connection_string)

##--Now I want to connect, clean the data, and send it to the database Amazon_Mobile_Insights.

data=pd.read_csv(r"C:\Users\hp\Desktop\Amazon_Unlocked_Mobile.csv"
                 ,usecols=['Product Name', 'Brand Name', 'Price','Rating']
                 ,dtype={'Product Name':str,
                         'Brand Name':str,
                         'Price':str})
print(data.info())

# # ##- Clean Data in  Brand Name Column
# # # # Now I want to clean the Product Name column
data['Brand Name']=data['Brand Name'].fillna('unknown')

# print("**************************************",(data["Brand Name"]=='unknown').sum())
# # # This function is very important because through it we replaced the unknown value with known and correct values  
brands_new = ["Apple","Samsung","Huawei","Honor","Lenovo","LG","Sony","HTC",
           "Nokia","Motorola","BlackBerry","Asus","Acer","Alcatel","ZTE",
           "Google","Microsoft","OnePlus","BLU"]
print('before th edit *************************',(data["Brand Name"]=='unknown').sum())
def replace_name(name):
     curent_name=str(name['Brand Name']).lower()
     pro_name=str(name['Product Name']).lower()
     if curent_name =='unknown':
       for i in brands_new:
         if i.lower() in pro_name:
            return i.capitalize() 
       return 'unknown'
    
     return curent_name.capitalize()  
data['Brand Name']=data.apply(replace_name,axis=1)
print('after the edit  ****************************',(data["Brand Name"]=='unknown').sum())# this code to confirm the func working true
print('********************',(data["Brand Name"].isnan()).sum())
print(data['Brand Name'].value_counts())# this code to confirm that he made the transfer



# # ##--Clean Data in Price Column
# print(data[data['Price'].str.contains(r'\$ |,',na=False)])# this code to sure the price do not contains $ or , becuse we want to sent to  sql server
if 'Price' in data.columns:
     data['Price']=data['Price'].str.replace(r'[$,]','',regex=True)
     



data['Price']=data['Price'].astype(float) # in this code we convert datatype frpm str to float
# # print(data.info())# new i check up datatype
meanPrice=np.mean(data['Price'])
# print(meanPrice)
data['Price']=data['Price'].fillna(meanPrice) # her i fill insted of null to mean_Value 

data=data.drop_duplicates() # This is important step because drop the data drop_duplicates

# # # # # ##-Now I want to define the data types in preparation for transferring them to SQL.
data_type={
    'Product Name':sql.types.VARCHAR(2000) , 
    'Brand Name':sql.types.VARCHAR(200),
    'Price':sql.types.Float
}

# # # ##-- Now I wnat to sent the file csv to sql server
data.to_sql(
    name=database_name,
    con=engine,
    chunksize=1000,
    index=False,
    if_exists='replace',
    dtype=data_type
)

print("It has been sent successfully")
