# ArcGIS Product Codes Updater

This script automates the process of updating the product codes list by scraping the Esri Knowledge Base article for the latest ArcGIS product uninstall codes.

## Overview

The script:
1. Fetches or uses cached content from the Esri KB article: https://support.esri.com/en-us/knowledge-base/how-to-silently-uninstall-arcgis-products-000013200
2. Parses the HTML to extract product names and GUIDs organized by ArcGIS version
3. Updates the product codes files in the `product-codes/` directory with new versions

## Usage

### Prerequisites

- Python 3.11 or higher
- `uv` package manager

### Running the Script

```bash
# Run with uv (recommended - automatically handles dependencies)
cd SysAdmin/deployment
uv run update_product_codes.py

# Or run with python directly after installing dependencies
pip install requests beautifulsoup4
python update_product_codes.py
```

### How It Works

1. **Caching**: The script caches the HTML content in `esri_kb.html` to avoid repeated requests
2. **Parsing**: Uses BeautifulSoup to parse the HTML and extract version information
3. **Updates**: Adds new versions to the appropriate product files:
   - `main.txt` - Contains all products organized by ArcGIS version
   - `datastore.txt` - Contains only ArcGIS Data Store product codes
   - `server.txt` - Contains only ArcGIS Server product codes  
   - `web-adapter.txt` - Contains only Web Adaptor product codes

### Output

```
Reading from cache: d:\code\YG\arcplus\SysAdmin\deployment\esri_kb.html
Found 32 versions.
Updating d:\code\YG\arcplus\SysAdmin\deployment\product-codes\main.txt...
  No new versions found for main.txt.
Updating d:\code\YG\arcplus\SysAdmin\deployment\product-codes\datastore.txt...
  No new versions found for datastore.txt.
Updating d:\code\YG\arcplus\SysAdmin\deployment\product-codes\server.txt...
  No new versions found for server.txt.
Updating d:\code\YG\arcplus\SysAdmin\deployment\product-codes\web-adapter.txt...
  No new versions found for web-adapter.txt.
```

## File Formats

### main.txt Format (Suite-centric)
```
From "How To: Silently uninstall ArcGIS products"
https://support.esri.com/en-us/knowledge-base/how-to-silently-uninstall-arcgis-products-000013200
2024-11-27

ArcGIS 12.0
ArcGIS Data Store {E62C9D19-53FE-45C2-B9C5-C86C7C703B8F}
ArcGIS Mission Server {16AF7BDF-E692-4490-A3F6-1F41812CF155}
ArcGIS Notebook Server {42B859BB-95D1-4778-B2A7-991F3DD812E1}
...
```

### Product-specific files format
```
ArcGIS Enterprise Server Products
2024-11-27

ArcGIS Server
https://enterprise.arcgis.com/en/server/latest/install/windows/uninstall-arcgis-server.htm

11.2 {0F6C2D4F-9D41-4D25-A8AF-51E328D7CD8F}
10.9.1 {E4A5FD24-5C61-4846-B084-C7AD4BB1CF19}
...
```

## Features

- **PEP 723 Style**: Uses inline script metadata for dependencies
- **Caching**: Avoids repeated requests to Esri's website
- **Duplicate Prevention**: Only adds new versions not already present
- **Version Sorting**: Maintains proper version ordering (newest first)
- **Multiple Formats**: Handles both suite-centric and product-centric file formats

## Dependencies

- `requests` - For fetching web content
- `beautifulsoup4` - For parsing HTML

These are automatically handled when using `uv run`.

## Script Location

`SysAdmin/deployment/update_product_codes.py`

## Related Files

- `SysAdmin/deployment/esri_kb.html` - Cached HTML content
- `SysAdmin/deployment/product-codes/` - Directory containing product code files
- `SysAdmin/deployment/uninstall-ALL-ArcGIS-products.bat` - Main uninstall script that uses these product codes
