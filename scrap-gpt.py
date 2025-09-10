import re
from bs4 import BeautifulSoup
import openai
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


google_search_api = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

if not google_search_api or not search_engine_id:
    raise ValueError("Google API credentials not found")
if not openai.api_key:
    raise ValueError("OpenAI API key not found")

search_query = 'Realme buds Air 6'
url = 'https://www.googleapis.com/customsearch/v1'
sites = ['flipkart.com','amazon.in','web']

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
    'Cookie': os.getenv('AMAZON_COOKIE', ''),
    "X-Amzn-Trace-Id": "Root=1-66ba761c-23a18c3915856d8c122d2adb",
}

def search_on_site(site, query):
    if(site == 'web'):

        params = {
            'q': query,
            'key': google_search_api,
            'filter': 1,
            'gl': 'IN',
            'hl': 'en',
            # 'exactTerms': 'realme air buds 6',
            'cx': search_engine_id,
            'num': 3,
        }
    else :
        params = {
            'q': query,
            'key': google_search_api,
            'filter': 1,
            'gl': 'IN',
            'hl': 'en',
            # 'exactTerms': 'realme air buds 6',
            'cx': search_engine_id,
            # 'fileType' : "pdf",
            'siteSearch': site,  # Restrict search to a specific site
            'num': 2,
        }
    response = requests.get(url, params=params)
    return response.json()['items']
final_websites = []
for site in sites:
    res = search_on_site(site, search_query)
    for item in res:
        final_websites.append(item['link'])

def scrape_website(url, file_name):
    try:
        response = requests.get(url,headers=custom_headers)
        response.raise_for_status()  # Ensure we notice bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the webpage
        text = soup.get_text(separator=' ', strip=True)
        
        # Save the text to a file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Content from {url} saved to {file_name}")
        return text
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return None
    
for i, url in enumerate(final_websites):
    file_name = f"website_content_{i+1}.txt"
    scrape_website(url, file_name)

prod = "realme air buds 6"
inp = ['Earbuds Brand', 'Model', 'Availability', 'Warranty', 'Box Contents', 'Design', 'Design Type', 'Colour(s)', 'Bluetooth', 'Microphone', 'Bluetooth Range', 'controls', 'ANC', 'ANC Intensity', 'Features', 'Driver Size', 'Driver Type', 'Sensitivity', 'Frequency Response', 'Codecs', 'Hi-Res Support', 'Battery Capacity', 'Battery Type', 'Battery Life', 'Charging Time', 'Charging type', 'Weight', 'Dimensions', 'Water Resistant', 'Price']
def summarize_with_chatgpt(text, model="gpt-4o"):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Web Scraper but the site doesnt necessarily refers to the product that I need searching for so be mindful and skip incase its a different product"},
            {"role": "user", "content": f'''Search these websites and retrieve the details precisely for the given product if the website is for exact prodcut mentioned {final_websites}  
    if you dont find data on ANC(Active Noise Cancelling) on any website then consider it a No ! be cautious to never consider ENC !!! or anything else, NO RUBBISH DATA especially for ANC and driver size and 
    design type- in-ear, open-ear, meanwhile design means -> TWS Earbuds or wiredneckband...etc for the product: {prod}. 
    Provide the details in the given order {inp} and the also price without the inr sign only and present them as a dictionary ONLY
    with key-value pairs where the values are strings only. Check the values 
    twice especially the driver size and ANC  for accuracy and Bring as much as possible data. 
    Do not include any text that is not explicitly asked for. '''}
        ],
        stream = True,
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
# print(summarize_with_chatgpt(final_websites[0]))