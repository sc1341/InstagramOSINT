#! /usr/bin/env python3
# Instagram Scraper
# Coded by sc1341 
# http://github.com/sc1341/InstagramOSINT
# I am not responsible for anything you do with this script
# This is mean to be imported as a python module for use in custom applications
#
#

from bs4 import BeautifulSoup
import json
import os
import requests
import random
import string
import sys
import time


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InstagramOSINT:

    def __init__(self, username):
        self.username = username
        self.useragents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

        self.scrape_profile()


    def __repr__(self):
        return f"Current Username: {self.username}"

    def __str__(self):
        return f"Current Username: {self.username}"

    def __getitem__(self, i):
        return self.profile_data[i]


    def scrape_profile(self):
        """
        This is the main scrape which takes the profile data retrieved and saves it into profile_data
        :params: None
        :return: profile data
        """
        # Get the html data with the requests module
        r = requests.get(f'http://instagram.com/{self.username}', headers={'User-Agent': random.choice(self.useragents)})
        soup = BeautifulSoup(r.text, 'html.parser')
        # Find the tags that hold the data we want to parse
        general_data = soup.find_all('meta', attrs={'property': 'og:description'})
        more_data = soup.find_all('script', attrs={'type': 'text/javascript'})
        description = soup.find('script', attrs={'type': 'application/ld+json'})
        # Try to parse the content -- if it fails then the program exits
        try:
            text = general_data[0].get('content').split()
            self.description = json.loads(description.get_text())
            self.profile_meta = json.loads(more_data[3].get_text()[21:].strip(';'))

        except:
            print(colors.FAIL + f"Username {username} not found" + colors.ENDC)
            return 1
        self.profile_data = {"Username": self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
                             "Profile name": self.description['name'],
                             "URL": self.description['mainEntityofPage']['@id'],
                             "Followers": text[0], "Following": text[2], "Posts": text[4],
                             "Bio": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['biography']),
                             "profile_pic_url": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'profile_pic_url_hd']),
                             "is_business_account": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                     'is_business_account']),
                             "connected_to_fb": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'connected_fb_page']),
                             "externalurl": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
                             "joined_recently": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'is_joined_recently']),
                             "business_category_name": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                     'business_category_name']),
                             "is_private": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
                             "is_verified": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}

        return self.profile_data


    def scrape_posts(self):
        """Scrapes all posts and downloads them
        :return: none
        :param: none
        """
        if self.profile_data['is_private'].lower() == 'true':
            print("[*]Private profile, cannot scrape photos!")
            return 1
        else:
            posts = {}
            for index, post in enumerate(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']):
                os.mkdir(str(index))
                posts[index] = {"Caption": str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
                                "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                                "Comments Disabled": str(post['node']['comments_disabled']),
                                "Taken At Timestamp": str(post['node']['taken_at_timestamp']),
                                "Number of Likes": str(post['node']['edge_liked_by']['count']),
                                "Location": str(post['node']['location']),
                                "Accessability Caption": str(post['node']['accessibility_caption'])
                                }

                # Downloads the thumbnails of the post
                # Picture is just an int index of the url in the list
                with open(f'{os.getcwd()}/{index}/' + ''.join([random.choice(string.ascii_uppercase) for x in range(random.randint(1, 9))]) + '.jpg', 'wb') as f:
                    # Delay the request times randomly (be nice to Instagram)
                    time.sleep(random.randint(5, 10))
                    r = requests.get(post['node']['thumbnail_resources'][0]['src'], headers={'User-Agent':random.choice(self.useragents)})
                    # Takes the content of r and puts it into the file
                    f.write(r.content)

            with open('posts.txt', 'w') as f:
                f.write(json.dumps(posts))

    def make_directory(self):
        """Makes the profile directory and changes the cwd to it
        this should only be called from the save_data function!
        :return: True
        """
        try:
            os.mkdir(self.username)
            os.chdir(self.username)
        except FileExistsError:
            num = 0
            while os.path.exists(self.username):
                num += 1
                try:
                    os.mkdir(self.username + str(num))
                    os.chdir(self.username + str(num))
                except FileExistsError:
                    pass

    def save_data(self):
        """Saves the data to the username directory
        :return: none
        :param: none
        """
        self.make_directory()
        with open('data.txt', 'w') as f:
            f.write(json.dumps(self.profile_data))
        # Downloads the profile Picture
        self.download_profile_picture()
        print(f"Saved data to directory {os.getcwd()}")

    def print_profile_data(self):
        """Prints out the data to the screen by iterating through the dict with it's key and value
        :return: none
        :param: none
        """
        # Print the data out to the user
        print(colors.HEADER + "---------------------------------------------" + colors.ENDC)
        print(colors.OKGREEN + f"Results: scan for {self.profile_data['Username']} on instagram" + colors.ENDC)
        for key, value in self.profile_data.items():
            print(key + ':' + value)

    def download_profile_picture(self):
        """Downloads the profile pic and saves it to the directory
        :return: none
        :param: none
        """
        with open("profile_pic.jpg", "wb") as f:
            time.sleep(1)
            r = requests.get(self.profile_data['profile_pic_url'], headers={'User-Agent':random.choice(self.useragents)})
            f.write(r.content)

