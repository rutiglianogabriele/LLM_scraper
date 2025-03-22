"""
Configuration settings for the web scraper.
"""

# HTTP request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://www.google.com',
    'Accept-Language': 'en-US,en;q=0.5'
}

# File paths
INPUT_FILE = "data/input_urls.txt"
OUTPUT_FILE = "data/analyzed_content.txt"
ERROR_LOG = "error_log.txt"

# Scraping settings
MAX_URLS_PER_SITE = 70
MAX_RELEVANT_URLS = 10
MAX_CONTENT_CHARS = 23000
RETRY_ATTEMPTS = 3
RETRY_MIN_WAIT = 2000  # milliseconds
RETRY_MAX_WAIT = 6000  # milliseconds

# File extensions to exclude from scraping
EXCLUDED_EXTENSIONS = ['.zip', '.mp4', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

# OpenAI settings
URL_SELECTION_MODEL = "gpt-4o-mini-2024-07-18"
CONTENT_ANALYSIS_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

# Configure these questions based on what you want to extract
# Brief questions for URL selection
QUESTIONS_BRIEF = {
    "Org Name": "Find the organization's name",
    "Main URL": "Find the main website URL",
    "Location": "Find the organization's location information",
    "Description": "Get a short description of the organization/product",
    "Category": "Identify the main category of the product/service",
    "Target Users": "Identify who uses the product/service",
    "Legal Pages": "Find URLs to terms, privacy, etc."
}

# Detailed questions for content analysis
QUESTIONS = {
    "Organization Name": "Extract the full legal name of the organization associated with the given URL. Return just the name with a short explanation.",
    "Location": "Identify the headquarters or primary location of the organization. Provide only the country and city name with a short explanation.",
    "Description": "Write a 200-character technical description of what the organization offers or produces. Use precise, neutral language without marketing claims.",
    "Category": "Based on the content, classify this organization into a specific industry category. Provide only the most appropriate category name.",
    "Target Audience": "Identify the primary audience or users this organization serves. List specific types of users, industries, or demographic groups.",
    "Key Features": "Extract 3-5 key features or services offered by the organization based only on the content provided.",
    "Founding Year": "Find the year when this organization was founded, if mentioned."
}