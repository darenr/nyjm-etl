from BeautifulSoup import BeautifulSoup
import requests
import operator
import sys
import glob
import shutil

'''
  Takes scraped files of the NYJM collection, extracts from the meta og tags the work title and image url, then finds the description text and artist name.

  Note: unzip the raw/thejewishmuseum.zip files to some folder and pass this folder as the argument

  The result is json file of content

'''


headers = {
    'user-agent': 'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5'}


def get_page_soup(filename):
    with open(filename) as f:
        return BeautifulSoup(f.read())

def get_description(soup):
  # <div class="description">
  for div in soup.findAll("div", {"class": "description"}):
    return ' '.join(div.findAll(text=True))

def save_url_to_disk(url, filename):
  response = requests.get(url, stream=True)
  with open(filename, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
  del response

def get_works_title(soup):
  meta_title = soup.find('meta', attrs={"property": "og:title", 'content': True})
  return meta_title['content']


def get_main_image(soup):
  meta_image = soup.find('meta', attrs={"property": "og:image", 'content': True})
  return meta_image['content']

def process_collection(root):
    for filename in glob.iglob(root + '/[0-9]*.html'):
        soup = get_page_soup(filename)
        print get_description(soup)
        print get_main_image(soup)
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_collection(sys.argv[1])
