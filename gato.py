import requests
import tweepy
import shutil

twitterTokens = {
                'consumerKey':'',
                'consumerSecret':'',
                'accessToken':'',
                'accessTokenSecret':''
}

theCatApiToken = ''

searchKeywords = ['gato','gata','gatos','gatas']

def getImgUrl(APIKey):
    r = requests.get('https://api.thecatapi.com/v1/images/search?limit=1',headers={'x-api-key':APIKey})

    json = r.json()

    if isinstance(json,list):
        return json[0]['url']
    else:
        return None

def downoadImg(url,fileName):
    r = requests.get(url,stream=True)

    file = open('tmp/'+fileName,'wb')

    shutil.copyfileobj(r.raw,file)

    file.close()
    del r

def startTwitterApi(consumerKey,consumerSecret,accessToken,accessTokenSecret):
    auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
    auth.set_access_token(accessToken,accessTokenSecret)

    api = tweepy.API(auth)

    return api

def getTweets(api,keywords,since):
    tweetsList = []

    query = keywords[0]
    for keyword in keywords[1:]:
        query = query+' OR '+keyword

    tweets = api.search(query,since_id=since,count=100)

    for tweet in tweets:
        if any([keyword in tweet.text for keyword in keywords]):
            tweetsList.append({'username':tweet.user.screen_name,'tweetId':tweet.id_str})

    return tweetsList


api = startTwitterApi(twitterTokens['consumerKey'],twitterTokens['consumerSecret'],twitterTokens['accessToken'],twitterTokens['accessTokenSecret'])

tweets = getTweets(api,keywords,1280971097400315906)

for tweet in tweets:
    imgUrl = getImgUrl(theCatApiToken)
    downoadImg(imgUrl,tweet['tweetId']+'.'+imgUrl.split('.')[-1])

    status = "@"+tweet['username']+' Olá! Aqui está uma imagem de um gato para vc'
    api.update_with_media('tmp/'+tweet['tweetId']+'.'+imgUrl.split('.')[-1],status,in_reply_to_status_id=tweet['tweetId'])
