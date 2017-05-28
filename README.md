# HubTube
Networking final project.

## Networking specifications
We are using plain HTTP for this project since it's answers all of our needs.

"Listeners" are the clients who send song requests.

The Server's GUI is HTML Youtube Player which sits on the hosting machine, and plays
    the songs.

So, once the server is listening he is ready ready to receive song requests.

The JS Server Script sends requests to the server every interval (for example, 5 secs),
    and checks for when the first song is sent.

Meanwhile, the listeners send the server some POST requests with the songs they
    want, through their client HTML GUI.

Every song POST will contain:
 - video-url : the URL of th Youtube video
 - name : name of sender
encoded as JSON.

Then, the server inserts the requests to a list he remembers. Let's call
    it playlist

The JS Server script will send a GET request once a song is over,
    asking for the next one. The response will contain the following fields
    in json format:
 - video-id : The id of the video
 - name : name of sender

* Note: if there are no more songs, the JS Server script retries to request every
    interval seconds (for example 5 secs).
* Another note: all data passed will be encoded in JSON.
