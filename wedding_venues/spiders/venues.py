import scrapy
import logging
import re  

logging.basicConfig(level=logging.DEBUG)

class VenuesSpider(scrapy.Spider):
    name = "venues"
    start_urls = [
        'https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1'
    ]

    def parse(self, response):
        logging.debug(f"Parsing page: {response.url}")

        # Extract venue detail URLs
        venue_links = response.css("a[href*='/venue/']::attr(href)").getall()
        for venue_link in venue_links:
            detail_url = response.urljoin(venue_link)
            logging.debug(f"Found venue: {detail_url}")
            yield scrapy.Request(detail_url, callback=self.parse_venue)

        # Extract total number of pages from pagination
        page_numbers = response.css("button[aria-current='false']::text").getall()
        if page_numbers:
            last_page_number = int(page_numbers[-1])  
        else:
            last_page_number = 1 
        # Extract the current page number
        current_page = response.css("button[aria-current='true']::text").get()
        if current_page:
            current_page_number = int(current_page)
        else:
            current_page_number = 1 

        # If there is another page, follow it
        if current_page_number < last_page_number:
            next_page_number = current_page_number + 1
            next_page_url = self.generate_next_page_url(response.url, next_page_number)
            logging.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)

    def generate_next_page_url(self, current_url, next_page_number):
        """Generate the next page URL by replacing the 'sr=' parameter."""
        import urllib.parse

        parsed_url = urllib.parse.urlparse(current_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Update page number
        query_params["sr"] = [str(next_page_number)]

        # Reconstruct URL
        updated_query = urllib.parse.urlencode(query_params, doseq=True)
        next_page_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{updated_query}"

        return next_page_url

    def parse_venue(self, response):
        logging.debug(f"Parsing venue detail page: {response.url}")

        venue_name = response.css("h1::text").get()
        phone = response.css("a[href^='tel:']::attr(href)").get()
        if phone:
            phone = phone.replace('tel:', '').strip()

        venue_highlights = response.css(".header_venueHighlights__zdWMf *::text").getall()
        venue_highlights = [highlight.strip() for highlight in venue_highlights if highlight.strip()]

        
        guest_capacity_text = response.css(".ShortInfo_capacity__1jfEs p *::text, .ShortInfo_capacity__1jfEs p::text").getall()
        guest_capacity_text = "".join(guest_capacity_text).strip()
        capacity_number = "".join(re.findall(r"\d+", guest_capacity_text))
        
        address_part1 = response.css(".header_socialLink__62cYD ::text").get()
        address_part2 = response.css(".location p:nth-of-type(2)::text").get()
        address = None
        if address_part1 and address_part2:
            address = f"{address_part1.strip()} {address_part2.strip()}"
        elif address_part1:
            address = address_part1.strip()
        elif address_part2:
            address = address_part2.strip()

        logging.debug(f"Extracted venue: {venue_name}, Phone: {phone}, Highlights: {venue_highlights}, Guest Capacity: {capacity_number}, Address: {address}")

        yield {
            'url': response.url,
            'venue_name': venue_name,
            'phone': phone,
            'venue_highlights': venue_highlights,
            'guest_capacity': capacity_number,
            'address': address,
        }
