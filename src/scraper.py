"""
Functions for scraping web content.
"""

import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urljoin, urlparse
from retrying import retry

from src.config import (
    HEADERS, EXCLUDED_EXTENSIONS, MAX_URLS_PER_SITE, 
    MAX_CONTENT_CHARS, RETRY_ATTEMPTS, RETRY_MIN_WAIT, RETRY_MAX_WAIT
)

def is_valid_url(url):
    """
    Check if a URL is valid for scraping.
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and not any(parsed.path.lower().endswith(ext) for ext in EXCLUDED_EXTENSIONS)

def extract_urls_from_html(session, url):
    """
    Extract URLs from a given webpage.
    
    Args:
        session (requests.Session): Session object for making HTTP requests
        url (str): URL to extract links from
        
    Returns:
        list: List of valid URLs found on the page
    """
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = {urljoin(url, link['href']) for link in soup.find_all('a', href=True)}
        return [url for url in urls if is_valid_url(url)][:MAX_URLS_PER_SITE]
    except requests.RequestException as e:
        logging.error(f"Failed to extract URLs from {url}: {str(e)}")
        return []

@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_random_min=RETRY_MIN_WAIT, wait_random_max=RETRY_MAX_WAIT)
def scrape_page_content(session, url):
    """
    Scrape content from a webpage with retry mechanism.
    
    Args:
        session (requests.Session): Session object for making HTTP requests
        url (str): URL to scrape content from
        
    Returns:
        str: Scraped text content
    """
    try:
        print(f"Scraping content from: {url}")
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for element in soup(['script', 'style', 'noscript']):
            element.decompose()

        # Get text content
        content = "\n".join([p.get_text(strip=True) for p in soup.find_all('p')])
        if not content.strip():
            content = soup.get_text(separator="\n").strip()

        # Truncate content to avoid OpenAI limits
        return re.sub(r'[^\x20-\x7E]+', '', content[:MAX_CONTENT_CHARS])
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return ""