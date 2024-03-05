import time
import json
import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


class MaxRetriesExceeded(Exception):
    def __init__(self, message="You exceeded the number of possible retries.") -> None:
        self.message = message
        super().__init__(self.message)


class WikipediaScraper:
    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.cookies_endpoint: str = self.base_url + "/cookie"
        self.cookies = self.refresh_cookie()
        self.country_endpoint: str = self.base_url + "/countries"
        self.leaders_endpoint: str = self.base_url + "/leaders"
        self.leaders_data: dict = {}

    def __str__(self) -> str:
        """
        Function that gives a string representation of the WikipediaScraper.

        :return: A str that tells you how many countries the scraper retrieved 
            information for, and how many leaders in each country.
        """  
        text = f"My WikipediaScraper has information on leaders from {len(self.leaders_data.keys())} countries, scraped from URL {self.base_url}."
        for country in self.leaders_data.keys():
            text += f"\nCountry {country} has {len(self.leaders_data[country])} leaders."

        return text

    def refresh_cookie(self) -> object:
        """
        Function that will retrieve the cookies from the base url.

        :param cookie: An Object that contains the cookies from the given base url.
        :type requests.cookies.RequestsCookieJar
        :return: An Object that contains the cookies from the given root url (from 
            the requests.cookies.RequestsCookieJar class).
        """        
        return requests.get(self.cookies_endpoint).cookies

    def get_countries(self) -> list:
        """
        Function that will return the countries from the country endpoint.

        :return: A list of countries from the country endpoint.
        """
        retry = 0

        if retry < 2:
            try:
                countries = requests.get(self.country_endpoint, cookies=self.cookies).json()

            except RequestException as e:
                print(f"An error occurred: {e}")
                retry += 1
                time.sleep(1)

                self.cookies = self.refresh_cookie()
                countries = requests.get(self.country_endpoint, cookies=self.cookies).json()

        else:
            raise MaxRetriesExceeded()

        return countries
    
    def get_leaders(self, country: str) -> list:
        """
        Function that will populate the leaders_data dictionary with the leaders 
        for a specific country.

        :param country: A str that speficies the country for which the leaders are 
            to be retrieved.
        :type str
        """
        retry = 0

        if retry < 2:
            try:
                leaders = requests.get(self.leaders_endpoint, cookies=self.cookies,
                                       params={"country": country})
            
            except RequestException as e:
                print(f"An error occurred: {e}")
                retry += 1
                time.sleep(1)

                self.cookies = self.refresh_cookie()
                leaders = requests.get(self.leaders_endpoint, cookies=self.cookies,
                                       params={"country": country})

        else:
            raise MaxRetriesExceeded()

        self.leaders_data[country] = leaders.json()

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        """
        Function that will return the first paragraph of a given Wikipedia url.

        :param wikipedia_url: A str that contains the URL for which the paragraph 
            is to be returned.
        :type str
        :return: A str that contains the first paragraph with the information 
            about the leader.
        """
        retry = 0

        if retry < 2:
            try:
                wikipedia_response = requests.get(wikipedia_url)
                soup = BeautifulSoup(wikipedia_response.text, "html.parser")

                first_paragraph = ""
                for paragraph in soup.find_all("p"):
                    if paragraph.find("b"):
                        first_paragraph = paragraph.get_text()
                        first_paragraph = re.sub(r' \[.*\].*?,', ',', first_paragraph)
                        break

            except:
                print("There was an error.")
                retry += 1
                time.sleep(1)
                self.get_first_paragraph(wikipedia_url)

        else:
            raise MaxRetriesExceeded()
        
        return first_paragraph
    
    def to_json_file(self, filepath: str) -> None:
        """
        Function that stores the leader_data dictionary in a JSON file with the
            specified filepath.

        :param filepath: A str that contains filepath of the JSON file that is
            to be created.
        :type str
        """
        with open(filepath, "w") as fp:
            json.dump(self.leaders_data, fp)