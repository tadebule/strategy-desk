import feedparser
import json
import os
from datetime import datetime

# Define the RSS feeds for the firms
FEEDS = {
    'McKinsey & Company': 'https://www.mckinsey.com/insights/rss',
    'BCG': 'https://www.bcg.com/rss.aspx',
    'Bain & Company': 'https://www.bain.com/insights/index.xml'
}

def fetch_insights():
    all_articles = []
    
    for firm, url in FEEDS.items():
        print(f"Fetching updates from {firm}...")
        try:
            # Parse the RSS feed
            feed = feedparser.parse(url)
            
            # Grab the 5 most recent articles from each firm
            for entry in feed.entries[:5]:
                # Standardize publication date tracking
                pub_date = entry.get('published', datetime.now().strftime('%b %d, %Y'))
                
                article_data = {
                    'firm': firm,
                    'title': entry.get('title', 'No Title Available'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', 'No summary provided. Visit link to read.'),
                    'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                all_articles.append(article_data)
                
        except Exception as e:
            print(f"Error reading feed for {firm}: {e}")
            
    return all_articles

def save_data(data):
    # This creates/overwrites a JSON file that your frontend dashboard will read later
    output_file = 'data_signals.json'
    
    output_payload = {
        "last_updated": datetime.now().strftime('%B %d, %Y at %I:%M %p'),
        "articles": data
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_payload, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {len(data)} articles to {output_file}")

if __name__ == "__main__":
    insights = fetch_insights()
    save_data(insights)