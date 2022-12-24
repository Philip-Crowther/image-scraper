from bs4 import BeautifulSoup
import lxml
import argparse
import urllib.request
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    with urllib.request.urlopen(args.url) as response:
        page = response.read()
        soup = BeautifulSoup(page, "lxml")
        images = soup.find_all('img')
        image = images[0]
        url = image.attrs['src']
        r = urllib.request.urlretrieve(url, 'filename.jpg')

        
            

if __name__ == "__main__":
    main()
