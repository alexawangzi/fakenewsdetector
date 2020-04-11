from bs4 import BeautifulSoup as soup  # HTML data structure
import urllib
from urllib.request import urlopen as uReq  # Web client
import json

def get_homepages(page_soup, url):
    sources = page_soup.find_all(
        lambda tag: tag.name == 'p' and (
                    tag.text.startswith('Sources:') or tag.text.startswith('Source:')))
    homepages = set()
    for source in sources:
        try:
            homepages.add(source.find("a")['href'])
        except TypeError:
            print("Unable to retrieve homepage from: " + str(source))

    if len(homepages) != 1:
        print("No sources/Multiple homepages detected for " + url)
        print(homepages)
        return ''
    else:
        return homepages.pop()


def get_name(page_soup, url):
    sources = page_soup.find_all(True, {"class": ["page-title-layout1", "page-title"]})
    names = set()

    for source in sources:
        try:
            names.add(source.text)
        except TypeError:
            print("Unable to retrieve name from: " + str(source))

    if len(names) != 1:
        print("No sources/Multiple names detected for " + url)
        print(names)
        return ''
    else:
        return names.pop()


# URl to web scrap from.
page_url = "https://mediabiasfactcheck.com"

# categories of sources, each is a page
categories = ["leftcenter", "center", "right-center", "right", "pro-science", "conspiracy", "fake-news", "satire", "left" ]

# name the output file to write to local disk
out_filename = "biases.csv"
# header of csv file to be written
headers = "category,homepage \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# .json container
biases = {}

# loops over each product and grabs attributes about
# each product
for category in categories:
    # opens the connection and downloads html page from url
    uClient = uReq(page_url + "/" + category)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()

    # Finds all sites within the specific category
    rows = page_soup.find("table", {"id": "mbfc-table"}).findChildren('tr')

    # Finds all the urls of the sites
    urls = list()
    for site in rows:
        try:
            urls.append(site.find("a")['href'])
        except TypeError:
            print("Skipping non-entry row")

    # prints the dataset to console
    print("category: " + category)
    print("number of sites: " + str(len(urls)))
    print("first: " + urls[0])
    print("last: " + urls[len(urls) - 1])

    # go to specific url and grab the homepage

    for url in urls:

        try:
            uClient = uReq(url)
            page_soup = soup(uClient.read(), "html.parser")
            uClient.close()
        except urllib.error.HTTPError:
            print('HTTPError! Skipping url: ' + url)
            continue
        except urllib.error.URLError:
            print('URLError! Skipping url: ' + url)
            continue
        except urllib.error.ContentTooShortError:
            print('ContenTooShortError! Skipping url: ' + url)
            continue
        except:
            print('Unclear error! Skipping url: ' + url)
            continue

        name = get_name(page_soup, url)
        homepage = get_homepages(page_soup, url)

        if name == '' or homepage == '':
            continue


        # writes the dataset to .csv
        f.write(homepage + ", " + name + "," + category + "\n")

        # writes the dataset to json
        biases[homepage] = []
        biases[homepage].append({
            'name': name,
            'category': category,
        })

        print("Added: " + category + ": " + name)


f.close()  # Close the .csv file

with open('biases.txt', 'w') as outfile:
    json.dump(biases, outfile)


