import requests as req
from bs4 import BeautifulSoup as bs

def get_page_soup(url:str,
                      search_term:str,
                      new_or_used:int = 1) -> bs:
    if new_or_used == 1:
        url = f"{url}/used-cars/search/"
    elif new_or_used == 2:
        url = f"{url}/new-cars/search/"

    url = f"{url}-/?q={search_term}"

    print(url)

    r = req.get(url)
    s = bs(r.content, "lxml")

    return s




if __name__ == "__main__":
    print("Starting to scrape")

    soup = get_page_soup("https://www.pakwheels.com", "rx8", 1)

    d = soup.find_all("a", {"class": "car-name"})

    for i in d:
        print(i.findChild("h3").text)