more_data = ['entry_data']['ProfilePage'][0]['graphql']

profile_pic_url = d['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']

business_account = d['entry_data']['ProfilePage'][0]['graphql']['user']['is_business_account']

connected_to_fb = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['is_business_account']['connected_fb_page']) #This is nonetype if not connected, needs to be parsed as a string

externalurl = d['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']



bio = d['entry_data']['ProfilePage'][0]['graphql']['user']['biography']

joined_recently = d['entry_data']['ProfilePage'][0]['graphql']['user']['is_joined_recently']

business_category_name = d['entry_data']['ProfilePage'][0]['graphql']['user']['business_category_name']

is_private = d['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']

is_varified = d['entry_data']['ProfilePage'][0]['graphql']['user']['is_verfied']

username = d['entry_data']['ProfilePage'][0]['graphql']['user']['username']








{""}



>>> with open('/Users/stephen/Desktop/new.jpg','wb') as f:
...     r = requests.get(d['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'])
...     f.write(r.content)



