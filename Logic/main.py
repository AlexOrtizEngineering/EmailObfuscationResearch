import os
import re
import time
import csvreader
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import unquote

# Returns first and last name from home page
def get_name(soup):
    title = soup.title.string if soup.title else ''
    words = title.split() if title else ''
    first_name = words[0] if len(words) > 0 else ''
    last_name = words[1] if len(words) > 1 else ''
    return first_name, last_name

# Function to check if email contains character and replace with replaceCharacter if found, or catch parts that contain "remove"
def clean_email(email, first_name, last_name):
    replacements = {
        '(': ' ', ')': ' ', '[': ' ', ']': ' ', '{': ' ', '}': ' ', 'ø': 'o',
        ' - ': '', ' dot ': '.', ' at ': '@', ' -dot- ': '.', ' -at- ': '@',
        '+': '', ' ': '', '\xa0': '',
        'firstname': first_name.lower(), 'first-name': first_name.lower(), '<firstname>': first_name.lower(),
        'lastname': last_name.lower(), 'last-name': last_name.lower(), '<lastname>': first_name.lower()
    }
    for key, value in replacements.items():
        email = email.replace(key, value)
    
    email = re.sub(r'\.\w*(remove|this)\w*\.','.', email)
    return email

# Sends a GET request to URL, parses the HTML concent using Beautiful Soup, and converts that to string
def url_to_soup(URL):
    UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0 UCSBNetworkMeasurement/2024 (contact; stijn; at; ucsb.edu;)"

    headers = {
            "User-Agent": UA
    }

    response = requests.get(URL, headers=headers, timeout=5)

    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    return soup

# Remove unnecessary characters from HTML
def filtering(html):
    characters_to_replace = '()[]+<>'
    translation_table = str.maketrans(characters_to_replace, ' ' * len(characters_to_replace))
    return html.translate(translation_table)

# Converts html to a string, and return first found email
def email_extractor(URL, soup, first_name, last_name):            
    for script in soup(["script", "style"]):
        script.extract()

    html_text = str(soup).lower()
    html_text = filtering(html_text)

    found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html_text, re.IGNORECASE)
    if found_emails:
        found_email = found_emails[0]
        found_email = clean_email(found_email, first_name, last_name)
        #print(f"Extracted email from {URL}: {found_email}\n")
        return found_email, "regular"

    #obfuscated_email = re.findall(r'\b[A-Za-z0-9._%+-]+(?:\s(dot|\-dot\-|\.))?(?:\s(at|\-at\-|@))?[A-Za-z0-9.-]+(?:\s(dot|\-dot\-|\.))[A-Za-z0-9.-]+(?:\s(dot|\-dot\-|\.))[A-Za-z]{2,}\b', html_text, re.IGNORECASE)
    html_text = html_text.replace(".", " dot ")
    obfuscated_email = re.findall(r'\b[A-Za-z0-9._%+-]+(?:\s+(?:dot|\-dot\-|\.)\s+[A-Za-z0-9._%+-]+)*\s+(?:at|\-at\-|@)\s+[A-Za-z0-9.-]+(?:\s+(?:dot|\-dot\-|\.)\s+[A-Za-z0-9.-]+)*\s+(?:dot|\-dot\-|\.)\s+[A-Za-z]{2,}\b', html_text, re.IGNORECASE)
    if obfuscated_email:
        found_email = obfuscated_email[0]
        found_email = clean_email(found_email, first_name, last_name)
        #print(f"Extracted obfuscated email from {URL}: {found_email}\n")
        return found_email, "obfuscated"
    
    email_matches = re.findall(r'href=["\']mailto:([^"\']+)["\']', html_text)
    if email_matches:
        found_email = unquote(email_matches[0])
        found_email = clean_email(found_email, first_name, last_name)
        #print(f"Extracted email from mailto in {URL}: {found_email}\n")
        return found_email, "mailto"

    #print(f"No valid email found in {URL}\n")
    return None, "none"

# Consolidated use of url_to_soup and email_extractor
def soup_processor(URL, first_name, last_name):
    soup = url_to_soup(URL)
    email, category = email_extractor(URL, soup, first_name, last_name)
    if email:
        emails.append(email)
        return email, category
    else:
        return None, "none"

# Makes sure URLs start with https://
def normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    elif url.startswith("http://"):
        url = url.replace("http://", "https://", 1)
    return url

def concatenate_url(href, URL):
    modified_URL = URL
    if 'index.html' in URL:
        modified_URL = URL.replace('index.html', "")

    if href.startswith('/'):
        full_url = modified_URL.rstrip('/') + href
    else:
        full_url = modified_URL + href
    
    return full_url

def mail_to(href):
    email = href[7:]
    email = clean_email(email)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        #print(f"Found email address in href: {email}\n")
        emails.append(email)
        return email
    return None

# Start tracking run time
start_time = time.time()

# Lists of URLs that yielded emails
working_urls = []

# List of URLs that produce an error
broken_urls = []

# Blank list to store emails
emails = []

# Goes through each URL to extract emails
def process(pair):
    URL = pair[0]
    URL = normalize_url(URL)
    #gt_mail = pair[1] #Ground truth
    name = pair[1]
    try:
        soup = url_to_soup(URL)
        first_name, last_name = get_name(soup)
        email, category = email_extractor(URL, soup, first_name, last_name)
        #return category
        if email:
            emails.append(email)
            working_urls.append(URL)
        
        else:
            contact_link = None
            about_link = None
            email_link = None
            
            a_tags = soup.find_all('a')
            for a in a_tags:
                #print(a)
                href = a.get('href')
                if href:
                    if href.startswith('/') or URL in href or href.endswith(".html"):
                        if href.startswith('/'):
                            full_url = URL.rstrip('/') + href
                        elif href.endswith('.html'):
                            full_url = URL + "/" + href
                        else:
                            full_url = href
                            
                        if 'contact' in full_url:
                            contact_link = full_url
                        elif 'about' in full_url:
                            about_link = full_url
                        elif 'email' in full_url:
                            email_link = full_url
                    
                    if not contact_link and 'contact' in href:
                        contact_link = concatenate_url(href, URL)
                    elif not about_link and 'about' in href:
                        about_link = concatenate_url(href, URL)
                    elif not email_link and 'email' in href:
                        email_link = concatenate_url(href, URL)

            if not email and contact_link:
                email, category = soup_processor(contact_link, first_name, last_name)
                if email:
                    working_urls.append(URL)
            if not email and about_link:
                email, category = soup_processor(about_link, first_name, last_name)
                if email:
                    working_urls.append(URL)
            if not email and email_link:
                email, category = soup_processor(email_link, first_name, last_name)
                if email:
                    working_urls.append(URL)
            #if not contact_link and not about_link and not email_link:
            #    print(f"No contact, about, or email link found for {URL}\n")

        if email == "blog@wordpress.com":
            category = "wordpress"


        #if category == "none":
        #    print(URL)
        print(URL, category)
        return category

    except requests.exceptions.RequestException as e:
        #print(URL)
        #print(f"Error fetching {URL}: {e}\n")
        broken_urls.append(URL)


# Get the directory where main.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "websites.txt")

infile = open(file_path, "r")
pairs = []
for line in infile:
    split = line.split(",")
    name = split[0].strip()
    website = split[1].strip()
    pairs.append((website, name))

for pair in pairs:
    process(pair)


# Print total runtime of program
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total runtime: {elapsed_time} seconds")

exit()
