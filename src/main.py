import os
from dotenv import load_dotenv
from tqdm import tqdm
import requests
import logging

from src.scraper import extract_urls_from_html, scrape_page_content
from src.processor import ask_openai_for_relevance, process_content_with_openai, parse_openai_response
from src.config import INPUT_FILE, ERROR_LOG

def setup():
    """Set up the environment and logging."""
    load_dotenv()
    logging.basicConfig(filename=ERROR_LOG, level=logging.ERROR)
    os.makedirs("data", exist_ok=True)

def main():
    """Main function to process each URL."""
    setup()
    
    # Read URLs from input file
    with open(INPUT_FILE, "r") as input_file:
        urls = [line.strip() for line in input_file]
    
    for url in tqdm(urls, desc="Processing URLs"):
        print(f"\nProcessing URL: {url}")
        
        try:
            with requests.Session() as session:
                # Step 1: Extract URLs from the site
                print("Step 1: Extracting URLs")
                site_urls = extract_urls_from_html(session, url)
                if not site_urls:
                    print(f"No URLs found for {url}. Skipping...")
                    continue
                
                # Step 2: Select relevant URLs
                print("Step 2: Selecting relevant URLs")
                relevant_urls = ask_openai_for_relevance(site_urls)
                if not relevant_urls:
                    print(f"No relevant URLs found for {url}. Skipping...")
                    continue
                
                # Step 3: Scrape content from relevant URLs
                print("Step 3: Scraping content")
                all_content = []
                for relevant_url in relevant_urls:
                    content = scrape_page_content(session, relevant_url)
                    if content:
                        all_content.append(content)
                
                if not all_content:
                    print(f"No content found for {url}. Skipping...")
                    continue
                
                # Step 4: Process all content at once
                print("Step 4: Processing content")
                combined_content = "\n\n".join(all_content)
                processed_results = process_content_with_openai(combined_content)
                
                # Step 5: Save results
                parse_openai_response(processed_results, url)
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            parse_openai_response("Error processing content", url)
            logging.error(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    main()