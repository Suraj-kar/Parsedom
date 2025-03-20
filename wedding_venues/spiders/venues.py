import scrapy
import logging
import re  # For extracting guest capacity numbers

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

class VenuesSpider(scrapy.Spider):
    name = "venues"
    start_urls = [
        'https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1'
    ]

    def parse(self, response):
        logging.debug(f"Parsing page: {response.url}")
        
        # Extract venue detail URLs using CSS
        for venue_link in response.css("a[href*='/venue/']::attr(href)").getall():
            detail_url = response.urljoin(venue_link)  # Convert relative URL to absolute URL
            logging.debug(f"Found detail URL: {detail_url}")
            yield scrapy.Request(detail_url, callback=self.parse_venue)

        # Handle pagination using CSS
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            logging.debug(f"Found next page: {next_page}")
            yield response.follow(next_page, self.parse)

    def parse_venue(self, response):
        logging.debug(f"Parsing venue detail page: {response.url}")

        # Extract venue details using CSS
        venue_name = response.css("h1::text").get()

        # Extract phone number
        phone = response.css("a[href^='tel:']::attr(href)").get()
        if phone:
            phone = phone.replace('tel:', '').strip()

        # Extract venue highlights using CSS
        venue_highlights = response.css(".VenueHighlights--label::text").getall()
        venue_highlights = [highlight.strip() for highlight in venue_highlights if highlight.strip()]

        # Extract Guest Capacity using CSS
        guest_capacity_text = response.css(".guest-capacity .value::text").get()
        guest_capacity = None
        if guest_capacity_text:
            match = re.search(r'\d+', guest_capacity_text)
            if match:
                guest_capacity = match.group()

        # Extract Address using CSS
        address_part1 = response.css(".location p:nth-of-type(1)::text").get()
        address_part2 = response.css(".location p:nth-of-type(2)::text").get()
        address = None
        if address_part1 and address_part2:
            address = f"{address_part1.strip()} {address_part2.strip()}"
        elif address_part1:
            address = address_part1.strip()
        elif address_part2:
            address = address_part2.strip()

        # Log extracted details for debugging
        logging.debug(f"Extracted venue: {venue_name}, Phone: {phone}, Highlights: {venue_highlights}, Guest Capacity: {guest_capacity}, Address: {address}")

        # Yield the extracted data
        yield {
            'url': response.url,
            'venue_name': venue_name,
            'phone': phone,
            'venue_highlights': venue_highlights,
            'guest_capacity': guest_capacity,
            'address': address,
        }
