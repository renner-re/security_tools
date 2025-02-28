#!/usr/bin/python3


import os
import sys
import argparse
import requests
import BeautifulSoup
import re
import urllib.parse as urlparse
from urllib.parse import parse_qs
import nmap
import Selenium
from termcolor import colored
import webdriver_manager

# check for SQL injection, XSS, CSRF, Dir traversal, remote code exec
def discover_urls(target_url):
    response = response.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a')]
    return urls

######################################################################
#                 Detect different attack types                      #
######################################################################

##############################################################
#         function to detect SQL Injection at a url          #
##############################################################

def detect_sql_inj(url, param):
    payload = "' OR '1'='1"
    response = requests.get(f"{url}?{param}={payload}")
    if "syntax error" in response.text.lower():
        print(f"SQL Injection vulnerability found at {url}. ")
    else:
        print(f"No SQL Injection found at {url}. ")

#############################################################
#                     Detect XSS at a url                   #
#############################################################
# https://thepythoncode.com/article/make-a-xss-vulnerability-scanner-in-python
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from colorama import Fore, Style
import argparse

# payloads to test with
# Add more payloads
XSS_PAYLOADs = [
    '"><svg/onload=alert(1)>',
    '\'><svg/onload=alert(1)>',
    '<img src=x onerror=alert(1)>',
    '\'><img src=x onerror=alert(1)',
    "';alert(String.fromCharCode(88,83,83))//'; alert(String.fromCharCode(88,83,83))//--></script>",
    "<Script>alert('XSS')</Script>",
    "<script>alert(document.cookie)</script>"
]

# global var to store all crawled links here
crawled_links = set()

def print_crawled_links():
    print(f"\n[+] Links crawled: ")
    for link in crawled_links:
        print(f"     {link}")
    print()

# Get all forms it can
def get_all_forms(url):
    try:
        soup = bs(requests.get(url).content, "html.parser")
        return soup.find_all("form")
    except requests.exceptions.RequestExceptions as e:
        print(f"[-] Error retrieving forms from {url}: {e}")
        return []

# Extract form details
def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("input")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    # store form details in dic
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# Submit form with a specific value
def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}

    # fill inputs with provided value
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    # make HTTP request based on form method (GET or POST)
    try:
        if form_details["method"] = "post"
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)
    except:
        print(f"[-] Error submitting form to {target_url}: {e}")
        return None

# Extract all links from URL
def get_all_links(url):
    try:
        soup = bs(requests.get(url).content, "html.parser")
        return [urljoin[url, link.get("href")) for link in soup.find_all("a")]
    except requests.exceptions.RequestException as e:
        print(f"[-] Error getting links from {url}: {e}")
        return []


##########################################################
#               function to detect CSRF                  #
##########################################################
def detect_csrf(url, param):
    payload = 
    response = response.get()

##########################################################
#     function to detect Directory Traversal at a url    #
##########################################################
def detect_dir_trav(url, param):
    payload = 
    response = response.get()

##########################################################
#   function to detect Remote Code Execution at a url    #
##########################################################
def detect_rem_code_exec(url, param):
    payload = 
    response = response.get()

###########################################################
# function to detect File Upload vulnerabilities at a url #
###########################################################
def detect_file_upload(url, param):
    payload = 
    response = response.get()

####################################################################
#                          Create Reporting                        #
####################################################################

def gen_report(vulnerabilities):
    with open('report.json', 'w') as report_file:
        json.dump(vulnerabilities, report_file, indent=4)
    print("Report Generated: report.json")
