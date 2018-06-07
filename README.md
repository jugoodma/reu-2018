# REU 2018
by Justin Goodman & Marc Moore

Data expander

Dataset is from [Google's AudioSet](https://research.google.com/audioset///download.html)

Steps:
1. Run ./setup.sh to install Flask and download the dataset
1. Install our script on Amazon Mechanical Turk
1. Do stuff...

Initial setup (make sure you have python 3):
```bash
pip install Flask
wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv
```

Make sure you have an AWS account linked to your MTurk Requester account. Then setup awscli:
```bash
pip install awscli
aws configure
```

To get started in dev mode, run:
```bash
FLASK_APP=app.py FLASK_ENV=development flask run
```

To setup a production server (Apache/Ubuntu) [follow these instructions](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/)

To run in production (Apache/Ubuntu) (maybe, unsure about this):
```bash
FLASK_APP=app.py FLASK_ENV=production flask run --host=0.0.0.0
```
