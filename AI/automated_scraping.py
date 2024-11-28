import re
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key="my_key_here")
model = genai.GenerativeModel("gemini-1.5-flash")

CHUNK_SIZE = 2000

def split_into_chunks(text):
    return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def get_email(html):
    chunks = split_into_chunks(html)
    for chunk in chunks:
        prompt = f"Please extract an email from the following HTML or return \"error\": {chunk}"
        response = get_ai_response(prompt)
        if response.strip() != "error" and is_valid_email(response):
            return response.strip()
    return None

emails = []
URLs = [
    "http://www.informatics.indiana.edu/xw7",
    "https://www.kellimarshall.net/",
    "https://nickbostrom.com/",
    "https://krissabbi.com",
    "https://www.geoengineer.org/",
    "https://inesvbarreiros.weebly.com/",
    "https://isabellaoleksy.weebly.com",
    "https://brett-morgan.weebly.com"
]

# prompt = f"I am going to give you HTML that may or may not contain an email. When I enter the HTML, either return the email without quotations or return \"error.\""
# response = get_ai_response(prompt)

for URL in URLs:
    try:
        #extract html from url
        response = requests.get(URL)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        html_text = str(soup)
        #extract email from html
        email = get_email(html_text)
        if email:
            emails.append(email)
        else:
            print(f"No valid email found for {URL}")
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {URL}: {e}\n")

print(emails)
