import requests
import pandas as pd
import random
import amazon_search
import flipkart_search
import time
import json
import ast
from bs4 import BeautifulSoup
import google.generativeai as genai

keys = ["AIzaSyBiECn9JR0wMuujNrYCBadYPykKJGk5asA"]
model1 = genai.GenerativeModel('gemini-2.5-pro',generation_config={"response_mime_type": "application/json"})
genai.configure(api_key=random.choice(keys))

search_engine = [['24e195608ec9d46c4','AIzaSyBg_4XdTYAdMcGv1JY48vdBRZk38rvbXo4']]
# search_query = 'Realme buds Air 6'

custom_headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
     'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
     'Cookie' : 'session-id=262-2285634-7972431; ext_name=ojplmecpdpgccookcobabopnaifgidhf; ubid-acbin=257-7270922-3650353; sst-acbin=Sst1|PQHCWI7g-LDVDmqDvpu22jgwCaat0JNUCIziIY-CWwZJOb1VW1ohyKy2eQNMcXqWv2n2o8RRg7Lmf32trfaAQf4_bP_vWYUYXfUovffPELlZMGnitQhV9bvUo86MNbJSCqEF6fTw53W62hp73uQn6N_ICegtWMajIbd9BwNThgZoevyIK1Ebs4fxoBavdxzgZNq55P6AwBxLc5eLCA9kr3VZCnN20MNF2GFVPmbn-zdLo5-YPgUJwAaqd7_OljrrxakQOjjuMVSBwjp8JZPth4wHJTKnG3RoOvyil6lSkAtm1jU; i18n-prefs=INR; x-acbin="uP6k4bXI43te7Aqqs9KJ@Kr@Nd6YHOB6r46gjrb4BTmcvMI0VlNnbire2vU20Xrj"; at-acbin=Atza|IwEBIC1fa8cHeixuVNdOnMzb2O0HN-HsVOG71lKSvlcfNEdS79w1_OppSh8iDDcVe_hEcO8PPubz34bonoPOFKvxJGXgukb4hVID_jwxcBAKa6VKzWN6Ts9W9ZUdzGbOrC4dCuch5GS4-wzeP7eRA5I5PrjU3aDjJUFbrseVnGKlNCZEwcHSDoQje2yZ0hfV2ut10ny9Qa7flaj_FX14ZPHjX6nOf7vWzAwNlJLlZB9YUK0IdA; sess-at-acbin="LBk6SHR+gV4m5Ly83tUVvOyOJpI1fEOzdN7OHPQShcA="; lc-acbin=en_IN; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiOGRiNjYyIiwia2V5IjoiWHQyM3I1YmdtbFhTYWZLWEF0UGovTjA0d3N6bTM2VmlKeFpPTjIxbC8rb0g2Y2JDYXFhejZpdGFjRUZoOVlkS3dXaU45RjR3aVhiRjU2Y3Y2MXVheXY3RjdpalFmQU93RUwxQ1R6ZkRvYzV0Y2Ntcnp4eEtZMFRvWDE0dXVZdHNOLy9GcGxJNDdQTHUzdE5nNHcrUE9aWGYybjgxMmIvaVAvY25EQXlKQlR5NUNUMUN0ekpsTFRUTWxrN3NCdzBWR0Urckp6dE1YaEQvQmY0aFNlSy96ZWNVY2JERklSQ0ZTc2plY21vQ0NUWW9yM2JEYlpLeFdRWlp4U3puZEVPYTZuRnFZUGtuTmRIT0RiZlI0ZHZtZ0ZXaWRtdmxsOWg1WWMrRVNsV0lJc3FENEJrRHlDc3JmaWErbDQ5VE83d1FuV0N0cXAxRkcxanZQRFE3RWxoWEN3PT0ifQ==; session-id-time=2082787201l; session-token=CNrn9/uaH9nqrH3iG34cCuHgZQ4QW0qavYpcbyA4hKruMAVoadXV96JNch7Yh8oIJ8ZbejiY4j/FL5NaEPUaoWFzMGFDVs8wWxHz/N5e0orKLZgrmzqOtWzNgu9MJVnaOLKvw1cZP6DWQlD/f3zaVcwFVN3fmU4g0V4facp94H0gUWh7mNbRwsb5Q2ILF3cv6CQmaerM9mQmFTNyUVQ4MQzgF0oIIBaf78FlOddm383wJzcQB3PmwVY7+3ezqXyN1viAX+Neg31vusd800bkBcZwKjVcb6f8Pyv8mRMNm2ZIudC/zEUuVJSfhPF2ei4F0x3gOnjunvMK8iwjH83uRD1gmH47WRhuxlgXb1XCVgro/B2yaCui3Di21KNy29+g; csm-hit=TQ93GC9S3DNA00SGRBNE+s-EKGMRA3KNCKKXY2P9QPX|1723495626933',
     "X-Amzn-Trace-Id": "Root=1-66ba761c-23a18c3915856d8c122d2adb",   
}

def search_on_site(site, query):
    url = 'https://www.googleapis.com/customsearch/v1'
    searching = random.choice(search_engine)
    params = {
        'q': query,
        'key': searching[1],
        'filter': 1,
        'gl': 'IN',
        'hl': 'en',
        'cx': searching[0],
        'num': 4 if site == 'web' else 2,
        'siteSearch': site if site != 'web' else None,
    }
    response = requests.get(url, params=params,headers={'Connection': 'close'})
    time.sleep(8)
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get('items', [])
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print(response.status_code)
            # print(f"Response Text: {response.text}")
    else:
        print(f"Failed request with status code: {response.status_code}")
        # print(f"Response Text: {response.text}")
    
    return []

filexl = 'data1.xlsx'
log_file = 'logfile.txt'
df = pd.read_excel(filexl)
# Get the first row (index 0) as a dictionary
first_row = df.iloc[0].to_dict()
inp = []
# Print the first row values
for attribute, value in first_row.items():
     if "name" in attribute:
        inp.append(value)

# sites = ['flipkart.com','amazon.in','smartprix.com','91mobiles.com','web']

start = int(input("Start Index: "))
attributes = {value: attribute for attribute, value in first_row.items() if "name" in attribute}

# Attributes is for mapping
with open(log_file, mode='a') as file:
    file.write(f"\n Script Started\n")
sites = ['amazon.in','flipkart.com']

for index, row in df.iloc[start:len(df.index)].iterrows():
    result = []
    final_context = ""
    productname = str(row['Name'])
    # productname = 'realme s2 watch'
    for site in sites:
        res = search_on_site(site, productname)
        time.sleep(5)
        for item in res:
            result.append(item['link'])
    
    for url in result:
        webpage = requests.get(url, headers=custom_headers)
        soup = BeautifulSoup(webpage.content, "lxml")
        if('amazon' in url) :
            final_context+=f"\nStart of New context please check if its the same product or some other variant by matching from Product's title(if different in any sense then skip this context) \nProduct Title :\n{amazon_search.amazon_get_title(soup)} \n\nBox Content:\n{amazon_search.amazon_get_box_cont(soup)} \n\nAbout Product:\n{amazon_search.amazon_get_about(soup)}\n\nMore info:\n{amazon_search.amazon_get_manufacturer_info(soup)}\n\nInfo Table:\n{amazon_search.amazon_get_table_data(soup)}\n\n\n"
        else :
            final_context+= f"\nStart of New context please check if its the same product or some other variant by matching from Product's title(if different in any sense then skip this context) \nProduct Title :\n{flipkart_search.flipkart_get_title(soup)}\n\nColor(s):\n{flipkart_search.flipkart_get_color(soup)}\n\nAbout Product:\n{flipkart_search.flipkart_get_about(soup)}\n\nSome Description:\n{flipkart_search.flipkart_get_description(soup)}\n\nProduct Description:\n{flipkart_search.flipkart_product_description(soup)}\n\nInfo Table:\n{flipkart_search.flipkart_get_table(soup)}"
            print(final_context)
    genai.configure(api_key=random.choice(keys)) 
    print(productname)
    prompt = f'''Here is The Information you need:\n{final_context}\n\n and retrieve the details precisely and be cautious to never consider ENC as ANC, they are different.
    if you dont find relevent data for a field then try to deduce from given data or if needed give generic info like how every tws uses lithium ion battery and how sbc codec is supported by all along with some others and 
    Warranty is usually 1 year unless mentioned extra,enter sensitivity value as you seem fine, High res support is when high res codec is mentioned,Enter Battery Capacity as you seem fine according to the product or a standard plausible value but dont let it be empty, 
    charging time whatever you seem fine, charging type is type-C with some extra info if given, Microphone means Yes and how many mics ? and "Frequency Response": "20Hz-20kHz", "Codecs": "SBC, AAC" unless mentioned otherwise with other codecs ELSE 
    cosider it a No.
    design type is - in-ear, open-ear, meanwhile design means -> TWS Earbuds or wiredneckband...etc for the product: {productname}. 
    Provide the details in the given order {inp} and present them as a dictionary ONLY
    with key-value pairs where the values are strings only. 
    Do not include any text that is not explicitly asked for. '''
    response = model1.generate_content(prompt)
    print(response.text)
    res = ast.literal_eval(response.text)
    final_dict = {attributes[key].replace('name', 'value(s)'): value for key, value in res.items()}
    
    for key, value in final_dict.items():
        if key in df.columns:
            df.at[index, key] = value

    with open(log_file, mode='a',encoding="utf-8") as file:
        file.write(f"\n\nProduct Name: {productname}\n")
        for key, val in res.items():
            file.write(f"{key} : {val}\n")
    time.sleep(45)    
    try:
        df.to_excel(filexl, index=False, engine='openpyxl')
        print(f"Data for the entry {index + 1} updated in {filexl}")
    except Exception as e:
        print(f"Error writing the Excel file: {e}")
    


