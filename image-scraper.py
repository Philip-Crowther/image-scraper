from bs4 import BeautifulSoup
import argparse
import urllib.request
import os

class ImageScraper():
    def __init__(self, args) -> None:
        self.args = args
    
    def run(self):
        # scrapes only the single page provided
        # make HTTP request and perform main operations
        with urllib.request.urlopen(args.url) as response:
            # finds images
            images = self.find_images(response)
            # cycle through and retrieve all images 
            count = 0
            for i in range(len(images)):
                url = self.check_url(images[i])
                if not url:
                    continue
                count += 1
                self.check_path(self.args.directory)
                self.save_image(url, self.args.directory, count)

    def find_images(self, response):
        # read HTML
        page = response.read()
        # parse HTML
        soup = BeautifulSoup(page, 'lxml')
        # find all images on page
        return soup.find_all('img')

    def check_url(self, image):
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

    # parse and return arguments
    return parser.parse_args()
        
if __name__ == '__main__':
    
    # get arguments
    args = get_arguments()
    # construct scraper
    scraper = ImageScraper(args)

    # scrape
    scraper.run()

