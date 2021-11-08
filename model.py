import base62 as b62
import redis, json, time, random, os

ID_SEED = 1000000
NO_SUCH_URL_MSG = "No Such Short URL Exists"

client = redis.Redis(host='redis', port=6379, db=1)

def createEntry(urlData, urlTimestamp=None):
    id = random.randrange(100, ID_SEED)

    while client.hexists('shortURL_map', id):
        id = random.randrange(100, ID_SEED)
        print ("set new id is " + str(id))
    
    if urlTimestamp is not None:
        urlTimestamp =  urlTimestamp + int(time.time())

    print("Before setting into map " + str(id))
    client.hset('shortURL_map', int(id), json.dumps({'urlData' : urlData, 'timestamp' : urlTimestamp, 'visits': 0}))

    return b62.idToShortURL(int(id))


def findEntry(shortURL):
    print ("shortURRL " + shortURL + "ZZ")

    id = b62.shortURLToId(shortURL)

    print ("ID for shortURL " + str(id))

    shortURLMap = client.hget('shortURL_map', id)

    if shortURLMap is None:
        return NO_SUCH_URL_MSG

    shortURLMap = json.loads(shortURLMap)
    future_epoch = shortURLMap['timestamp']
    
    print ("future epoch is " + str(future_epoch))

    if future_epoch is not None and int(time.time()) - future_epoch > 0:
        return NO_SUCH_URL_MSG

    print("json data " + shortURLMap['urlData'])

    #increase visit count
    shortURLMap['visits'] =  shortURLMap['visits'] + 1
    
    client.hset('shortURL_map', int(id), json.dumps(shortURLMap))

    return shortURLMap['urlData']

def deleteEntryFromMap(shortUrl):
    id = b62.shortURLToId(shortUrl)
    if client.hexists('shortURL_map', id):
        client.hdel('shortURL_map', id)
        return "Successfully Deleted"
    return NO_SUCH_URL_MSG

def analyzeEntryFromMap(shortUrl):
    id = b62.shortURLToId(shortUrl)
    if client.hexists('shortURL_map', id):
        entry = json.loads(client.hget('shortURL_map', id))
        return "Visits for " + shortUrl + ": " + str(entry['visits'])
    return NO_SUCH_URL_MSG
