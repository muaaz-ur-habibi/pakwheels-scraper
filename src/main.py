import requests as req
from bs4 import BeautifulSoup as bs

def get_page_soup(url:str,
                      search_term:str,
                      new_or_used:int = 1,
                      page_num:int = 1) -> bs:
    if new_or_used == 1:
        url = f"{url}/used-cars/search/"
    elif new_or_used == 2:
        url = f"{url}/new-cars/search/"

    if page_num != 1:
        url = f"{url}-/?q={search_term}&page={page_num}"
    else:
        url = f"{url}-/?q={search_term}"

    r = req.get(url)
    s = bs(r.content, "lxml")

    return s

def scrape_used_cars_page(soup:bs, url:str):
    try:
        total_pages = int(soup.find("li", {"class", "last next"}).findChild("a")['href'].split("=")[-1])
    except AttributeError:
        print("Error occured trying to get total number of pages. Defaulting to 1")
        total_pages = 1
    #total_pages = 2
    
    p = [str(i.text).replace("\n", "").strip()[4:] for i in soup.find_all("div", {"class": "price-details"})]
    d = soup.find_all("a", {"class": "car-name"})
    actual_data = [f'{i.findChild("h3").text}, f"{url}{i["href"]}", {p[idx]}' for idx, i in enumerate(d)]

    return actual_data, total_pages

def SCRAPE_FROM_USED_CAR(search_term:str,
                         new_or_used:int):
    url = "https://www.pakwheels.com"
    total_data = []

    search_term = search_term.replace(" ", "+")

    soup = get_page_soup(url, search_term, new_or_used)
    data_from_page, pages_to_scrape = scrape_used_cars_page(soup, url)

    total_data = total_data + data_from_page

    for i in range(1, pages_to_scrape):
        soup = get_page_soup(url, search_term, new_or_used, i)
        data_from_page, _ = scrape_used_cars_page(soup, url)

        total_data = total_data + data_from_page

    return total_data

def pretty_print_data(data:list):
    
    for d in data:
        print(
            f"Name: {d[0]}   for {d[2]}\nURL: {d[1]}\n\n"
        )

def save_data_to_file(file_path:str,
                      data_list:list) -> None:
    with open(file_path, "w") as file:
        for data in data_list:
            file.write(data)

    file.close()

if __name__ == "__main__":
    print("Starting to scrape")

    # 1 is used, 2 is new
    search_for = input("Enter the car name to search for: ")

    print(f"Scraping used {search_for}s")
    save_data_to_file("used_cars.txt", SCRAPE_FROM_USED_CAR(search_for, 1))
    #pretty_print_data(SCRAPE_FROM_USED_CAR(search_for, 1))