"""
Functions for processing content with OpenAI.
"""

import os
import re
import json
import csv
import logging
from openai import OpenAI

from src.config import (
    QUESTIONS_BRIEF, QUESTIONS, URL_SELECTION_MODEL, CONTENT_ANALYSIS_MODEL, 
    TEMPERATURE, MAX_RELEVANT_URLS, OUTPUT_FILE
)

# Initialize OpenAI client (API key loaded from .env)
client = OpenAI()

def ask_openai_for_relevance(urls):
    """
    Ask OpenAI to select the most relevant URLs.
    
    Args:
        urls (list): List of URLs to select from
        
    Returns:
        list: Selected relevant URLs
    """
    try:
        url_list_str = "\n".join(urls)
        prompt = (
            f"I have a list of URLs from a website. Select the most relevant URLs that are likely to contain information about the following aspects:\n\n"
            + "\n".join([f"- {field}: {brief_description}" for field, brief_description in QUESTIONS_BRIEF.items()])
            + "\n\nReturn ONLY the list of selected URLs, separated by commas, without any additional text."
            + "\n\nURLs to choose from:\n" + url_list_str
        )

        completion = client.chat.completions.create(
            model=URL_SELECTION_MODEL,
            messages=[{"role": "system", "content": prompt}]
        )
        
        response = completion.choices[0].message.content
        return [url.strip() for url in response.split(',')][:MAX_RELEVANT_URLS] if response else []
    except Exception as e:
        print(f"Error while querying OpenAI: {e}")
        logging.error(f"OpenAI query error: {str(e)}")
        return []

def process_content_with_openai(scraped_content):
    """
    Process scraped content with OpenAI to extract information.
    
    Args:
        scraped_content (str): Scraped content from websites
        
    Returns:
        str: OpenAI's response with extracted information
    """
    try:
        # Create chunks of content to avoid token limits
        max_chunk_size = 22000  # Approximate chunk size
        content_chunks = [scraped_content[i:i + max_chunk_size] 
                         for i in range(0, len(scraped_content), max_chunk_size)]
        
        # Process first chunk only to avoid excessive API calls
        chunk = content_chunks[0]
        
        combined_prompt = (
            "Analyze the following content and answer all questions. Base all answers on factual data and do not make assumptions. "
            "Format your response as a JSON object, followed by explanations for each answer and their confidence level separated by '|||'. "
            "Each field in the JSON should correspond to one of the questions.\n\n"
            "Questions to answer:\n"
        )
        
        for field, question in QUESTIONS.items():
            combined_prompt += f"\n{field}: {question}"
            
        combined_prompt += f"\n\nContent to analyze:\n{chunk}"
        
        completion = client.chat.completions.create(
            model=CONTENT_ANALYSIS_MODEL,  
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes content and provides structured answers in JSON format. Separate responses and explanations with '|||'."},
                {"role": "user", "content": combined_prompt}
            ]
        )
        
        response = completion.choices[0].message.content
        print("Raw OpenAI Response received")
            
        return response
    
    except Exception as e:
        print(f"Error processing content with OpenAI: {e}")
        logging.error(f"OpenAI processing error: {str(e)}")
        return "Error processing content"

def parse_openai_response(response_text, url):
    """
    Parse the response from OpenAI and save to CSV file.
    
    Args:
        response_text (str): Response from OpenAI
        url (str): URL of the analyzed website
        
    Returns:
        str: Status message
    """
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    file_exists = os.path.isfile(OUTPUT_FILE)
    
    try:
        if response_text == "Error processing content":
            json_content = {field: f"Error: Could not process {url}" for field in QUESTIONS.keys()}
        else:
            # Extract and parse JSON
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if not json_match:
                # Try alternative JSON extraction if markdown format isn't found
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if not json_match:
                    raise ValueError("No JSON content found in response")
            
            try:
                json_content = json.loads(json_match.group(0).strip())
            except json.JSONDecodeError:
                # If JSON parsing fails, create error content
                json_content = {field: f"Error: Invalid JSON from {url}" for field in QUESTIONS.keys()}
        
        # Try to extract explanations, but don't fail if not found
        explanations_dict = {}
        explanations_match = re.search(r'### Explanations:\s*(.*?)(?=\Z|\n\n(?!-))', response_text, re.DOTALL)
        if explanations_match:
            explanations_text = explanations_match.group(1).strip()
            for field in json_content.keys():
                field_escaped = re.escape(field)
                pattern = rf"\*\*{field_escaped}\*\*:(.*?)(?=\n-|\n\n|\Z)"
                match = re.search(pattern, explanations_text, re.DOTALL)
                if match:
                    explanation = match.group(1).strip()
                    explanation = re.sub(r'\*\*Confidence Level:.*?\*\*', '', explanation)
                    explanation = explanation.replace('"', '').strip()
                    explanations_dict[field] = explanation
                else:
                    explanations_dict[field] = "No explanation provided"
        else:
            explanations_dict = {field: "No explanation provided" for field in json_content.keys()}
        
        # Format any arrays as string if present
        for key, value in json_content.items():
            if isinstance(value, list):
                json_content[key] = ', '.join(value)
        
        # Create the combined data dictionary
        combined_data = {"URL": url}
        for field in json_content.keys():
            combined_data[field] = json_content[field]
            combined_data[f"{field} Explanation"] = explanations_dict.get(field, "No explanation provided")
        
        # Write to CSV file
        with open(OUTPUT_FILE, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["URL"] + sum([[field, f"{field} Explanation"] for field in QUESTIONS.keys()], [])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(combined_data)
        
        return f"Data has been {'appended to' if file_exists else 'written to new'} CSV file '{OUTPUT_FILE}' successfully"
    
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        logging.error(f"Parse error: {str(e)}")
        return f"Error: {str(e)}"