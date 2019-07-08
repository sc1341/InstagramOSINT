#! /usr/bin/env python3
# Instagram Scraper
import argparse
from banner import banner
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


class Scraper:

    def __init__(self, username):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
        self.profile_data = {}
        self.username = username
        self.make_directory()
        self.scrape(self.username)
        self.print_data()
        self.save_data()



    def scrape(self, username: str):
        """Takes a username as a string to find information about that person's instagram profile, a random
        user agent is picked to spoof when the data is collected
        :return: none
        :param: username: str
        """
        print("[*] Starting Scan")
        # Get the html data with the requests module
        r = requests.get(f'http://instagram.com/{username}', headers={'User-Agent': random.choice(self.user_agents)})
        soup = BeautifulSoup(r.text, 'html.parser')
        # Find the tags that hold the data we want to parse
        general_data = soup.find_all('meta', attrs={'property': 'og:description'})
        more_data = soup.find_all('script', attrs={'type': 'text/javascript'})
        description = soup.find('script', attrs={'type': 'application/ld+json'})
        # Try to parse the nessicary content but if it fails, then user != exist
        try:
            text = general_data[0].get('content').split()
            # Get the json data held inside of the <script> type="applicaiton/il/json"
            description = json.loads(description.get_text())
            profile_meta = json.loads(more_data[3].get_text()[21:].strip(';'))

        except:
            print(colors.FAIL + f"Username {username} not found" + colors.ENDC)
            sys.exit()

        # If the user does not have anything in their bio, the value will not be in the json dump
        # So we just set the bio to an empty string
        # I don't know if I still need this try/catch block atm
        try:
            self.profile_data = {"Username": text[-1], "Profile name": description['name'],
                                 "URL": description['mainEntityofPage']['@id'],
                                 "Followers": text[0], "Following": text[2], "Posts": text[4],
                                 "Bio": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['biography']),
                                 "profile_pic_url": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'profile_pic_url_hd']),
                                 "is_business_account": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                         'is_business_account']),
                                 "connected_to_fb": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'connected_fb_page']),
                                 "externalurl": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
                                 "joined_recently": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'is_joined_recently']),
                                 "business_category_name": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                         'business_category_name']),
                                 "is_private": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
                                 "is_verified": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}
        except KeyError:
            self.profile_data = {"Username": text[-1], "Profile name": description['name'],
                                 "URL": description['mainEntityofPage']['@id'],
                                 "Followers": text[0], "Following": text[2], "Posts": text[4],
                                 "Bio": '',
                                 "profile_pic_url": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'profile_pic_url_hd']),
                                 "is_business_account": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                         'is_business_account']),
                                 "connected_to_fb": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'connected_fb_page']),
                                 "externalurl": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
                                 "joined_recently": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                            'is_joined_recently']),
                                 "business_category_name": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                         'business_category_name']),
                                 "is_private": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
                                 "is_verified": str(
                                     profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}
        # Tries to scrape posts if it is a public profile
        self.scrape_posts(profile_meta)


    def scrape_posts(self, profile_meta: str):
        """Scrapes all posts and downloads thumbnails when necessary
        :return: none
        """
        if self.profile_data['is_private'].lower() == 'true':
            print("Private profile, cannot scrape photos!")
        else:
            posts = {}
            for index, post in enumerate(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']):
                posts[index] = {"Caption": str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
                                "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                                "Comments Disabled": str(post['node']['comments_disabled']),
                                "Taken At Timestamp": str(post['node']['taken_at_timestamp']),
                                "Number of Likes": str(post['node']['edge_liked_by']['count']),
                                "Location": str(post['node']['location']),
                                "Accessability Caption": str(post['node']['accessibility_caption'])
                                }

                # Downloads the thumbnails of the post
                for url in post['node']['thumbnail_resources']:
                    # Picture is just an int index of the url in the list
                    with open(''.join([random.choice(string.ascii_uppercase) for x in range(random.randint(1, 9))]) + '.jpg', 'wb') as f:
                        # Delay the request times randomly (be nice to Instagram)
                        time.sleep(random.randint(2, 16))
                        r = requests.get(url['src'])
                        f.write(r.content)
                        print("Got an Image")

            with open('posts.txt', 'w') as f:
                f.write(json.dumps(posts))


    def make_directory(self):
        """Makes the profile directory and changes the cwd to it
        :return: True
        """
        try:
            os.mkdir(self.username)
            os.chdir(self.username)
        except FileExistsError:
            os.chdir(self.username)

    def save_data(self):
        """Saves the data to the uname directory
        :return: none
        :param: none
        """
        with open('data.txt', 'w') as f:
            f.write(json.dumps(self.profile_data))
        self.download_profile_picture()
        print(f"Saved data to directory {os.getcwd()}")

        return True

    def print_data(self):
        """Prints out the data to the screen by iterating through the dict with it's key and value
        :return: True
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
            r = requests.get(self.profile_data['profile_pic_url'])
            f.write(r.content)


def parse_args():
    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument("--username", help="profile username", required=True, nargs=1)
    return parser.parse_args()


def main():
    args = parse_args()
    print(banner)
    if args.username == '':
        print("Please enter the username")
        sys.exit()
    else:
        s = Scraper(args.username[0])


if __name__ == '__main__':
    main()
