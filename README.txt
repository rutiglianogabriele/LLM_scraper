# Web Scraper with AI Analysis

A tool for scraping websites and extracting information using AI analysis.

## Setup

1. Clone this repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Add target URLs to `data/input_urls.txt` (one URL per line)
5. Configure your scraping parameters in `src/config.py`

## Usage

Run the main script from the project root:

```
python -m src.main
```

Results will be saved to `data/analyzed_content.txt`

## Project Structure

- `data/`: Contains input URLs and output files
- `src/`: Contains source code
  - `main.py`: Entry point for the application
  - `scraper.py`: Functions for extracting URLs and content
  - `processor.py`: Functions for processing content with OpenAI
  - `config.py`: Configuration settings

## Disclaimer

This script has been designed to be adaptable to various contexts and to be as flexible as possible. As such, it needs further refinements to be adapted to your specific needs. The default configuration is just a starting point.

**Important Legal Notice**: It is the user's responsibility to ensure that the websites being scraped allow for this kind of automated content extraction. Many websites have terms of service that prohibit scraping, and using this tool might violate those terms. Always:

1. Check the website's robots.txt file
2. Review the terms of service
3. Consider rate limiting your requests
4. Respect copyright and intellectual property rights

The authors of this tool accept no liability for misuse or any consequences thereof.

## Potential Use Cases

This tool can be adapted for various purposes, such as:

1. **Competitive Analysis**: Gather information about competitors' products, services, and positioning in the market.

2. **Research Aggregation**: Collect data from multiple sources for academic or market research projects.

3. **Content Monitoring**: Track changes on important websites over time.

4. **Lead Generation**: Extract contact information and company details for sales prospecting (where permitted).

5. **Industry Trend Analysis**: Analyze multiple industry websites to identify emerging trends and terminology.

6. **Knowledge Base Creation**: Extract and organize information to build internal knowledge repositories.

7. **Data Sets for Training**: Create labeled datasets for training machine learning models (with appropriate permissions).

To adapt this tool for any of these use cases, modify the questions in `config.py` to target the specific information you need.