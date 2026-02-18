import scrapy
from urllib.parse import quote_plus
from scrapy.http import Response

class TestMapsSpider(scrapy.Spider):
    name = "test_maps"
    
    categories = [
        "Cooperative bank", "bank", "After school program", "Art school", "Bartending school", 
        "Boarding school", "Business school", "Childrens library", "Chinese language school", 
        "College", "Combined primary and secondary school", "Community college", 
        "Computer training school", "Dance school", "Drawing lessons", 
        "Drivers license training school", "Driving school", "Educational institution", 
        "Education center", "Elementary school", "English language school", "Farm school", 
        "General education school", "German language school", "Government school", 
        "Higher secondary school", "High school", "International school", "Language school", 
        "Library", "Middle school", "Montessori preschool", "Montessori school", "Music school", 
        "Preschool", "Primary school", "Private educational institution", "School center", 
        "School house", "School supply store", "Secondary school", "Special education school", 
        "Taekwondo school", "Technical school", "Training center", "University", 
        "Vocational school", "Acupuncture clinic", "Animal hospital", "Ayurvedic clinic", 
        "Blood bank", "Cancer treatment center", "Child health care center", 
        "Community health center", "Dental clinic", "Dentist", "Faculty of pharmacy", 
        "General hospital", "Government hospital", "Health and beauty shop", "Health consultant", 
        "Health food store", "Health insurance agency", "Home health care service", 
        "Hospital department", "Hospital equipment and supplies", 
        "Hospitality and tourism school", "Hospital", "Medical clinic", "Mental health service", 
        "Naturopathic practitioner", "Occupational health service", "Orthopedic clinic", 
        "Pain management physician", "Pharmacy", "Physical therapy clinic", "Private hospital", 
        "Public library", "Savings bank", "Self service health station", "Software company", 
        "Ticket office", "Tour operator", "Traffic police station", "Travel agency", 
        "Veterinarian", "Veterinary pharmacy", "Adventure sports center", "Athletic park", 
        "Banquet hall", "Beauty salon", "Beauty school", "Boxing gym", "Business park", 
        "City government office", "Community garden", "Corporate office", "District office", 
        "Federal government office", "Financial institution", "Food bank", "Garden", 
        "Government economic program", "Government", "Government office", "Gym", 
        "Local government office", "Memorial park", "Military school", "Mobile home park", 
        "Muay Thai boxing gym", "Office", "Office supply store", "Park", "Park _ ride", 
        "Photography studio", "Plaza", "Political party office", "Post office", 
        "State government office", "Water park", "Buddhist temple", "Hindu temple", 
        "Tourist attraction"
    ]

    def start_requests(self):
        for category in self.categories:
            # Clean category name (e.g. replace underscores or extra spaces)
            query = f"{category.replace('_', ' ').strip()} in Kathmandu valley"
            url = f"https://www.google.com/maps/search/{quote_plus(query)}"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "zyte_api_automap": {
                        "browserHtml": True,
                        "geolocation": "NP"  # Set geolocation to Nepal
                    },
                    "category": category
                }
            )

    def parse(self, response: Response):
        # This is a placeholder for parsing logic.
        # Google Maps structure is complex and dynamic.
        # Often data is in window.APP_INITIALIZATION_STATE or similar JSON blobs within the HTML,
        # or rendered in specific div classes.
        
        # Taking a simple approach to extract visible text or links for now.
        # Real Google Maps scraping usually requires more specific selectors or
        # using Zyte's "google_maps" specialized extraction (if available on your plan).

        self.logger.info(f"Scraped {response.url}")
        
        # Example: Extracting titles (selectors need to be verified against current Google Maps HTML)
        # Note: Selectors on Google Maps change frequently.
        for result in response.css('div[role="article"]'):
            yield {
                "category": response.meta["category"],
                "title": result.css('div.fontHeadlineSmall::text').get(),
                "link": result.css('a::attr(href)').get(),
            }
