Steps to visualize Spatial Annotation HITs:
1. Run a spatial annotation batch on MTurk
1. Once finished, download the `.csv` batch results and put it in this directory
1. Put all `.mp4` videos (cut to 10-sec length) from AudioSet in `/videos`
1. Run `clipper.py` to generate images of each video. Each video is cut to 1-sec intervals, and an image is taken on the 0.4-second mark of that 1-second interval. This may take a while
1. Run `vis.py` to create `vis-data.html` which will contain all the HIT responses
1. Open `vis-data.html` in web browser
1. Go through and accept/reject the responses you like/dislike. Some images may be horizontally compressed so be sure to look at the YouTube video just to be sure
1. Use the buttons at the top to download the responses you accepted and rejected. Put these files in this directory
1. Run `upload.py` to read the accepted/rejected files and fill in the necessary rows in your `.csv` you downloaded from MTurk
1. Re-upload that file to MTurk

This is a lengthy process because the spatial annotations are difficult to work with. If you have any questions, contact Justin or Marc.
