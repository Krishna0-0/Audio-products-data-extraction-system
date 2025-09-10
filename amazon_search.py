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
