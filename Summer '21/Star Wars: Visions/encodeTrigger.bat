@echo off
vspipe -y "%~1" - | ffmpeg -v quiet -stats -f yuv4mpegpipe -y -i - -c:v ffv1 -level 3 -threads 8 -pix_fmt yuv420p10le "D:/episode.mkv"
ffmpeg -v quiet -stats -i "D:/episode.mkv" -s 1920x816 -c:v libx265 -x265-params "no-sao=1:bframes=16:psy-rd=1.0:qcomp=0.8:psy-rdoq=2:aq-mode=3:ref=6:deblock=-1,-1" -crf 20 -pix_fmt yuv420p10le -preset slower "1080p/%~nx1.mkv"
ffmpeg -v quiet -stats -i "D:/episode.mkv" -s 1280x544 -c:v libx265 -x265-params "no-sao=1:bframes=16:psy-rd=1.0:qcomp=0.8:psy-rdoq=2:aq-mode=3:ref=6:deblock=-1,-1" -crf 21 -pix_fmt yuv420p10le -preset slower "720p/%~nx1.mkv"
del "D:/episode.mkv"
pause