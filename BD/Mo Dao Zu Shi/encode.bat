@echo off

for %%i in (*.mkv) do vspipe --y4m modaozushi.vpy --arg key="%%i" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 854x358 -c:v libx265 -x265-params "log-level=error:limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "480p/%%i"
for %%i in (*.mkv) do vspipe --y4m modaozushi.vpy --arg key="%%i" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 1280x538 -c:v libx265 -x265-params "log-level=error:limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "720p/%%i"
for %%i in (*.mkv) do vspipe --y4m modaozushi.vpy --arg key="%%i" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 1920x806 -c:v libx265 -x265-params "log-level=error:limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22 -pix_fmt yuv420p10le -preset slow "1080p/%%i"

pause
