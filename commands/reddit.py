# -*- coding: utf-8 -*-

import random
import json
from rest import callrest
from .decorators import register_as_command

from bs4 import BeautifulSoup
from expiringdict import ExpiringDict
cache = ExpiringDict(max_len=1, max_age_seconds=3600)

nsfw = ["SexyFrex","Upskirt","CelebsPrivate", "boobbounce","hugeboobs", "TheUnderboob", "homegrowntits", "TittyDrop","latinas" ,"curvy", "chubby", "nsfwoutfits", "Bondage","girlsinyogapants","OnOff", "ass", "collegesluts", "tinytits","milf", "christiangirls","collegensfw","thighhighs","palegirls","latinas" ,"redheads", "Playboy", "rearpussy", "datgap", "DirtySmall","tinytits","pussy", "nsfw_bw", "sweatermeat", "sexyfrex", "bustypetite", "asshole","Bondage","GWCouples","asstastic","penis","OnOff", "ass","PreggoPorn","AmateurArchives","chubby","BubbleButts","collegensfw","thighhighs","rule34","nsfw","latinas","nsfw_gifs","nsfwoutfits","nsfw_gif", "60fpsporn", "WTF", "NSFW_WTF","Fisting", "gonewild","Unashamed","NotSafeForNature", "milf","blowjobs", "shewantstofuck","curvy","TwinGirls","Orgasms","CollegeAmateurs", "DirtySmall","tinytits","pussy"]
foods = ["FoodPorn"]
images = ["Cinemagraphs","bridgeporn","spaceporn","AuroraPorn","SkyPorn","ExposurePorn", "Photobomb", "photoshopfail", "ITookAPicture", "photoshopbattles", "pic", "pics", "EarthPorn"]
lols = ["funny", "lolcats", "cats", "pets", "CatGifs", "lolcats", "aww"]
gifs = ["gifs", "CatGifs", "perfectLoops", "SurrealGifs", "SpaceGifs","aww"]
others = ["Futurology", "Nostalgia","ads","france", "CollegeCooking", "EarthPorn", "history", "videos","worldnews", "random", "random", "random"]

subreddits = [nsfw, foods, images, lols, gifs, others]

def get_reddit_random():
        # On melange les categorie principale.
        random.shuffle(subreddits)
        # Recuperation d'un subbreddit dans les categories.
        return get_reddit(random.choice(random.choice(subreddits)))

def get_reddit(subreddit):
    try:
        data = callrest(domain="www.reddit.com", port=443, ssl=True, path="/r/{0}/new/.json".format(subreddit), params={})[2]
        return random.choice(json.loads(data).get("data").get("children")).get("data")
    except Exception as e:
        print (e)
        return ("Oups", "Rien... "+subreddit)

def return_md(message, preview=False):
    url = message.get("url")
    if preview and ("jpeg" in url or "jpg" in url or "png" in url or "gif" in url) and "gifv" not in url:
        return "{0} : ![image]({1})".format(message.get("title"), url)
    else:
        return "{0} : {1}".format(message.get("title"), url)

def get_redditlist():
    if "redditlist" not in cache:
        cache["redditlist"] = callrest(domain="redditlist.com", type="GET", path="/nsfw", params={})[2]

    soup = BeautifulSoup(cache["redditlist"], "html.parser")
    links = soup.find_all("div", class_="listing-item")
    subReddit = random.choice(links).get("data-target-subreddit", "android")

    return get_reddit(subReddit)


@register_as_command("random")
def cmd_random(msg):
    # return return_md(get_reddit_random(), False)
    return return_md(get_redditlist(), False)

@register_as_command("nsfw")
def cmd_nsfw(msg):
    return return_md(get_reddit(random.choice(nsfw)), False)

@register_as_command("image")
def cmd_image(msg):
	return return_md(get_reddit(random.choice(images)), msg.get("preview", False))

@register_as_command("gif")
def cmd_gif(msg):
	return return_md(get_reddit(random.choice(gifs)), msg.get("preview", False))

@register_as_command("cute")
def cmd_cute(msg):
	return return_md(get_reddit(random.choice(lols)), msg.get("preview", False))

@register_as_command("top10")
def cmd_top10(msg):
    return_values = []
    try:
        data = callrest(domain="www.reddit.com", port=443, ssl=True, path="/top/.json", params={"limit":10, "sort":"top", "t":"hour"})[2]
        data = json.loads(data).get("data").get("children")

        for element in data:
            try:
                return_values.append("{title} : {url}".format(**element["data"]))
            except:
                pass

        return "Top10 : \r\n- {0}".format("\r\n- ".join(return_values))
    except Exception as e:
        raise Exception(e)
