from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)

@app.route("/")
@app.route("/create")
def create_page():
    return render_template("createurl.html")

@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")

@app.route("/delete")
def delete_page():
    return render_template("delete.html")

@app.route("/handleAnalyticsEndpoint")
def handle_analytics_endpoint():
    url = request.args.get('url')
    
    #sanitize the shortUrl
    shortUrl = url.split('/')[-1]

    message = model.analyzeEntryFromMap(shortUrl)
    return render_template("analytics.html", message=message)

@app.route("/deleteEndpoint")
def delete_analytics_endpoint():
    url = request.args.get('url')

    #sanitize the shortUrl
    shortUrl = url.split('/')[-1]

    message = model.deleteEntryFromMap(shortUrl)
    return render_template("delete.html", message=message)

@app.route("/handleCreateRequest", methods = ['POST'])
def handle_create_request():
    urlData = request.form['url']
    urlTimestamp = request.form['timestamp']
    
    #Adds an http:// to the string by default if not passed in
    urlData = sanitizeUrlData(urlData)

    if isInvalidUrlTimestamp(urlTimestamp):
        message = "Invalid URL Timestamp. It should be greater than 0 seconds"
        return render_template("createerror.html", message=message)
    else:
        urlTimestamp = int(urlTimestamp)
        shortenedID = model.createEntry(urlData, urlTimestamp)
        descriptiveUrl = "localhost:5000/url.short/" + shortenedID
        url = "http://" + descriptiveUrl
    return render_template("createurl.html", url=url, descriptiveUrl=descriptiveUrl)
    
@app.route('/<path:path>')
def findURL(path):
    path = path.split('/')

    print ("path = " + path[len(path)-1])

    message = model.findEntry(path[len(path)-1])

    if message == "No Such Short URL Exists":
        return render_template("redirecterror.html", message=message)
    else:
        return redirect(message, code="302")
 
def isInvalidUrlTimestamp(urlTimestamp) -> bool:
    urlTimestamp is not None and not urlTimestamp.isdigit() and int(urlTimestamp) < 0

def sanitizeUrlData(urlData) -> str:  
    if not "http://" in urlData and not "https://" in urlData:
        urlData = "http://" + urlData
    return urlData

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,debug=True)
