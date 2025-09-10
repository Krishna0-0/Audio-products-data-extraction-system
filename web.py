import os
from dotenv import load_dotenv
import requests
import pandas as pd
import random
from bs4 import BeautifulSoup
import google.generativeai as genai
load_dotenv()



# Secure configuration
keys = os.getenv('GEMINI_API_KEYS', '').split(',')
if not keys or keys == ['']:
    raise ValueError("GEMINI_API_KEYS environment variable not set")

model1 = genai.GenerativeModel('gemini-1.5-pro', generation_config={"response_mime_type": "application/json"})
genai.configure(api_key=random.choice(keys))

api_key = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')
search_query = 'Boult Audio W20'  

if not api_key or not search_engine_id:
    raise ValueError("Google API credentials not found in environment variables")

url = 'https://www.googleapis.com/customsearch/v1'

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
            'key': api_key,
            'filter': 1,
            'gl': 'IN',
            'hl': 'en',
            # 'exactTerms': 'realme air buds 6',
            'cx': search_engine_id,
            'num': 4,
        }
    else :
        params = {
            'q': query,
            'key': api_key,
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
    try:
        print(response)
        return response.json()['items']
    except:
        print(response.status_code)

def amazon_get_title(soup):
	try:
		title = soup.find("span", attrs={"id":'productTitle'})
		title_string = title.string.strip()
	except AttributeError:
		title_string = ""	
	return title_string

def amazon_get_box_cont(soup):
    try:
        # Locate the div that contains the "What's in the box?" information
        box_contents = soup.find("div", attrs={'id': 'postPurchaseWhatsInTheBox_MP_feature_div'})
        
        # Find all the span elements that contain the list items
        items = box_contents.find_all("span", class_="a-list-item")
        
        # Extract the text from each span and strip any extra whitespace
        box_items_text = [item.get_text(strip=True) for item in items]
        
        # Join the items into a single string, separated by new lines
        box_contents_text = "\n".join(box_items_text)
    
    except AttributeError:
        box_contents_text = ""
    
    return box_contents_text

def amazon_get_about(soup):
    try:
        # Locate the div that contains the feature bullets
        available = soup.find("div", attrs={'id': 'feature-bullets'})
        
        # Find all the span elements that contain the bullet points
        bullet_points = available.find_all("span", class_="a-list-item")
        
        # Extract the text from each span and strip any extra whitespace
        bullet_points_text = [point.get_text(strip=True) for point in bullet_points]
        
        # Join the bullet points into a single string, separated by new lines
        available_text = "\n".join(bullet_points_text)
    
    except AttributeError:
        available_text = ""
    
    return available_text

def amazon_get_manufacturer_info(soup):
    try:
        manufacturer_div = soup.find("div", attrs={'class': 'aplus-v2 desktop celwidget'})
        
        manufacturer_text = manufacturer_div.get_text(separator=' ', strip=True)
    
    except AttributeError:
        manufacturer_text = ""
    
    return manufacturer_text

def amazon_get_table_data(soup):
    try:
        # Locate the table that contains the technical specifications
        table = soup.find("table", attrs={'id': 'productDetails_techSpec_section_1'})
        
        # Initialize a dictionary to store the data
        table_data = {}
        
        # Find all table rows
        rows = table.find_all("tr")
        
        for row in rows:
            # For each row, get the header and value
            header = row.find("th").get_text(strip=True).replace('\u200e', '')
            value = row.find("td").get_text(strip=True).replace('\u200e', '')
            
            # Store the header-value pair in the dictionary
            table_data[header] = value
        
        # Return the dictionary with formatted key-value pairs
        ans = ""
        for key, value in table_data.items():
            ans +=(f"\n{key}: {value}")
        return ans
    except Exception as e:
        return str(e)

def flipkart_get_title(soup):
    try:
        # Locate the span with the specific class name
        span = soup.find("span", class_="VU-ZEz")
        
        # Get the text and clean up any unwanted characters or spaces
        text = span.get_text(strip=True).replace('\u00a0', ' ')
        
        return text
    
    except Exception as e:
        return str(e)

def flipkart_get_color(soup):
    try:
        # Find all the 'li' elements that contain the color options
        color_elements = soup.find_all("li", class_="aJWdJI")
        
        # Initialize a list to store the color names
        colors = []
        
        # Loop through each 'li' element and extract the color name
        for color_element in color_elements:
            color_name = color_element.find("div", class_="V3Zflw QX54-Q E1E-3Z").get_text(strip=True)
            colors.append(color_name)
        
        return colors
    
    except Exception as e:
        return str(e)
    
def flipkart_get_about(soup):
    try:
        # Find all 'li' elements with the specific class that contains the feature details
        feature_elements = soup.find_all("li", class_="_7eSDEz")
        
        # Initialize a list to store the features
        features = []
        
        # Loop through each 'li' element and extract the feature text
        for feature_element in feature_elements:
            feature_text = feature_element.get_text(strip=True)
            features.append(feature_text)
        ans = ""
        for item in features:
            if ':' in item:
                key, value = item.split(':', 1)
                ans+=(f"{key}: {value}\n")
            else:
                ans+=(f"Feature: {item}\n")
        return ans
    except Exception as e:
        return str(e)

def flipkart_get_description(soup):
    try:
        # Locate the span with the specific class name
        span = soup.find("div", class_="yN+eNk w9jEaj")
        
        # Get the text and clean up any unwanted characters or spaces
        text = span.get_text(strip=True).replace('\u00a0', ' ')
        
        return text
    
    except Exception as e:
        return str(e)

def flipkart_product_description(soup):
    feature_description_pairs = []

    # Find the main container for the product description
    description_divs = soup.find_all("div", class_="CB-A+e w9oVFJ")
    
    for description_div in description_divs:
        # Extract the feature title
        feature_title = description_div.find("div", class_="_9GQWrZ").get_text(strip=True)

        # Extract the feature description (if exists)
        feature_description = description_div.find("div", class_="AoD2-N")
        if feature_description:
            feature_description_text = feature_description.get_text(strip=True)
        else:
            feature_description_text = "No description available"
        
        # Append the title-description pair to the list
        feature_description_pairs.append((feature_title, feature_description_text))

    return feature_description_pairs

def flipkart_get_table(soup):
    # Find all tables with the class "_0ZhAN9"
    tables = soup.find_all("table", class_="_0ZhAN9")

    # Dictionary to store the extracted data
    specs = {}

    # Iterate through each table
    for table in tables:
        # Find all rows within the current table
        rows = table.find_all("tr", class_="WJdYP6 row")

        for row in rows:
            # Find the key
            key_td = row.find("td", class_="+fFi1w col col-3-12")
            key = key_td.get_text(strip=True) if key_td else None

            # Find the value
            value_td = row.find("td", class_="Izz52n col col-9-12")
            
            # If there's a <ul> tag, get all the list items
            if value_td and value_td.find("ul"):
                value = ", ".join([li.get_text(strip=True) for li in value_td.find_all("li")])
            else:
                value = value_td.get_text(strip=True) if value_td else None

            # Add to dictionary
            if key and value:
                specs[key] = value
    ans = ""
    for key, value in specs.items():
        ans +=(f"\n{key}: {value}")
    return ans

# sites = ['flipkart.com','amazon.in','smartprix.com','91mobiles.com','web']
sites = ['amazon.in','flipkart.com']

filexl = os.getenv('EXCEL_FILE', 'data1.xlsx')
log_file = os.getenv('LOG_FILE', 'logfile.txt')
df = pd.read_excel(filexl)
# Get the first row (index 0) as a dictionary
first_row = df.iloc[0].to_dict()
start = int(input("Start Index: "))
# for index, row in df.iloc[start:len(df.index)].iterrows():
#     result = []
#     final_context = ""
#     productname = str(row['Name'])
#     for site in sites:
#         print(site)
#         print(productname)
#         res = search_on_site(site, productname)
#         for item in res:
#             result.append(item['link'])
#     print(result)

for i in range(5):
    result = []
    for site in sites:
        res = search_on_site(site, search_query)
        for item in res:
            result.append(item['link'])
    print(result)
# inp = ['Earbuds Brand', 'Model', 'Availability', 'Warranty', 'Box Contents', 'Design', 'Design Type', 'Colour(s)', 'Bluetooth', 'Microphone', 'Bluetooth Range', 'controls', 'ANC', 'ANC Intensity', 'Features', 'Driver Size', 'Driver Type', 'Sensitivity', 'Frequency Response', 'Codecs', 'Hi-Res Support', 'Battery Capacity', 'Battery Type', 'Battery Life', 'Charging Time', 'Charging type', 'Weight', 'Dimensions', 'Water Resistant', 'Price']
# final_context = ""
# for url in result:
#     webpage = requests.get(url, headers=custom_headers)
#     soup = BeautifulSoup(webpage.content, "lxml")
#     if('amazon' in url) :
#         final_context+=f"\nStart of New context please check if its the same product or some other variant by matching from Product's title(if different in any sense then skip this context) \nProduct Title :\n{amazon_get_title(soup)} \n\nBox Content:\n{amazon_get_box_cont(soup)} \n\nAbout Product:\n{amazon_get_about(soup)}\n\nMore info:\n{amazon_get_manufacturer_info(soup)}\n\nInfo Table:\n{amazon_get_table_data(soup)}\n\n\n"
#     else :
#         final_context+= f"\nStart of New context please check if its the same product or some other variant by matching from Product's title(if different in any sense then skip this context) \nProduct Title :\n{flipkart_get_title(soup)}\n\nColor(s):\n{flipkart_get_color(soup)}\n\nAbout Product:\n{flipkart_get_about(soup)}\n\nSome Description:\n{flipkart_get_description(soup)}\n\nProduct Description:\n{flipkart_product_description(soup)}\n\nInfo Table:\n{flipkart_get_table(soup)}"

# print(final_context)

# response = model1.generate_content(f'''Here is The Information you need:\n{final_context}\n\n and retrieve the details precisely 
# if you dont find relevent data for a field then try to deduce from given data or if needed give generic info like how every tws uses lithium ion battery and how sbc and some basic codecs are supported by all only if possible ELSE cosider it a No instead of hallucinating!! 
# design type is - in-ear, open-ear, meanwhile design means -> TWS Earbuds or wiredneckband...etc for the product: {search_query}. 
# Provide the details in the given order {inp} and present them as a dictionary ONLY
# with key-value pairs where the values are strings only. 
# Do not include any text that is not explicitly asked for. ''')
# print(response.text)