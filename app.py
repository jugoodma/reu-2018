from flask import Flask

import csv

app = Flask(__name__)
data_file = 'unbalanced_train_segments.csv' # the file name from Google's AudioSet dataset
# variables for cutting up the videos
window = 1.0 # length, in seconds, of each clip we show to the MTurk worker
interval = 0.5 # interval, in seconds, of each window hop
# start and end times are dictated by each individual video
# end - start = 10sec
length = 10.0 # end - start for every video

# NOTES
#
# here's what the .csv file looks like:
# youtubeID,start_second,end_second,labels
#
# from what I've noticed, the youtubeID starts with either =-- or =- or -
#
# we display the labels to the worker so they know what to listen for in the video
#
# We need to generate an embedded iframe in the MTurk UI:
# <iframe src="https://www.youtube.com/embed/[youtubeID]?start=[start]&end=[end]" width="xxx" height="yyy"></iframe>
#
# here's how I see the MTurk flow:
# - worker opens our MTurk UI
# - javascript runs onLoad and GET requests this API for a youtube url from dataset
# - worker reads instructions and watches the video
# - - video should be 1sec, polled randomly from the given 10sec time interval
# - worker clicks radio button yes or no of whether or not the audio fit the labels
# - answer,youtubeID,start,end are POST requested back to this API
# - worker claims reward
#

@app.route('/video/<string:key>', methods=['GET'])
def show_video(key):
    # decrypt and verify the key
    
    # get a random video ID that's not already given
    
    return '6SlgtELqOWc'
