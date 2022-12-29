from bs4 import BeautifulSoup
import lxml
import argparse
import urllib.request
import os

def main():

    def get_arguments():
        # initialize argument parser
        parser = argparse.ArgumentParser()
        # add arguments
        parser.add_argument('directory', type=str)
        parser.add_argument('url', type=str)
        # parse arguments
        return parser.parse_args()

    args = get_arguments()
    
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

            def check_path(path):
                # check if path/directory exists
                if not os.path.isdir(path):
                    # create directory if it doesn't exist
                    os.mkdir(path)
                
            def save_image(url, directory, count):
                # prep file name/location
                location = os.path.join(directory, str(count) + '.jpg')
                # make request
                r = urllib.request.urlretrieve(url, location)

            check_path(args.directory)
            save_image(url, args.directory, count)

        
if __name__ == '__main__':
    main()
