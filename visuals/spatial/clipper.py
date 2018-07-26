import csv
import os
import subprocess
import shlex

# command to get duration
# ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 fileName
ffprobe = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}"

# command to split file
# i tried doing 1-sec video clips but that was not displaying right so i switched to pictures
# ffmpeg -i fileName -ss startTime -t 1 -async 1 outputName -y
#ffmpeg = "ffmpeg -i {} -ss {} -t 1 -async 1 {} -vcodec libx264 -acodec copy -pix_fmt yuv420p -movflags +faststart -y"
ffmpeg = "ffmpeg -ss {} -i {} -vf \"scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2\" -vframes 1 -q:v 2 {} -y"

output = 'clips/' # clips/abcdefg-start-end.jpg

'''
vids = []
with open("ave.csv", 'r', newline = '') as f:
    reader = csv.reader(f, quotechar = '"', delimiter = '&')
    for row in reader:
        vids.append(row[1] + ".mp4")
'''

run = [x for x in os.listdir("videos") if '.mp4' in x] # change this if you want to run a different directory or list or whatever

for filename in run:
    duration = int(float(subprocess.run(shlex.split(ffprobe.format("test/" + filename)), stdout = subprocess.PIPE).stdout.decode('utf-8')))
    for i in range(duration):
        p = subprocess.run(shlex.split(ffmpeg.format("00:00:0" + str(i) + ".4", "test/" + filename, output + filename.split('.')[0] + "-" + str(i) + "-" + str(i + 1) + ".jpg")), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        if not p.returncode == 0:
            print("error: " + filename + ", " + str(i))
        else:
            print('.', end = '')
