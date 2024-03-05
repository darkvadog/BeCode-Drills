from src.scraper import WikipediaScraper 

if __name__ == "__main__":
    # Instantiate scraper with correct URL
    scraper = WikipediaScraper("https://country-leaders.onrender.com")

    # Retrieve countries
    countries = scraper.get_countries()
    print(countries)
    
    # Retrieve leaders per country
    for country in countries:
        scraper.get_leaders(country)

    # Add the first paragraph for each leader
    for country, leaders in scraper.leaders_data.items():
        for leader in leaders:
            leader["first_paragraph"] = scraper.get_first_paragraph(leader["wikipedia_url"])

    # Save data structure to JSON file
    scraper.to_json_file("wikipedia_leaders.json")

    # Show string representation of the WikipediaScraper
    print(str(scraper))