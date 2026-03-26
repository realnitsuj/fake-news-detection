import feedparser
from newspaper import Article
import pandas as pd
import os
import time

RSS_FEEDS = [
    "https://www.france24.com/fr/france/rss",
    "https://www.lemonde.fr/rss/une.xml"
]

def collect_trusted_news(limit_per_feed=10):
    all_news = []

    for url in RSS_FEEDS:
        print(f" Lecture du flux : {url}")
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:limit_per_feed]:
            try:
                
                article = Article(entry.link)
                article.download()
                article.parse()
                
                all_news.append({
                    "title": entry.title,
                    "text": article.text,
                    "source": url.split('/')[2], 
                    "date": entry.get('published', time.strftime('%Y-%m-%d'))
                })
                print(f" Récupéré : {entry.title[:50]}...")
            except Exception as e:
                print(f" Échec sur {entry.link}: {e}")

    
    df = pd.DataFrame(all_news)
    
    if os.path.exists("articles_vrais.csv"):
        df_old = pd.read_csv("articles_vrais.csv")
        df = pd.concat([df_old, df]).drop_duplicates(subset=['title'])
    
    df.to_csv("articles_vrais.csv", index=False)
    print(f"\n  {len(all_news)} articles sauvegardés dans articles_vrais.csv")

if __name__ == "__main__":
    collect_trusted_news()
