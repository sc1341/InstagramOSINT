#! /usr/bin/env python3
#Instagram Scraper
from bs4 import BeautifulSoup
import requests, random, sys, json, time, os, argparse


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


    def __init__(self):
        self.user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
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


    def convert_to_int(self, num: str):
        '''Converts values like 11.9k to 11900 because instagram shortens
        their follower count, this currently does not work and idk how to fix it'''
        if "k" in num:
        #Find the first few digits that should be * 1000
            try:
                front = int(num[:num.index('.')])
                back = int(num[num.index('.')+1])
            except ValueError:
                return (front *1000)

            return (front * 1000) + (back * 100)

        elif "m" in num:
            try:
                front = int(num[:num.index('.')])
                back = int(num[num.index('.')+1])
            except ValueError:
                return (front * 1000000)

            return (front * 1000000) + (back*100000)

        else:
            return int(num.replace(',', ''))


    def scrape(self,username:str):
        '''Takes a username as a string to find information about that person's instagram profile, a random
        user agent is picked to spoof when the data is collected'''
        time.sleep(2)
        #Get the html data with the requests module
        r = requests.get(f'http://instagram.com/{username}', headers={'User-Agent': random.choice(self.user_agents)})
        soup = BeautifulSoup(r.text,'html.parser')
        #Find the tags that hold the data we want to parse
        general_data = soup.find_all('meta',attrs={'property':'og:description'})
        more_data = soup.find_all('script',attrs={'type':'text/javascript'})
        description = soup.find('script', attrs={'type': 'application/ld+json'})
        #Try to parse the nessicary content but if it fails, then user != exist
        try:
            text = general_data[0].get('content').split()
            #Get the json data held inside of the <script> type="applicaiton/il/json"
            description = json.loads(description.get_text())
            profile_meta = json.loads(more_data[3].get_text()[21:].strip(';'))

        except:
            print(colors.FAIL + f"Username {username} not found" + colors.ENDC)
            sys.exit()

        #If the user does not have anything in their bio, the value will not be in the json dump
        #So we just set the bio to an empty string
        try:
            self.profile_data = {"Username": text[-1], "Profile name": description['name'], "URL": description['mainEntityofPage']['@id'],
             "Followers": text[0], "Following": text[2], "Posts": text[4], "Bio": description['description'],
             "profile_pic_url": profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'],
             "is_business_account": profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_business_account'],
             "connected_to_fb": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['connected_fb_page']),
             "externalurl": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
             "joined_recently": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_joined_recently']),
             "business_category_name": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['business_category_name']),
             "is_private": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
             "is_verified": str(profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}
        except KeyError:
            profile_data = {"Username": text[-1], "Profile name": description['name'],
             "Followers": text[0], "Following": text[2], "Posts": text[4], "Bio": '', "URL":description['mainEntityofPage']['@id'], "ProfilePictureURL":description['image']}

        self.print_data()
        self.make_directory()
        self.download_profile_picture()
        self.save_data()

    def make_directory(self):
        """Makes the profile directory of the profile being searched
        :return: True
        """
        try:
            os.mkdir(self.profile_data['Username'])
        except FileExistsError:
            print("Error, directory exists!")
            sys.exit()


    def save_data(self):
        """Saves the data to the uname directory
        :return: none
        :param: none
        """
        os.chdir(self.profile_data['Username'])
        with open('data.txt','w') as f:
            f.write(json.dumps(self.profile_data))
        print(f"Saved data to directory {os.getcwd()}")

        return True

    def print_data(self):
        """Prints out the data to the screen
        :return: True
        """
        #Print the data out to the user
        print(colors.HEADER + "---------------------------------------------" + colors.ENDC)
        print(colors.OKGREEN + f"Results: scan for {self.profile_data['Username']} on instagram" + colors.ENDC)
        print(f"""Username:{self.profile_data["Username"]}""")
        print(f"URL:{self.profile_data['URL']}")
        print(f"Profile name: {self.profile_data['Profile name']}")
        print(f"Followers:{self.profile_data['Followers']}")
        print(f"Following:{self.profile_data['Following']}")
        print(f"Posts:{self.profile_data['Posts']}")
        #If the user does not have anything in their bio, the value will not be in the json dump
        #So we just set the bio to an empty string
        try:
            print(f"Profile Bio:{self.profile_data['Bio']}")
        except KeyError:
            self.profile_data['Bio'] = ''
            print("Profile Bio: ''")
        print("")


    def download_profile_picture(self):
        """Downloads the profile pic and saves it to the directory
        :return: none
        :param: none
        """
        os.chdir(self.profile_data['Username'])
        with open("profile_pic.jpg","wb") as f:
            r = requests.get(self.profile_data['profile_pic_url'])
            f.write(r.content)



def parse_args():
    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument("--username", help="profile username", required=True, nargs=1)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.username == '':
        print("Please enter the username")
        sys.exit()
    else:
        s = Scraper()
        s.scrape(args.username[0])


if __name__ == '__main__':
   main()



