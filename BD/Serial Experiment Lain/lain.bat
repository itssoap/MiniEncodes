@echo off

for %%i in (*.mkv) do vspipe --y4m lain.vpy --arg key="%%i" - | ffmpeg -v quiet -stats -hide_banner -f yuv4mpegpipe -i - -s 676x480 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "480p/%%i"
for %%i in (*.mkv) do vspipe --y4m lain.vpy --arg key="%%i" - | ffmpeg -v quiet -stats -hide_banner -f yuv4mpegpipe -i - -s 1014x720 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "720p/%%i"
for %%i in (*.mkv) do vspipe --y4m lain.vpy --arg key="%%i" - | ffmpeg -v quiet -stats -hide_banner -f yuv4mpegpipe -i - -s 1520x1080 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "1080p/%%i"

pause
