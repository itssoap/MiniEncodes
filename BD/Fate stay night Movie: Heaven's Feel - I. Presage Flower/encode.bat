@echo off
del *.png
ffmpeg -v quiet -stats -hide_banner -n -i "presageFiltered.mkv" -s 1920x1080 -c libx265 -x265-params "fps=24000/1001:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3:ref=6" -crf 21 -pix_fmt yuv420p10le -preset slow Presage1080p.mkv
ffmpeg -v quiet -stats -hide_banner -y -i "presageFiltered.mkv" -s 1280x720 -c libx265 -x265-params "fps=24000/1001:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3:ref=6" -crf 22 -pix_fmt yuv420p10le -preset slow Presage720p.mkv
ffmpeg -v quiet -stats -hide_banner -y -i "presageFiltered.mkv" -s 854x480 -c libx265 -x265-params "fps=24000/1001:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3:ref=6" -crf 22.5 -pix_fmt yuv420p10le -preset slow Presage480p.mkv
pause
