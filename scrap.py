import re
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

if not api_key or not search_engine_id:
    raise ValueError("Google API credentials not found in environment variables")

search_query = 'Realme buds Air 6'
url = 'https://www.googleapis.com/customsearch/v1'

def search_on_site(site, query):
    params = {
        'q': query,
        'key': api_key,
        'filter': 1,
        'gl': 'IN',
        'hl': 'en',
        # 'exactTerms': 'realme air buds 6',
        'cx': search_engine_id,
        'siteSearch': site,  # Restrict search to a specific site
        'num': 2,
    }
    response = requests.get(url, params=params)
    return response.json()

sites = ['flipkart.com','amazon.in','smartprix.com','91mobiles.com']
# Search on Flipkart
for site in sites:

    res = search_on_site(site, search_query)
    print("Results:")
    if 'items' in res:
        for item in res['items']:
            print(item['link'])

# General Web Search
params = {
    'q': search_query,
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

print("\nGeneral Web Results:")
if 'items' in general_results:
    for item in general_results['items']:
        print(item['link'])
