from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import webbrowser
import urllib.request as urllib3
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import cv2 as cv
import requests
import Tree
from lxml import html

# initialize an HTTP session
session = HTMLSession()

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    
    # CAPTCHA
    img_tags = form.find_all("img")
    for img_tag in img_tags:
        if img_tag.attrs.get('id') == "form_rcdl:j_idt34:j_idt41":
            cap_img = img_tag.attrs.get("src")
            cap_img_url = urljoin("https://parivahan.gov.in", cap_img)
            urllib3.urlretrieve(cap_img_url, "captcha.jpg")
            # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
            # im = Image.open("captcha.jpg") # Grayscale conversion
            

    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"

first_form = get_all_forms(url)[0]

form_details = get_form_details(first_form)

print(form_details)

data = {}
data['javax.faces.partial.ajax'] = 'true'
data['javax.faces.source'] = 'form_rcdl:j_idt46'
data['javax.faces.partial.execute'] = '@all'
data['javax.faces.partial.render'] = 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl'
data['javax.rcdl:j_idt46'] = 'form_rcdl:j_idt46'
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        if input_tag["name"] != "javax.faces.ViewState":
            authenticity_token = list(set(input_tag["value"]))[0]
            data[input_tag["name"]] = authenticity_token
        # if it's hidden, use the default value
        else:
            data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit":
        value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
        data[input_tag["name"]] = value

print(data)

url = urljoin(url, form_details["action"].split(';')[0])
print(url)

if form_details["method"] == "post":
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    res = session.post(url, data=data)
# elif form_details["method"] == "get":
#     res = session.get(url, params=data)

# the below code is only for replacing relative URLs to absolute ones
print(session.cookies)
print(res.content)
soup = BeautifulSoup(res.content, "html.parser")
# for link in soup.find_all("link"):
#     try:
#         link.attrs["href"] = urljoin(url, link.attrs["href"])
#     except:
#         pass
# for script in soup.find_all("script"):
#     try:
#         script.attrs["src"] = urljoin(url, script.attrs["src"])
#     except:
#         pass
# for img in soup.find_all("img"):
#     try:
#         img.attrs["src"] = urljoin(url, img.attrs["src"])
#     except:
#         pass
# for a in soup.find_all("a"):
#     try:
#         a.attrs["href"] = urljoin(url, a.attrs["href"])
#     except:
#         pass

# write the page content to a file
# open("page.html", "w").write(str(soup))

# open the page on the default browser
# webbrowser.open("page.html")  
  

