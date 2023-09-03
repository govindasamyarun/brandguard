import os
import argparse
import sys
import glob
import re

import pyfiglet
from termcolor import colored

from libs.typosquatDnstwist import TyposquatDnstwist
from libs.imageProcess import ImageProcess

def banner(text):

    # Choose a font from the available options (you can try different fonts)
    font = "slant"

    # Generate the banner text in the chosen font
    banner = pyfiglet.figlet_format(text, font=font)

    # Add color to the banner text (you can choose different colors)
    colored_banner = colored(banner, color="green")

    # Print the colored banner
    print(colored_banner)

if __name__ == "__main__":
    # print banner 
    banner("BrandGuard")
    parser = argparse.ArgumentParser(
		usage='%s [OPTION]... DOMAIN' % sys.argv[0],
		add_help=False,
		description=
		'''Identify suspicious domains that impersonates brand names, logos, slogans and taglines. '''
		)

    parser.add_argument('domain', help='Domain name or URL to scan')
    parser.add_argument('-w', '--webdriver-dir', help='Path to the Chrome WebDriver executable')
    parser.add_argument('-s', '--screenshot-dir', required=True, help='Path to store the screenshots')
    parser.add_argument('-d', '--dictionary', help='Enter dictionary file path')
    parser.add_argument('-t', '--tld', help='Enter tld file path')
    parser.add_argument('-k', '--keywords', required=True, nargs='+', default=[], help='Keywords to look for on suspicious websites')

    print("\nNote: If the Chrome web driver included in this package is outdated, download the latest version from https://chromedriver.chromium.org/downloads.\n")

    output = {}
    green_color = "\033[92m"
    reset_color = "\033[0m"

    if not sys.argv[1:] or '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        sys.exit()

    # File cleanup 
    dnstwist_log_file = os.path.join(os.getcwd(), 'dnstwist.log')
    if os.path.exists(dnstwist_log_file):
        os.remove(dnstwist_log_file)

    args = parser.parse_args()

    if os.path.exists(args.screenshot_dir):
        if (args.screenshot_dir.endswith('/') or args.screenshot_dir.endswith('\\\\')):
            screenshot_dir = args.screenshot_dir[:-1]
        else:
            screenshot_dir = args.screenshot_dir
        screenshot_file_names = glob.glob(args.screenshot_dir+'/*')

        if screenshot_file_names:
            user_input = input("Files will be deleted from the screenshot directory. Enter 'yes' to continue: ")
            if user_input.strip().lower() == 'yes':
                for f in screenshot_file_names:
                    os.remove(f)
                    pass
            else:
                sys.exit()
    else:
        print('Screenshot directory does not exist')
        sys.exit()

    if args.webdriver_dir:
        webdriver_dir = args.webdriver_dir
    else:
        webdriver_dir = os.path.join(os.getcwd(), 'webdriver/chromedriver')

    if args.keywords:
        keywords = args.keywords

    if args.dictionary:
        dictionary = args.dictionary
    else:
        dictionary = ''

    if args.tld:
        tld = args.tld
    else:
        tld = ''

    result_dnstwst = TyposquatDnstwist(webdriver_dir, screenshot_dir, dictionary, tld).generate(args.domain)

    if result_dnstwst["status"]:
        screenshot_file_names = glob.glob(screenshot_dir+'/*')
        for keyword in keywords:
            for file_name in screenshot_file_names:
                # Call the function to find the word within the image
                result = ImageProcess(keyword, file_name).analysis()
                domain = re.findall(r'\S+\_(\S+)\.png$', file_name)[0]
                if domain in output:
                    output[domain] = output[domain] | result
                else:
                    output[domain] = result

        print("\nImpersonated domains:")
        for key, value in output.items():
            if value == True:
                print(f'\t{green_color}{key}{reset_color}')
    else:
        print("Error executing dnstwist - {}".format(result_dnstwst["message"]))