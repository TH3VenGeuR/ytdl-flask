from flask import Flask, render_template, request
from utils.get_video_list import get_video_list
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.register_error_handler(404, lambda e: render_template('error.html', title="Page not found", error=404, message="The page you requested was not found."))
'''
app.register_error_handler(404, lambda e: render_template('error.html', error=e, title='404', message='Page not found'))
app.register_error_handler(500, lambda e: render_template('error.html', error=e, title='500', message='Internal server error'))
app.register_error_handler(Exception, lambda e: render_template('error.html', error=e, title='500', message='Internal server error'))
'''


@app.route('/')
def form():
    return render_template('index.html', title="YouTube Downloader - Search page", action="/data")


@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return render_template('index.html', title="YouTube Downloader - Search page", action="/data")
    if request.method == 'POST':
        # print(request.form['url'])
        url = request.form['url']
        list_video = get_video_list(url)
        try:
            if len(list_video[0][0][0][0]) > 1:
                print("playlist")
                return render_template('playlist.html', title="YouTube Downloader - Download page", playlist=list_video)
            else:
                print("video")
                return render_template('video.html',
                                       title="Download Videos",
                                       video_data=list_video[0],
                                       video_thumbnail=list_video[1],
                                       video_title=list_video[2])
        except IndexError:
            return render_template('error.html', title="YouTube Downloader - Error", error="No video found")


@app.route("/contacts/")
def about():
    return render_template('contacts.html', title="YouTube Downloader - About author")


http_server = WSGIServer(("", 5000), app)
http_server.serve_forever()
# app.run(host='localhost', port=5000, debug=True)
