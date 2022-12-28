from bs4 import BeautifulSoup
import lxml
import argparse
import urllib.request
import os

def main():

    # initialize argument parser
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument('directory', type=str)
    parser.add_argument('url', type=str)
    # parse arguments
    args = parser.parse_args()

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

            # temp/testing: place image info into variable
            image = images[i]
            # check image for source: if it isn't, then go to next image
            if 'src' not in image.attrs:
                continue
            count += 1
            # place image url into variable
            url = image.attrs['src']

            # check if directory exists
            if not os.path.isdir(args.directory):
                # create directory if it doesn't exist
                os.mkdir(args.directory)
                

            # prep file name/location
            location = os.path.join(args.directory, str(count) + '.jpg')
            # make request
            r = urllib.request.urlretrieve(url, location)

        
if __name__ == '__main__':
    main()
