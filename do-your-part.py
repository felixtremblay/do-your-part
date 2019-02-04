import rumps
import requests
import configparser
import os

#get the configurations
config = configparser.ConfigParser()
if os.path.isfile('debug_config.ini'):
    config.read('debug_config.ini')
else:
    config.read("config.ini")

api_key = config['DEFAULT']['api_key']
channel_1_id = config['DEFAULT']['channel_1_id'] 
channel_2_id = config['DEFAULT']['channel_2_id']
update_frequency = int(config['DEFAULT']['update_frequency'])

api_url = 'https://content.googleapis.com/youtube/v3/channels'
data = {
        "id" : '',
        "key" : api_key,
        "part" : 'statistics'
        }

def getSubGap():
    data["id"] = channel_1_id
    r = requests.get(api_url, params=data)
    channel_1_sub_count = int(r.json()["items"][0]["statistics"]["subscriberCount"])

    data["id"] = channel_2_id
    r = requests.get(api_url, params=data)
    channel_2_sub_count = int(r.json()["items"][0]["statistics"]["subscriberCount"])

    sub_gap =  "{:,}".format(channel_1_sub_count-channel_2_sub_count)
    return sub_gap

@rumps.timer(update_frequency)
def updateTimer(_):
    app.title = "Sub gap : " + getSubGap()

app = rumps.App("dyp default title", quit_button=rumps.MenuItem("Quit"))
app.run()
