import feedparser
import json
import datetime
import os
import requests

# Trusted Sources RSS Feeds
SOURCES = {
    "Google News": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reddit WorldNews": "https://www.reddit.com/r/worldnews/.rss",
    "Reuters (World)": "https://www.reutersagency.com/feed/?best-topics=world-news&post_type=best",
}

def calculate_reliability(source):
    high_reliability = ["Reuters", "BBC", "AP News", "Google News"]
    if any(s in source for s in high_reliability):
        return "High"
    return "Medium"

def assess_risk(title, summary):
    # Very basic heuristic for risk level
    critical_keywords = ["war", "crisis", "attack", "death", "blast", "killed", "emergency", "crash"]
    urgent_keywords = ["urgent", "breaking", "alert", "threat"]
    
    combined = (title + " " + summary).lower()
    
    if any(k in combined for k in critical_keywords):
        return "High"
    elif any(k in combined for k in urgent_keywords):
        return "Medium"
    return "Low"

def fetch_latest_news():
    all_news = []
    
    for source_name, url in SOURCES.items():
        print(f"Fetching from {source_name}...")
        try:
            # For Reddit, we need a User-Agent or it might block us
            headers = {"User-Agent": "NewsIntelligenceAgent/1.0"}
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:5]: # Take top 5 from each source
                # Basic cleaning/neutrality filter (stub)
                # In a real scenario, this would call an LLM to verify neutrality
                
                news_item = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("description", entry.get("summary", "")).split('<')[0], # Basic HTML strip
                    "full_text": entry.get("link", ""), # Link acts as reference
                    "source": source_name,
                    "published_at": entry.get("published", ""),
                    "category": entry.get("category", "General"),
                    "reliability_score": calculate_reliability(source_name),
                    "risk_level": assess_risk(entry.get("title", ""), entry.get("summary", ""))
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"Error fetching from {source_name}: {e}")
            
    return all_news

def main():
    news_data = fetch_latest_news()
    
    # Save to a daily file
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    output_dir = "news_reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, f"news_{date_str}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(news_data)} news items to {file_path}")

if __name__ == "__main__":
    main()
