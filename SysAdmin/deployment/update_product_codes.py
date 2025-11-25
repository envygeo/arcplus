# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
# ]
# ///

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

URL = "https://support.esri.com/en-us/knowledge-base/how-to-silently-uninstall-arcgis-products-000013200"
SCRIPT_DIR = Path(__file__).parent
PRODUCT_CODES_DIR = SCRIPT_DIR / "product-codes"

def fetch_and_parse_kb() -> Dict[str, List[str]]:
    """
    Fetches the Esri KB article and parses it into a dictionary.
    Key: Suite Version (e.g., "ArcGIS 11.5")
    Value: List of product strings (e.g., "ArcGIS Data Store {GUID}")
    """
    cache_file = SCRIPT_DIR / "esri_kb.html"
    content = ""
    
    if cache_file.exists():
        print(f"Reading from cache: {cache_file}")
        with open(cache_file, "rb") as f:
            content = f.read()
    else:
        print(f"Fetching {URL}...")
        try:
            response = requests.get(URL, timeout=30)
            response.raise_for_status()
            content = response.content
            with open(cache_file, "wb") as f:
                f.write(content)
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            sys.exit(1)

    soup = BeautifulSoup(content, "html.parser")
    
    # The structure observed is typically nested lists or headers followed by lists.
    # Based on visual inspection:
    # <ul>
    #   <li>ArcGIS 11.5
    #       <ul>
    #           <li>ArcGIS Data Store {GUID}</li>
    #           ...
    #       </ul>
    #   </li>
    # </ul>
    
    data = {}
    
    # Find all list items that might be version headers
    # We look for list items that contain text matching "ArcGIS \d+(\.\d+)*"
    # and have a nested list.
    
    # Strategy: Find the main content area first to avoid nav menus
    # Try to find where "ArcGIS 12.0" is to locate the content container
    target_text = soup.find(string=re.compile("ArcGIS 12.0"))
    if target_text:
        # Walk up to find a reasonable container
        content_div = target_text.parent.find_parent("div")
    else:
        content_div = soup.find("div", class_="article-content") or soup.find("div", class_="master-main") or soup

    # Alternative parsing strategy:
    # Look for "ArcGIS X.Y" text, then look for the next UL sibling.
    # This handles cases where the header is a <p> or <h3> and the list is a sibling <ul>.
    
    # Find all elements that contain "ArcGIS" text
    for element in content_div.find_all(["p", "h2", "h3", "h4", "li", "strong", "b", "span"]):
        text = element.get_text(strip=True)
        # Clean up text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Match "ArcGIS X.Y" or "ArcGIS X.Y.Z" or "ArcGIS 10.x"
        # Ensure it's the *whole* text or close to it (to avoid matching "ArcGIS 10.5 is great")
        version_match = re.match(r"^ArcGIS\s+(\d+(\.\d+)*(\.x)?)$", text, re.IGNORECASE)
        
        if version_match:
            version_key = version_match.group(0)
            # print(f"Found version header: {version_key} in <{element.name}>")
            
            products = []
            
            # Case 1: The list is nested inside this element (e.g. <li>Header <ul>...</ul></li>)
            nested_list = element.find(["ul", "ol"])
            
            # Case 2: The list is the next sibling (e.g. <p>Header</p> <ul>...</ul>)
            if not nested_list:
                # Look at next siblings
                curr = element
                while curr:
                    curr = curr.next_sibling
                    if not curr: break
                    
                    if curr.name in ["ul", "ol"]:
                        nested_list = curr
                        break
                    
                    # Case 3: Products are text nodes or <br> siblings (e.g. <b>Header</b><br>Product 1<br>Product 2)
                    if isinstance(curr, str) or curr.name == 'br':
                        text_content = curr if isinstance(curr, str) else ""
                        if not text_content and curr.name != 'br':
                             text_content = curr.get_text(strip=True)
                        
                        if "{" in text_content and "}" in text_content:
                             # Normalize whitespace
                            product_text = re.sub(r'\s+', ' ', text_content).strip()
                            if product_text:
                                products.append(product_text)
                        continue

                    if curr.name in ["p", "h2", "h3", "h4", "div", "li", "strong", "b"]:
                        # Stop if we hit another block element or header-like element
                        # But be careful not to stop on <br> or simple formatting
                        break
            
            if nested_list:
                for product_li in nested_list.find_all("li"):
                    product_text = product_li.get_text(" ", strip=True)
                    # Check if it looks like a product code line: "Name {GUID}"
                    if "{" in product_text and "}" in product_text:
                        # Normalize whitespace
                        product_text = re.sub(r'\s+', ' ', product_text).strip()
                        products.append(product_text)
            
            if products:
                data[version_key] = products
                
    return data

def update_main_txt(scraped_data: Dict[str, List[str]]):
    """
    Updates product-codes/main.txt with new versions found in scraped_data.
    """
    main_txt_path = PRODUCT_CODES_DIR / "main.txt"
    if not main_txt_path.exists():
        print(f"Warning: {main_txt_path} not found. Skipping.")
        return

    print(f"Updating {main_txt_path}...")
    
    with open(main_txt_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Parse existing versions from main.txt to avoid duplicates
    # We look for lines starting with "ArcGIS \d"
    existing_versions = set(re.findall(r"^ArcGIS\s+\d+(?:\.\d+)*(?:\.x)?", content, re.MULTILINE))
    
    new_content_blocks = []
    
    # Sort scraped versions descending (assuming semantic versioning in the key string works roughly okay for "ArcGIS X.Y")
    # We need a custom sort key to handle version numbers correctly
    def version_sort_key(key):
        # Extract version numbers: "ArcGIS 11.5" -> [11, 5]
        match = re.search(r"(\d+(?:\.\d+)*)", key)
        if match:
            return [int(x) for x in match.group(1).split(".")]
        return [0]

    sorted_keys = sorted(scraped_data.keys(), key=version_sort_key, reverse=True)
    
    for version_key in sorted_keys:
        if version_key not in existing_versions:
            print(f"  Adding new version: {version_key}")
            block = f"{version_key}\n"
            for product in scraped_data[version_key]:
                block += f"{product}\n"
            block += "\n"
            new_content_blocks.append(block)
            
    if not new_content_blocks:
        print("  No new versions found for main.txt.")
        return

    # Insert new blocks after the header
    # Header is assumed to end after the date or the first blank line
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            insert_idx = i + 1
            break
            
    # If we couldn't find a blank line, just insert at top (after potential comments)
    if insert_idx == 0 and len(lines) > 3:
        insert_idx = 4 # Arbitrary skip of header lines
        
    final_content = "".join(lines[:insert_idx]) + "".join(new_content_blocks) + "".join(lines[insert_idx:])
    
    with open(main_txt_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("  main.txt updated.")

def update_product_file(filename: str, product_pattern: str, scraped_data: Dict[str, List[str]]):
    """
    Updates a specific product file (e.g., datastore.txt) with new versions.
    """
    file_path = PRODUCT_CODES_DIR / filename
    if not file_path.exists():
        print(f"Warning: {file_path} not found. Skipping.")
        return

    print(f"Updating {file_path}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Parse existing versions in this file
    # Format is typically "Version {GUID}" e.g., "11.4 {GUID}"
    existing_versions = set()
    for line in content.splitlines():
        match = re.match(r"^(\d+(?:\.\d+)*)\s+\{", line.strip())
        if match:
            existing_versions.add(match.group(1))
            
    new_lines = []
    
    # Sort versions descending
    def version_sort_key(key):
        match = re.search(r"(\d+(?:\.\d+)*)", key)
        if match:
            return [int(x) for x in match.group(1).split(".")]
        return [0]

    sorted_keys = sorted(scraped_data.keys(), key=version_sort_key, reverse=True)
    
    for version_key in sorted_keys:
        # Extract version number from "ArcGIS 11.5" -> "11.5"
        version_num_match = re.search(r"(\d+(?:\.\d+)*)", version_key)
        if not version_num_match:
            continue
        version_num = version_num_match.group(1)
        
        if version_num in existing_versions:
            continue
            
        # Find the specific product in this version's list
        found_product = None
        for product_str in scraped_data[version_key]:
            if re.search(product_pattern, product_str, re.IGNORECASE):
                found_product = product_str
                break
        
        if found_product:
            # Extract GUID
            guid_match = re.search(r"(\{[-0-9A-F]+\})", found_product, re.IGNORECASE)
            if guid_match:
                guid = guid_match.group(1)
                print(f"  Adding {version_num} for {filename}")
                new_lines.append(f"{version_num} {guid}\n")
                
    if not new_lines:
        print(f"  No new versions found for {filename}.")
        return

    # Insert new lines after header
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            insert_idx = i + 1
            break
            
    final_content = "".join(lines[:insert_idx]) + "".join(new_lines) + "".join(lines[insert_idx:])
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"  {filename} updated.")

def main():
    if not PRODUCT_CODES_DIR.exists():
        print(f"Error: Directory {PRODUCT_CODES_DIR} does not exist.")
        sys.exit(1)
        
    data = fetch_and_parse_kb()
    
    if not data:
        print("No data found or parsing failed.")
        return
        
    print(f"Found {len(data)} versions.")
    
    update_main_txt(data)
    update_product_file("datastore.txt", r"Data Store", data)
    update_product_file("server.txt", r"ArcGIS Server\s+\{", data) # Be specific to avoid Mission Server etc
    update_product_file("web-adapter.txt", r"Web Adaptor", data)

if __name__ == "__main__":
    main()