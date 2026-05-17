import requests
from bs4 import BeautifulSoup


SAFE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_news(category):
    news_list = []
    urls = {
        "Top Stories": "https://www.bbc.com/news",
        "Economy": "https://www.bbc.com/news/business",
        "Sport": "https://www.bbc.com/sport"
    }
    try:

        res = requests.get(urls[category], headers=SAFE_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        for h in soup.find_all(["h2", "h3"]):
            text = h.get_text(strip=True)
            link = h.find_parent("a") or h.find("a")
            
            if text and len(text) > 20 and link:
                href = link['href']
                if href.startswith("/"): 
                    href = f"https://www.bbc.com{href}"
                
                if not any(d['title'] == text for d in news_list):
                    news_list.append({"title": text, "url": href})
                    
            if len(news_list) >= 15: break
            
    except Exception as e:
        print(f"BBC Error: {e}")
        
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