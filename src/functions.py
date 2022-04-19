from url import URL
import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import string

def get_urls(path):
    """Reading urls from /urls/urls.txt and returning list<URL> of urls"""
    urls = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            url_string = line.strip()
            url = URL(url_string)
            urls.append(url)

    return urls

def get_text_from_urls(urls: list) -> dict:
    """
        Collect text in 
            1) <title
            2) meta description
            3) <h1>...<h6> 
            4) <p>
        and collect data in dictionary
    """
    soups = []

    for url in urls:  
        if url.status_code == 200: 
            print(f"Analyzing url {url}")
            try:
                html = urlopen(url.url)
            except HTTPError as e:
                print(e)
            except URLError as e:
                print(e)
                
            try:
                soup = BeautifulSoup(html.read(), 'html.parser')
                soups.append(soup)
            except AttributeError as e:
                print(e)
        
    text_dict = {
        "title_tags": [],
        "meta_descriptions": [],
        "h_tags": [],
        "p_tags": [],
    }
    
    try:
        # Find all title tags
        for soup in soups:
            titles = soup.find_all('title')
            if titles:
                for title in titles:
                    text_dict["title_tags"].append(title.text.strip())
    except Exception as e:
        print(f"Error Title: {soup.title.string} -> {e}")

    try:
        # Find all meta descriptions
        for soup in soups:
            meta_description = soup.find('meta', attrs={'name':'description'})['content']
            text_dict["meta_descriptions"].append(meta_description)

    except Exception as e:
        print(f"Error Meta Description: {soup.title.string} -> {e}")

    try:
        # Find all heading-tag
        for soup in soups:
            for i in range(1,7):
                h_level = 'h' + str(i)
                h_tags = soup.find_all(h_level)
                if h_tags:
                    for h_tag in h_tags:
                        text_dict["h_tags"].append(h_tag.text.strip())
    except Exception as e:
        print(f"Error Heading: {soup.title.string} -> {e}")

    try:
        # Find all p-tag
        for soup in soups:
            p_tags = soup.find_all('p')
            if p_tags:
                for p_tag in p_tags:
                    text_dict["p_tags"].append(p_tag.text.strip())
    except Exception as e:
        print(f"Error Paragraph: {soup.title.string} -> {e}")

    return text_dict

def analyze_texts_from_urls(text_dict: dict) -> dict:
    """Returns dictionary with frequency of the words in text of the web page."""
    text = ""

    # Collect text in one string
    for v in text_dict.values():
        for entry in v:
            text += entry.strip().lower() + " "

    # Prepare text to list
    # TODO: remove stop words
    punctuations = string.punctuation
    punctuations += "«»1234567890"
    for character in punctuations:
        text = text.replace(character, " ")

    word_list = text.split(" ")

    # Analyze text
    word_counts = dict()
    for word in word_list:
        word = word.strip()
        if word and len(word) > 1:
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts

def create_dataframe(analysis: dict):
    data = {'Word': analysis.keys(), 'Count': analysis.values()}
    df = pd.DataFrame(data=data)
    df.sort_values(by="Count", ascending=False, inplace=True)
    return df

if __name__ == "__main__":
    urls = get_urls()
    text = get_text_from_urls(urls)
    analysis = analyze_texts_from_urls(text)
    df = create_dataframe(analysis)
