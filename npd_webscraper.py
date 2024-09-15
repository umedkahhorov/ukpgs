# web scraping from NPD wellbore info
# https://www.sodir.no/en/about-us/open-data/
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class WebScraper:
    """
    A class to scrape a webpage, extract data from an HTML table, and store the data in a pandas DataFrame.

    Attributes:
        url (str): The URL of the webpage to scrape.
        soup (BeautifulSoup object): Parsed HTML content of the webpage.
        attributes (list): A list to store the table's attributes (column 1).
        values (list): A list to store the corresponding values (column 2).
    """
    
    def __init__(self, url):
        """
        Initializes the WebScraper with the URL and prepares empty lists for attributes and values.
        
        Args:
            url (str): The URL of the webpage to scrape.
        """
        self.url = url
        self.soup = None  # Will hold the parsed HTML content
        self.attributes = []  # List to hold the 'Attribute' column data
        self.values = []  # List to hold the 'Value' column data

    def fetch_webpage(self):
        """
        Fetches the webpage content using the requests library and parses it using BeautifulSoup.
        """
        response = requests.get(self.url)  # Fetches the content from the provided URL
        
        if response.status_code == 200:  # 200 means the request was successful
            # Parsing the HTML content with BeautifulSoup
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve the webpage: {self.url}")  # Handle request failure

    def extract_table_data(self):
        """
        Extracts data from the HTML table and stores it in the attributes and values lists.
        This method looks for a specific table structure and extracts row data.
        """
        if not self.soup:
            raise Exception("Soup object is not initialized. Call fetch_webpage() first.")  # Ensure webpage is parsed
        
        # Find the specific table body (adjust this selector as needed for your table)
        table_body = self.soup.select('div div div div div table tbody')  

        for tbody in table_body:  # Iterate over each table body (there may be multiple)
            rows = tbody.find_all('tr')  # Find all table rows in the table body

            for row in rows:
                # Process each row to extract the attribute and value
                attribute, value = self.process_row(row)
                
                # Only append non-empty attributes and values
                if attribute and value:
                    self.attributes.append(attribute)  # Store attribute (first column)
                    self.values.append(value)  # Store value (second column)

    def process_row(self, row):
        """
        Processes each row of the table to extract the attribute (first column) and value (second column).
        
        Args:
            row (BeautifulSoup element): A row from the table.

        Returns:
            tuple: A tuple containing the cleaned attribute and value from the row.
        """
        # Extract the first cell (Attribute) and second cell (Value)
        attribute_td = row.find_all('td')[0] if len(row.find_all('td')) > 0 else None
        value_td = row.find_all('td')[1] if len(row.find_all('td')) > 1 else None

        # Clean the attribute and extract value
        attribute = self.clean_attribute(attribute_td) if attribute_td else None
        value = self.extract_value(value_td) if value_td else None

        return attribute, value

    @staticmethod
    def clean_attribute(attribute_td):
        """
        Cleans up the attribute text by removing excessive newlines and extra spaces.
        
        Args:
            attribute_td (BeautifulSoup element): The table cell containing the attribute.

        Returns:
            str: Cleaned attribute text.
        """
        attribute = attribute_td.get_text(strip=False)  # Get text from the HTML element without stripping
        # Remove excessive newlines by splitting at multiple newlines
        return attribute.split('\n\n\n\n')[0]  # Adjust this splitting logic based on table structure

    @staticmethod
    def extract_value(value_td):
        """
        Extracts the value from a table cell, handling cases where a button might be present.
        
        Args:
            value_td (BeautifulSoup element): The table cell containing the value.

        Returns:
            str: Extracted and cleaned value text.
        """
        button = value_td.find('button')  # Check if there's a button inside the table cell
        if button:
            # Extract text from the button if it exists
            return button.get_text(strip=True)
        # Otherwise, extract the regular text from the table cell
        return value_td.get_text(strip=True)

    def create_dataframe(self):
        """
        Creates a pandas DataFrame from the extracted attributes and values.

        Returns:
            DataFrame: A pandas DataFrame with two columns: 'Attribute' and 'Value'.
        """
        # Create a DataFrame with the attributes and values
        df = pd.DataFrame({
            'Attribute': self.attributes,
            'Value': self.values
        })

        # Clean up the 'Attribute' column by removing any '\n' characters and trimming spaces
        df['Attribute'] = df['Attribute'].apply(lambda x: re.sub(r'\n+', ' ', x).strip())

        return df

    def scrape(self):
        """
        The main method that orchestrates the entire scraping process:
        1. Fetch the webpage.
        2. Extract the table data.
        3. Create and return a pandas DataFrame with the extracted data.

        Returns:
            DataFrame: A pandas DataFrame containing the scraped table data.
        """
        self.fetch_webpage()  # Step 1: Fetch the webpage
        self.extract_table_data()  # Step 2: Extract the table data
        return self.create_dataframe()  # Step 3: Return the DataFrame

# Usage example
url = "https://factpages.sodir.no/en/wellbore/PageView/Exploration/All/105"  # URL of the webpage you want to scrape
scraper = WebScraper(url)  # Create an instance of WebScraper with the URL
df = scraper.scrape()  # Call the scrape method to get the DataFrame
# Display the resulting DataFrame
df.head(10)
