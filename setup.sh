#!/usr/bin/env bash

pip install Flask
export FLASK_APP=app.py
export FLASK_ENV=development

wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
