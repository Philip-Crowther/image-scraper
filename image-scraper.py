from bs4 import BeautifulSoup
import lxml
import argparse
import urllib.request
import os

class ImageScraper():
    def __init__(self, args) -> None:
        self.args = args
        self.pages_to_visit = []
        self.visited_pages = set()
    
    def run(self):
        # scrapes only the single page provided
        # make HTTP request and perform main operations
        with urllib.request.urlopen(args.url) as response:

            # read HTML
            page = response.read()
            # parse HTML
            soup = BeautifulSoup(page, 'lxml')
            # find all images on page
            images = soup.find_all('img')

            count = 0
            #cycle through and retrieve all images 
            for i in range(len(images)):

                # check image for source: if there isn't one, then go to next image
                if 'src' not in images[i].attrs:
                    continue
                count += 1

                # get image url
                url = images[i].attrs['src']

                self.check_path(self.args.directory)
                self.save_image(url, self.args.directory, count)

    def run_recursive(self):
        # scrapes page provided and links on page with same domain
        pass

    @staticmethod
    def check_path(path):
        # check if path/directory exists; build path if it doesn't
        if not os.path.isdir(path):
            os.mkdir(path)
    
    @staticmethod
    def save_image(url, directory, image_number=1):
        # prep file name/location
        location = os.path.join(directory, str(image_number) + '.jpg')
        # make request
        r = urllib.request.urlretrieve(url, location)

        
if __name__ == '__main__':

    # initialize argument parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument('directory', type=str)
    parser.add_argument('url', type=str)
    parser.add_argument('-r', '--recursive', action='store_const', const=True)

    # parse arguments
    args = parser.parse_args()

    # construct scraper
    scraper = ImageScraper(args)

    # scrape
    if args.recursive:
        # runs recursive version that finds other sites under same domain
        scraper.run_recursive()
    else:
        # runs the single site version
        scraper.run()

