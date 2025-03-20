# Wedding_Venues Scraper

This Scrapy project scrapes venue details from [Wedding Spot](https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1), extracting key details like venue name, phone number, guest capacity, highlights, and address.


# Features
- Scrapes venue details including:
  - Name
  - Phone number
  - Guest capacity
  - Venue highlights
  - Address
- Supports pagination to scrape multiple pages.
- Extracts only numeric values for guest capacity.
- Cleans and structures address data properly.
- Saves data in JSON format.


# Setup Instructions

#  Install Dependencies
Ensure you have Python (3.7 or later) installed.

# Then, install Scrapy:
 pip install scrapy

# To start scraping and save data to a JSON file:
 scrapy crawl venues -o output.json

Finally, Scraped data are saved in output.json in proper format check there.