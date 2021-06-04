@echo off
timeout 16200

for %%i in (*.mkv) do (ffmpeg -hide_banner -v quiet -stats -i "%%i" -c:v libx265 -x265-params "no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3:ref=6" -c:a copy -map 0 -crf 25 -maxrate 700k -bufsize 1000k -preset slow -pix_fmt yuv420p10le "a%%i"
"C:/Program Files/MKVToolNix\mkvmerge.exe" -o "%%i" "a%%i"
del "a%%i")
pause
