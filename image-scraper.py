from bs4 import BeautifulSoup
import lxml
import argparse
import urllib.request
import shutil

def main():
    # initialize argument parser
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument('url', type=str)
    # parse arguments
    args = parser.parse_args()
    # make HTTP request and perform main operations
    with urllib.request.urlopen(args.url) as response:
        # read HTML
        page = response.read()
        # parse HTML
        soup = BeautifulSoup(page, "lxml")
        # find all images on page
        images = soup.find_all('img')
        # temp/testing: place image info into variable
        image = images[0]
        # place image url into variable
        url = image.attrs['src']
        # make image request/download image
        r = urllib.request.urlretrieve(url, 'filename.jpg')

        
            

if __name__ == "__main__":
    main()
