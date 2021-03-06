# scrape_traveloka
Web scraper for traveloka to get hotel listings. Written in Python and using Selenium library

NOTE: 
- To use the script you need to download [__Chrome Selenium driver__](https://sites.google.com/a/chromium.org/chromedriver/downloads) first. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin. You can also use another browser driver if you want.
- You need VPN or proxy services to bypass the anti-scraping tools on the website.

Flow of the script summary:  
1. In the city loop (starts from row 47), 
  - the script type the city name from the cities list to the search box in the website.
  - Then, the script will select city option or area option based on the city name typed (in that order).
  - The script continues to the next loop.
  - If both of the options are not found, script will skip that city name and append it to the unfound_cities list.
2. The page loop (starts from row 71):
  - After the city loop, the browser get to the first page of hotel listing result.
  - Script will scrap the data from that page and add the data to the hotels dataframe.
  - Find the next button.
  - If the button is not found, means the browser get to the last page. The loop breaks, then the script goes back to the city loop.
  - If the button is found, script then click the button to get to the next page.
3. In the end of the script, the duplicates in the hotels dataframe, if found, will be dropped. Then, the dataframe will be exported to csv.

Variables to specify:
- The list of cities to search in a CSV file, the CSV name, and the CSV directory. (Row 18) 
- You also can directly define the cities list in the script.
- The CSV name and directory of the exported data. (Row 21)

Outputs hotel listings to CSV with the following information:
- Hotel name
- City
- Hotel Star
- Hotel Rating
- URL of the listing
