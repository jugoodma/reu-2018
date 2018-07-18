# REU 2018
by Justin Goodman & Marc Moore

Data expander

Datasets are from
* [Google's AudioSet](https://research.google.com/audioset/download.html)
* [Microsoft's MSR-VTT](http://ms-multimedia-challenge.com/2017/dataset)

Paste the `.html` files in `/templates` into the Amazon Mechanical Turk Requester frontend interface
Use the `.xml` files in `/templates` for backend HIT creation

Download required files using:
```bash
wget -nc http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
wget -nc https://raw.githubusercontent.com/audioset/ontology/master/ontology.json
wget -nc http://vrttest2017.oss-us-east-1.aliyuncs.com/data/videodatainfo_2017.json
```

For backend HIT creation and general script usage
```bash
pip install csv json boto3
```

Our <Audio-Video Separate Streams> dataset is formatted in JSON as follows (similar to MSR-VTT):
```json
{
	"info": {
		"year": str,
	        "version": str,
	        "description": str,
		"contributor": str,
		"data_created": str
	},
	"data": {
		"id": int,
		"video_id": str,
	        "origin": int,
		"ytid": str,
		"start time": float,
		"end time": float,
		"split": str
	        "audio": {
			"sen_id": str, # int + 'a'
			"video_id": str,
			"caption": str
		},
		"video": {
			"sen_id": str, # int + 'v'
			"video_id": str,
			"caption": str
		}
    	}
}
```