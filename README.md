# REU 2018
by Justin Goodman & Marc Moore

Data expander

Dataset is from [Google's AudioSet](https://research.google.com/audioset///download.html)

Steps:
1. Create Amazon Mechanical Turk Requester Account
1. Create new project with settings outlined in settings.txt
1. In design layout click 'source', then paste in the text from ui.html
1. Preview, then Finish
1. Click Publish Batch
1. Change settings and run database.py
1. Upload the generated .csv
1. Publish HIT batch
1. ???
1. Profit!

Download required files using:
```bash
wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv
wget -nc http://vrttest2017.oss-us-east-1.aliyuncs.com/data/videodatainfo_2017.json
```

```bash
pip install boto3
```
