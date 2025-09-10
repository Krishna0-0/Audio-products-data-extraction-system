import pandas as pd
import time
import google.generativeai as genai
import ast 
import random 
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

keys = os.getenv('GEMINI_API_KEYS', '').split(',')
if not keys or keys == ['']:
    raise ValueError("GEMINI_API_KEYS environment variable not set")

model1 = genai.GenerativeModel('gemini-1.5-pro')

filexl = os.getenv('EXCEL_FILE', 'data1.xlsx')
log_file = os.getenv('LOG_FILE', 'logfile.txt')


df = pd.read_excel(filexl)
# Get the first row (index 0) as a dictionary
first_row = df.iloc[0].to_dict()
inp = []
# Print the first row values
for attribute, value in first_row.items():
     if "name" in attribute:
        inp.append(value)
start = int(input("Start Index: "))
#inp gets sent to AI
attributes = {value: attribute for attribute, value in first_row.items() if "name" in attribute}
i = 0

import re
import requests
import pandas as pd

api_key = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

search_query = 'OnePlus Nord Buds 2r'
url = 'https://www.googleapis.com/customsearch/v1'

def search_on_site(site, query):
    params = {
        'q': query,
        'key': api_key,
        'filter': 1,
        'gl': 'IN',
        'hl': 'en',
        # 'exactTerms': 'Realme Air buds 6',
        'cx': search_engine_id,
        'filter': 1,
        'siteSearch': site, 
        'num': 2,
    }
    response = requests.get(url, params=params)
    return response.json()

sites = ['flipkart.com','amazon.in','gadget360.com','smartprix.com','91mobiles.com']

#Attributes is for mapping
with open(log_file, mode='a') as file:
    file.write(f"\n Script Started\n")
for index, row in df.iloc[start:len(df.index)].iterrows():
    links = []
    productname = row['Name']
    for s in sites:
        results = search_on_site(s, productname)
        if 'items' in results:
            for item in results['items']:
                links.append((item['link']))

    params = {
        'q': productname,
        'key': api_key,
        'gl': 'IN',
        'hl': 'en',
        'filter': 1,
        # 'exactTerms': 'Realme Air buds 6',
        'cx': search_engine_id,
        'num': 4,
    }
    response = requests.get(url, params=params)
    general_results = response.json()

    if 'items' in general_results:
        for item in general_results['items']:
            links.append((item['link']))
    # i += 1
    # if(i == 12):
    #     break
    genai.configure(api_key=random.choice(keys))
    
    print(productname)
    print(links)
    response = model1.generate_content(f'''Search the web and retrieve the details precisely from these websites {links} 
    if you dont find data on ANC(Active Noise Cancelling) on any website then consider it a No ! be cautious to never consider ENC !!! or anything else, NO RUBBISH DATA especially for ANC and driver size and 
    design type- in-ear, open-ear, meanwhile design means -> TWS Earbuds or wiredneckband...etc for the product: {productname}. 
    Provide the details in the given order {inp} and the also price without the inr sign only and present them as a dictionary ONLY
    with key-value pairs where the values are strings only. Check the values 
    twice especially the driver size and ANC  for accuracy and Bring as much as possible data. 
    Do not include any text that is not explicitly asked for. ''')
    
    res = ast.literal_eval(response.text)
    final_dict = {attributes[key].replace('name', 'value(s)'): value for key, value in res.items()}

    for key, value in final_dict.items():
        if key in df.columns:
            df.at[index, key] = value

    with open(log_file, mode='a') as file:
        file.write(f"\n\nProduct Name: {productname}\n")
        for key, val in res.items():
            file.write(f"{key} : {val}\n")
        
    try:
        df.to_excel(filexl, index=False, engine='openpyxl')
        print(f"Data for the entry {index + 1} updated in {filexl}")
    except Exception as e:
        print(f"Error writing the Excel file: {e}")
    time.sleep(45)