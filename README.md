# Campus Newspaper Scraper  
Using Student Newspapers to Study Campus Culture Over Time

## Project Goal

This project collects articles from college newspaper websites to analyze how campus culture has changed over time. Student newspapers serve as a meaningful proxy for understanding shifting perspectives, campus issues, and cultural trends.

Many college newspapers publicly expose RSS feeds (for example: `/rss`, `/feed`, or `/api`). This project automatically:

1. Discovers the RSS feed URL from each school's homepage  
2. Fetches and downloads the RSS XML  
3. Parses and extracts article metadata  
4. Outputs the scraped data into a structured CSV file

The resulting dataset can be used for further analysis such as topic modeling, sentiment analysis, or longitudinal trend studies.

## Project Structure

```
task1_webscraping/
│
├── src/
│   └── webscraping.py        # Helper functions (headers, get_rss, xml_to_df)
│
├── notebooks/
│   └── scraping.ipynb        # Jupyter notebook running the full pipeline
│
├── data/
│   └── articles.csv          # Final combined dataset (generated)
│
└── README.md
```


## How to Run (Jupyter Notebook)

All scraping is performed through the Jupyter Notebook located in the `notebooks/` directory.

### 1. Install dependencies

If using a virtual environment:

```bash
pip install -r requirements.txt
