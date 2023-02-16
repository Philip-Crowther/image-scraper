from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
import urllib.request
import os


class ImageScraper():
    def __init__(self, args) -> None:
        self.args = args  # [directory, url]
        self.parsed_url = urlparse(args.url)  # named tuple - some items: scheme ('html'), netloc (domain), path
        self.pages_to_visit = []
        self.visited_pages = set()
        self.check_path(args.directory)
    
    def run(self):
        # make HTTP request and perform main operations
        with urllib.request.urlopen(self.args.url) as response:
            # read html into BeautifulSoup object
            soup = BeautifulSoup(response.read(), 'lxml')
            # scrape images
            self.scrape_images(soup, self.args.url)

    def run_recursive(self):  # TODO: add limiter to stop search from running for too long
        # scrapes page provided and links on page with same domain
        self.pages_to_visit.append(args.url)
        # scrape until no more pages to visit
        while self.pages_to_visit:
            # get next page (also adds page to visted_pages)
            current_page = self.get_page()
            # skips pages that return errors  # TODO: replace
            try:
                # make HTTP request and perform main operations 
                with urllib.request.urlopen(current_page) as response:
                    # read html into BeautifulSoup object
                    soup = BeautifulSoup(response.read(), 'lxml')
                    # scrape images
                    self.scrape_images(soup, current_page)
                    # find new pages to add to stack
                    self.find_links(soup)
            except:
                continue
    
    def get_page(self):
        # get next page to visit
        current_page = self.pages_to_visit.pop()
        # add page to visited
        self.visited_pages.add(current_page)
        return current_page
 
    def find_images(self, soup):
        # find all images on page
        return soup.find_all('img')

    def find_links(self, soup): 
        # traverses page and finds valid links to add to pages to visit
        links = []
        # find all links on the page
        for link in soup.find_all('a'): 
            links.append(link.get('href'))
        # iterate through links, test if it's on the same domain, then if it's been visited
        for i in range(len(links)):
            # make sure link is full
            link = self.build_absolute_link(links[i]) if self.is_relative_link(links[i]) else links[i]
            # check if link is valid
            if self.link_valid(link):
                # add to pages to visit
                self.pages_to_visit.append(link)

    def build_absolute_link(self, link):
        # returns absolute link from relative
        base = self.parsed_url.scheme + '://' + self.parsed_url.netloc
        if not link:
            return base
        if link[0] != '/':
            link = '/' + link
        return base + link
    
    def is_relative_link(self, link):  
        # return True if link is relative
        return not urlparse(link).netloc

    def link_valid(self, link):
        # check to see if the link has been visited before
        if link in self.visited_pages:
            return False
        # check to see if it's on the same domain
        if not self.same_domain(link):
            return False
        return True

    def same_domain(self, link):
        # test if provided link is on the same domain as the link passed during init
        parsed= urlparse(link)
        return self.parsed_url.netloc == parsed.netloc and self.parsed_url.scheme == parsed.scheme

    def scrape_images(self, soup, url):
        # finds images
        images = self.find_images(soup)
        # director
        directory = os.path.join(self.args.directory, soup.title.string)
        # ensure that the current planned directory exists
        self.check_path(directory)
        #cycle through and retrieve all images 
        self.retrieve_images(url, images, directory)

    def retrieve_images(self, url, images, directory): 
        # cycle through and retrieve all images
        count = 0
        for i in range(len(images)):
            url = self.check_url_for_source(images[i])
            if not url:
                continue
            count += 1
            self.save_image(url, directory, count)

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

