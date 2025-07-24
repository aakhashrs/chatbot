import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,  # Increased retries
        backoff_factor=2,  # Increased backoff
        status_forcelist=[500, 502, 503, 504, 599]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Add headers to mimic a browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    return session

def scrape_url(url, delay=2):
    try:
        print(f"Scraping {url}...")
        time.sleep(delay)
        
        session = create_session()
        response = session.get(url, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple content areas with more specific selectors
        content_selectors = [
            'div.content-wrapper',
            'div.content',
            'div#content',
            'div.main-content',
            'div#main-content',
            'article',
            'main',
            'div.catalog-content',  # Specific to catalog pages
            'div.program-content'   # Specific to program pages
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
                
        if not main_content:
            main_content = soup.find('body')
        
        content_data = {
            "url": url,
            "title": soup.title.string if soup.title else "",
            "content": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Extract content with better filtering
        for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'div.text', 'table']):
            # Skip navigation and footer elements
            if any(skip in str(element.get('class', [])) for skip in ['nav', 'footer', 'menu', 'sidebar']):
                continue
                
            text = element.get_text(strip=True)
            if text and len(text) > 20:
                content_data["content"].append(text)
        
        if content_data["content"]:
            print(f"Found {len(content_data['content'])} content blocks")
            return content_data
            
        print(f"Warning: No content found on {url}")
        return None
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def create_vector_store(scraped_data):
    documents = []
    for page in scraped_data:
        content = page["content"]
        if content:
            text = " ".join(content)
            text += f"\nSource: {page['url']}"
            documents.append(text)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vector_store = FAISS.from_texts(documents, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def main():
    # Updated URLs that are directly accessible
    urls = [
        "https://jindal.utdallas.edu/",
        "https://jindal.utdallas.edu/about-the-jindal-school-of-management/",
        "https://jindal.utdallas.edu/admission-requirements/",
        "https://jindal.utdallas.edu/academics/",
        "https://infosystems.utdallas.edu/ms-ba-options/",
        "https://infosystems.utdallas.edu/ms-business-analytics/",
        "https://infosystems.utdallas.edu/ms-business-analytics-cohort/",
        "https://infosystems.utdallas.edu/ms-business-analytics-cohort/data-science/",
        "https://infosystems.utdallas.edu/ms-business-analytics-cohort/scholarships/",
        "https://infosystems.utdallas.edu/ms-business-analytics-cohort/application-process/",
        "https://jindal.utdallas.edu/faculty/gaurav-shekhar/",
        "https://infosystems.utdallas.edu/ms-business-analytics-cohort/contact/"
    ]
    
    scraped_data = []
    
    # Scrape URLs
    print("Scraping URLs...")
    for url in urls:
        content = scrape_url(url)
        if content:
            scraped_data.append(content)
            print(f"✓ Successfully scraped {url}")
        else:
            print(f"✗ Failed to scrape {url}")
    
    if not scraped_data:
        print("Error: No data was successfully scraped!")
        return
    
    # Save raw data
    with open('utd_data.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    print(f"\nScraped data saved to utd_data.json")
    
    # Create vector store
    create_vector_store(scraped_data)
    print("Vector store created in faiss_index/")

if __name__ == "__main__":
    main() 
# import json
# import requests
# import os
# from bs4 import BeautifulSoup
# from datetime import datetime
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_core.documents import Document
# import time
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry

# def create_session():
#     session = requests.Session()
#     retry = Retry(
#         total=5,
#         backoff_factor=2,
#         status_forcelist=[500, 502, 503, 504, 599]
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#     session.headers.update({
#         'User-Agent': 'Mozilla/5.0',
#         'Accept': 'text/html',
#         'Accept-Language': 'en-US,en;q=0.5',
#     })
#     return session

# def scrape_url(url, delay=2):
#     try:
#         print(f"Scraping {url}...")
#         time.sleep(delay)
#         session = create_session()
#         response = session.get(url, timeout=60)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         selectors = [
#             'div.content-wrapper', 'div.content', 'div#content',
#             'div.main-content', 'div#main-content', 'article',
#             'main', 'div.catalog-content', 'div.program-content'
#         ]
#         main_content = None
#         for selector in selectors:
#             main_content = soup.select_one(selector)
#             if main_content:
#                 break
#         if not main_content:
#             main_content = soup.find('body')

#         content_data = {
#             "url": url,
#             "title": soup.title.string if soup.title else "",
#             "content": [],
#             "timestamp": datetime.now().isoformat()
#         }

#         for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li']):
#             if any(skip in str(element.get('class', [])) for skip in ['nav', 'footer', 'menu', 'sidebar']):
#                 continue
#             text = element.get_text(strip=True)
#             if text and len(text) > 20:
#                 content_data["content"].append(text)

#         return content_data if content_data["content"] else None

#     except Exception as e:
#         print(f"Error scraping {url}: {str(e)}")
#         return None

# def create_vector_store(scraped_data):
#     documents = []
#     for page in scraped_data:
#         for chunk in page["content"]:
#             documents.append(
#                 Document(
#                     page_content=chunk,
#                     metadata={
#                         "url": str(page.get("url", ""))[:300],  # ensure flat & short
#                         "title": str(page.get("title", ""))[:200]
#                     }
#                 )
#             )

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2",
#         model_kwargs={"device": "cpu"}
#     )

#     vector_store = FAISS.from_documents(documents, embeddings)

#     os.makedirs("data", exist_ok=True)
#     vector_store.save_local("data/faiss_index")
#     print("✓ FAISS index saved at data/faiss_index")

# def main():
#     urls = [
#         "https://jindal.utdallas.edu/",
#         "https://jindal.utdallas.edu/about-the-jindal-school-of-management/",
#         "https://jindal.utdallas.edu/admission-requirements/",
#         "https://jindal.utdallas.edu/academics/",
#         "https://infosystems.utdallas.edu/ms-ba-options/",
#         "https://infosystems.utdallas.edu/ms-business-analytics/",
#         "https://infosystems.utdallas.edu/ms-business-analytics-cohort/",
#         "https://infosystems.utdallas.edu/ms-business-analytics-cohort/data-science/",
#         "https://infosystems.utdallas.edu/ms-business-analytics-cohort/scholarships/",
#         "https://infosystems.utdallas.edu/ms-business-analytics-cohort/application-process/",
#         "https://jindal.utdallas.edu/faculty/gaurav-shekhar/",
#         "https://infosystems.utdallas.edu/ms-business-analytics-cohort/contact/"
#     ]

#     scraped_data = []
#     print("🔍 Starting scrape...")

#     for url in urls:
#         content = scrape_url(url)
#         if content:
#             scraped_data.append(content)
#             print(f"✓ Scraped: {url}")
#         else:
#             print(f"✗ Failed: {url}")

#     if not scraped_data:
#         print("🚫 No pages scraped.")
#         return

#     os.makedirs("data", exist_ok=True)
#     with open("data/utd_data.json", "w", encoding="utf-8") as f:
#         json.dump(scraped_data, f, indent=2, ensure_ascii=False)

#     print("📝 Scraped data saved to data/utd_data.json")

#     create_vector_store(scraped_data)

# if __name__ == "__main__":
#     main()
