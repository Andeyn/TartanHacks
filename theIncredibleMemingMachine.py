from imageai.Detection import ObjectDetection
import os
import argparse
import json
import itertools
import logging
import re
import os
import uuid
import random
import sys
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = configure_logging()

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query

def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    return link_type_records

def extract_images(query, num_images):
    url = get_query_url(query)
    logger.info("Souping")
    soup = get_soup(url, REQUEST_HEADER)
    logger.info("Extracting image urls")
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)

def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'
    file_name = str(uuid.uuid4().hex) + "." + extension
    save_path = os.path.join(save_directory, file_name)
    with open(save_path, 'wb+') as image_file:
        image_file.write(raw_image)

def download_images_to_dir(images, save_directory, num_images):
    for i, (url, image_type) in enumerate(images):
        try:
            logger.info("Making request (%d/%d): %s", i, num_images, url)
            raw_image = get_raw_image(url)
            save_image(raw_image, image_type, save_directory)
        except Exception as e:
            logger.exception(e)

def run(query, save_directory, num_images=100):
    query = '+'.join(query.split())
    logger.info("Extracting image links")
    images = extract_images(query, num_images)
    logger.info("Downloading images")
    download_images_to_dir(images, save_directory, num_images)
    logger.info("Finished")
    
    
def get_key(num1, num2, noun_path, adj_path):
    lines1 = open(noun_path).read().splitlines()
    noun = lines1[num1]
    #noun = "meme"
    lines2 = open(adj_path).read().splitlines()
    adj = lines2[num2]
    list = ["person", "food", "meme", "clothes", "animal", "instrument","depression", "andeyng", "hack", "CMU","farnam"]
    return noun + " " + adj + " " + random.choice(list)

    
def generateImg():
    num_random_images = 1
    for i in range(num_random_images):
        keyword = get_key(random.randint(0, 4600), random.randint(0, 1340),"C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\nounlist.txt", "C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\adjlist.txt")
        print("""
        ______________________________________
        noun = """ + keyword + """
        ______________________________________
        """)
        parser = argparse.ArgumentParser(description='Scrape Google images')
        parser.add_argument('-s', '--search', default=keyword, type=str, help='search term')
        parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
        parser.add_argument('-d', '--directory', default="C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages", type=str, help='save directory')
        args = parser.parse_args()
        run(args.search, args.directory, args.num_images)


    
def detectObj():
    execution_path = os.getcwd()
    detector = ObjectDetection()    
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    execution_path = os.path.join(execution_path, "ObjectDetection")
    execution_path = os.path.join(execution_path, "googleImages")
    
    print(execution_path)
    detections = detector.detectObjectsFromImage(input_image = os.path.join(execution_path, os.listdir("C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages")[0]),    output_image_path=os.path.join(execution_path , "output.jpg"))
    
    result = []

    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        result.append(eachObject["name"])
    
    print(execution_path)
    
    os.remove(os.path.join(execution_path, os.listdir("C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages")[0]))
    os.remove(os.path.join(execution_path, os.listdir("C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages")[0]))
        
    return result
    
def main():
    generateImg()
    detectObj()
    os.remove(os.path.join(execution_path, os.listdir("C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages")[0]))
    os.remove(os.path.join(execution_path, os.listdir("C:\\Users\\Tim\\Documents\\Github\\TartanHacks\\ObjectDetection\\googleImages")[0]))
    

if __name__ == '__main__':
    main()
    