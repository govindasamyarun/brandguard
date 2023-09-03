import os
import dnstwist
from selenium import webdriver

class TyposquatDnstwist:
    def __init__(self, webdriver_path, screenshots_path, dictionary, tld) -> None:
        self.webdriver_path = webdriver_path
        self.screenshots_path = screenshots_path
        self.dictionary = dictionary
        self.tld = tld
        self.log_file_path = "dnstwist.log"

    def generate(self, domain):

        # Configure Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
        chrome_options.add_argument("--window-size=1920x1080")  # Set browser window size (optional)

        # Add the WebDriver path to the PATH environment variable
        os.environ['PATH'] = f'{os.environ["PATH"]}:{self.webdriver_path}'

        # Create a WebDriver instance with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            dnstwist.run(domain=domain, registered=True, format='null', phash=True, screenshots=self.screenshots_path, dictionary=self.dictionary, tld=self.tld)
            return {"status": True, "message": ""}
        except Exception as e:
            return {"status": False, "message": str(e)}