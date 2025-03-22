# 🔍 Web Scraper with AI 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Beta-orange)

An intelligent web scraping tool that uses AI to extract and analyze specific information from websites, powered by OpenAI's language models.

## Features

- Automatically extracts and filters relevant URLs from websites
- Uses AI to identify and select the most informative pages
- Extracts structured data based on configurable questions
- Provides explanations for each extracted data point
- Highly configurable for different website types and use cases

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper-ai.git
   cd web-scraper-ai
   ```

2. Install required packages:
   ```bash
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

```bash
python -m src.main
```

Results will be saved to `data/analyzed_content.txt` in CSV format (semicolon-delimited).

## Project Structure

```
web_scraper/
├── README.md
├── requirements.txt
├── .env
├── data/
│   ├── input_urls.txt    # URLs to be processed
│   └── analyzed_content.txt  # Generated output
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── scraper.py        # URL extraction and content scraping
│   ├── processor.py      # AI processing of content
│   └── config.py         # Configuration settings
└── error_log.txt         # Error logging
```

## Configuration

Edit `src/config.py` to customize:

- HTTP request headers
- Scraping behavior (timeouts, retries, etc.)
- OpenAI model selection
- Questions for URL selection
- Questions for content analysis

## Disclaimer

This script has been designed to be adaptable to various contexts and to be as flexible as possible. As such, it requires further refinements to be adapted to your specific needs. The default configuration is just a starting point.

**Important Legal Notice**: It is the user's responsibility to ensure that the websites being scraped permit automated content extraction. Many websites have terms of service that prohibit scraping, and using this tool might violate those terms. Always:

1. Check the website's robots.txt file
2. Review the terms of service
3. Implement appropriate rate limiting
4. Respect copyright and intellectual property rights
5. Follow applicable data privacy regulations

The authors of this tool accept no liability for misuse or any consequences thereof.

## Potential Use Cases

This tool can be adapted for various purposes. Here is something ChatGPT suggests:

| Use Case | Description |
|----------|-------------|
| **Competitive Analysis** | Gather information about competitors' products, services, and positioning in the market. |
| **Research Aggregation** | Collect data from multiple sources for academic or market research projects. |
| **Content Monitoring** | Track changes on important websites over time. |
| **Lead Generation** | Extract contact information and company details for sales prospecting (where permitted). |
| **Industry Trend Analysis** | Analyze multiple industry websites to identify emerging trends and terminology. |
| **Knowledge Base Creation** | Extract and organize information to build internal knowledge repositories. |
| **Data Sets for Training** | Create labeled datasets for training machine learning models (with appropriate permissions). |

To adapt this tool for any of these use cases, modify the questions in `config.py` to target the specific information you need.
