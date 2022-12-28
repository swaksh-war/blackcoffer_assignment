import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import tqdm

#we will define this function to extract text from the urls that are in the xlsx file. this function can
# be used as standalone function
def fetch_data(file):
    links = pd.read_excel(file)
    working_url = []
    # Fetching Excel File and scrapping the data using request and beautifulsoup
    for url_id, url in tqdm.tqdm(zip(links['URL_ID'], links['URL'])):
        #we need to use User-Agent header to avoid 406 error.
        r = requests.get(url, headers={"User-Agent":"XY"})
        soup = BeautifulSoup(r.text, 'lxml')
        container = soup.find("div", class_ = 'td-post-content')
        #there is one url that is returning 404 page not found so have to appy if container != None
        if container != None:
            working_url.append(url)
            all_p_tags = container.find_all("p")
            text = ""
            for i in all_p_tags:
                st = i.string
                if st is not None:
                    text += st

            with open(f'blackcoffer_assignment/scraped/scraped_{url_id}.txt', 'w') as f:
                f.write(text)
    return working_url

# args = sys.argv
# file = args[1]