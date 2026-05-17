import requests
from bs4 import BeautifulSoup

SAFE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_news(category):
    news_list = []
    urls = {
        "Top Stories": "https://www.independent.co.uk/news/world",
        "Economy": "https://www.independent.co.uk/news/business",
        "Sport": "https://www.independent.co.uk/sport"
    }
    try:
        res = requests.get(urls[category], headers=SAFE_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        headlines = soup.find_all(["h2", "h3", "a"], class_=lambda x: x and ("title" in x or "headline" in x) or not x)

        for item in headlines:
            link = item if item.name == "a" else item.find("a")
            if link:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                
                if text and len(text) > 25 and href:
                    if href.startswith("/"): 
                        href = f"https://www.independent.co.uk{href}"
                    
                    if not any(d['title'] == text for d in news_list):
                        news_list.append({"title": text, "url": href})
            
            if len(news_list) >= 15: break
            
    except Exception as e:
        print(f"Independent Error: {e}")
        
    return news_list

def get_content(url):
    try:
        res = requests.get(url, headers=SAFE_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        paragraphs = soup.find_all("p")
        content_list = []
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 40: 
                content_list.append(text)
            if len(content_list) == 3: 
                break
                
        summary = "\n\n".join(content_list)
        return summary if summary else "Summary content not found on the page."
        
    except Exception as e:
        return f"Error while fetching summary: {str(e)}"