# BrandGuard

## About The Project

Adversaries often use organization logos, slogans, and taglines to make typosquat domains appear legitimate. Even if the domain doesn't match the original website exactly, a logo or tagline can be enough to trick customers into falling for a scam. 

Brand Guard can identify suspicious domains that impersonate organization brand names, logos, taglines, and slogans in typosquat domains. This tool is built on top of the powerful [Dnstwist](https://github.com/elceef/dnstwist) tool, which enhances monitoring and significantly reduces analysis time.

<img width="1039" alt="Screenshot 2023-09-03 at 4 50 32 PM" src="https://github.com/govindasamyarun/brandguard/assets/69586504/f401901e-ebc4-41df-bbe4-07058d89f1b9">

## Getting started

### Prerequisites

* Chrome
* tesseract

### Options 

* domain - domain name to be monitored
* -w, --webdriver-dir - Path to the Chrome WebDriver executable. Default: ./webdriver/chromedriver (optional). If the Chrome web driver included in this package is outdated, download the latest version from https://chromedriver.chromium.org/downloads.
* -s, --screenshot-dir - Path to store the screenshots
* -d, --dictionary - Add keywords to the ./dictionaries/domains.dict file
* -t, --tld - Add tld keywords to the ./dictionaries/tld.dict file
* -k, --keywords - Enter brand name, slogan and taglines 

### Installation

1. Clone the repository

   ```sh
   cd /Data
   git clone https://github.com/govindasamyarun/brandguard.git
   ```
   
2. Build the container

   ```sh
   pwd: /Data/brandguard
   docker build -t app .
   ```

3. Start the container

   ```sh
   pwd: /Data/brandguard
   
   docker run --rm -it --cap-add=SYS_ADMIN --security-opt seccomp=unconfined --name=app app /bin/bash
   ```

4. Execute the script

    ```py
    python brandguard.py <<domain>> -k logoname 'slogan test' -s ./screenshots -d ./dictionaries/domains.dict -t ./dictionaries/tlds.dict
    ```
