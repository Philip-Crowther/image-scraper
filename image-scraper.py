from bs4 import BeautifulSoup
import argparse
import urllib.request
import os

class ImageScraper():
    def __init__(self, args) -> None:
        self.args = args  # [directory, url]
        self.pages_to_visit = []
        self.visited_pages = set()
    
    def run(self):
        # make HTTP request and perform main operations
        with urllib.request.urlopen(self.args.url) as response:
            # read html into BeautifulSoup object
            soup = BeautifulSoup(response.read(), 'lxml')
            # scrape images
            self.scrape_images(soup, self.args.url)

    def run_recursive(self):
        # scrapes page provided and links on page with same domain
        self.pages_to_visit.append(args.url)
        # scrape until no more pages to visit
        while self.pages_to_visit:
            # get next page
            current_page = self.get_page()
            # make HTTP request and perform main operations 
            with urllib.request.urlopen(current_page) as response:
                # read html into BeautifulSoup object
                soup = BeautifulSoup(response.read(), 'lxml')
                # scrape images
                self.scrape_images(soup, current_page)
                # # add new pages to scrape to stack
                # self.find_links(current_page)
    
    def get_page(self):
        # get next page to visit
        current_page = self.pages_to_visit.pop()
        # add page to visited
        self.visited_pages.add(current_page)
        return current_page

    def scrape_images(self, soup, url):
        # finds images
        images = self.find_images(soup)
        #cycle through and retrieve all images 
        self.retrieve_images(url, images)

    def find_images(self, soup):
        # find all images on page
        return soup.find_all('img')

    def find_links(self, soup):
        # traverses page and finds unvisited links on the same domain
        pass

    def retrieve_images(self, url, images):
        # cycle through and retrieve all images
        count = 0
        for i in range(len(images)):
            url = self.check_url_for_source(images[i])
            if not url:
                continue
            count += 1
            self.check_path(self.args.directory)
            self.save_image(url, self.args.directory, count)

    def check_url_for_source(self, image):
        # check image for source: return nothing if not
        if 'src' not in image.attrs:
            return None
        # return image url
        return image.attrs['src']

    def check_path(self, path):
        # check if path/directory exists; build path if it doesn't
        if not os.path.isdir(path):
            os.mkdir(path)
    
    def save_image(self, url, directory, image_number=1):
        # prep file name/location
        location = os.path.join(directory, str(image_number) + '.jpg')
        # make request
        r = urllib.request.urlretrieve(url, location)

def get_arguments():
    # initialize argument parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument('directory', type=str)
    parser.add_argument('url', type=str)
    parser.add_argument('-r', '--recursive', action='store_const', const=True)

    # parse and return arguments
    return parser.parse_args()
        
if __name__ == '__main__':
    
    # get arguments
    args = get_arguments()
    # construct scraper
    scraper = ImageScraper(args)

    # scrape
    if args.recursive:
        # runs recursive version that finds other sites under same domain
        scraper.run_recursive()
    else:
        # runs the single site version
        scraper.run()

