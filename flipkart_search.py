
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
            color_name = color_element.find("div", class_="V3Zflw QX54-Q E1E-3Z").get_text(strip=True).replace('\u200e', '')
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
            feature_text = feature_element.get_text(strip=True).replace('\u200e', ' ')
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
        text = span.get_text(strip=True).replace('\u200e', '')
        
        return text
    
    except Exception as e:
        return str(e)

def flipkart_product_description(soup):
    feature_description_pairs = []

    # Find the main container for the product description
    description_divs = soup.find_all("div", class_="CB-A+e w9oVFJ")
    
    for description_div in description_divs:
        # Extract the feature title
        feature_title = description_div.find("div", class_="_9GQWrZ").get_text(strip=True).replace('\u200e', '')

        # Extract the feature description (if exists)
        feature_description = description_div.find("div", class_="AoD2-N")
        if feature_description:
            feature_description_text = feature_description.get_text(strip=True).replace('\u200e', '')
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
            key = key_td.get_text(strip=True).replace('\u200e', '') if key_td else None

            # Find the value
            value_td = row.find("td", class_="Izz52n col col-9-12")
            
            # If there's a <ul> tag, get all the list items
            if value_td and value_td.find("ul"):
                value = ", ".join([li.get_text(strip=True).replace('\u200e', '') for li in value_td.find_all("li")])
            else:
                value = value_td.get_text(strip=True).replace('\u200e', '') if value_td else None

            # Add to dictionary
            if key and value:
                specs[key] = value
    ans = ""
    for key, value in specs.items():
        ans +=(f"\n{key}: {value}")
    return ans
