import requests
from bs4 import BeautifulSoup

SAFE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_news(category):
    news_list = []
    urls = {
        "Top Stories": "https://www.karar.com/",
        "Economy": "https://www.karar.com/ekonomi-haberleri",
        "Sport": "https://www.karar.com/spor-haberleri"
    }
    try:
        res = requests.get(urls[category], headers=SAFE_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        headlines = soup.find_all(["h1", "h2", "h3", "span", "div"], class_=["title", "content", "box-title"])

        for h in headlines:
            text = h.get_text(strip=True)
            link = h if h.name == "a" else (h.find_parent("a") or h.find("a"))
            
            if text and len(text) > 20 and link:
                href = link['href']
                if href.startswith("/"):
                    href = f"https://www.karar.com{href}"
                
                if not any(d['title'] == text for d in news_list):
                    news_list.append({"title": text, "url": href})
            
            if len(news_list) >= 15: break
    except Exception as e:
        print(f"Karar Error: {e}")
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