import random
import json
from rest import callrest

sexys = ["SexyFrex","Upskirt","CelebsPrivate", "Bondage","girlsinyogapants","OnOff", "ass", "collegesluts", "tinytits","milf", "christiangirls","collegensfw","thighhighs","palegirls","latinas" ,"redheads", "Playboy", "rearpussy", "datgap", "DirtySmall","tinytits","pussy", "nsfw_bw", "sweatermeat", "sexyfrex", "bustypetite"]
porns = ["asshole","Bondage","GWCouples","asstastic","penis","OnOff", "ass","PreggoPorn","AmateurArchives","chubby","BubbleButts","collegensfw","thighhighs","rule34","nsfw","latinas","nsfw_gifs","nsfwoutfits","nsfw_gif", "60fpsporn", "WTF", "NSFW_WTF","Fisting", "gonewild","Unashamed","NotSafeForNature", "milf","blowjobs", "shewantstofuck","curvy","TwinGirls","Orgasms","CollegeAmateurs", "DirtySmall","tinytits","pussy"]
boobs = ["boobbounce","hugeboobs", "TheUnderboob", "homegrowntits", "TittyDrop","latinas" ,"curvy", "chubby", "nsfwoutfits"]
foods = ["FoodPorn"]
images = ["Cinemagraphs","MSPaintBattles", "Photobomb", "photoshopfail", "ITookAPicture", "photoshopbattles", "pic", "pics", "EarthPorn", "SpaceGifs"]
lols = ["ProgrammerHumor", "funny", "lolcats", "cats", "pets", "CatGifs", "lolcats", "aww"]
gifs = ["gifs", "CatGifs", "perfectLoops", "SurrealGifs", "SpaceGifs","aww"]
others = ["Futurology", "Nostalgia","ads","france", "CollegeCooking", "EarthPorn", "history", "videos","worldnews", "random", "random", "random"]

subreddits = [sexys, porns, boobs, foods, images, lols, gifs, others]

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

def cmd_random(msg):
    return return_md(get_reddit_random(), False)

def cmd_sexy(msg):
    return return_md(get_reddit(random.choice(sexys)), False)

def cmd_porn(msg):
    return return_md(get_reddit(random.choice(porns)), False)

def cmd_boobs(msg):
    return return_md(get_reddit(random.choice(boobs)), False)

def cmd_image(msg):
	return return_md(get_reddit(random.choice(images)), msg.get("preview", False))

def cmd_gif(msg):
	return return_md(get_reddit(random.choice(gifs)), msg.get("preview", False))

def cmd_cute(msg):
	return return_md(get_reddit(random.choice(lols)), msg.get("preview", False))

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
