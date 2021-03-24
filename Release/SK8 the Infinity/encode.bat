@echo off

for /r %%i in (release/*.mkv) do vspipe --y4m sk8release.vpy --arg key="release/%%~nxi" - | ffmpeg -hide_banner -v quiet -stats -y -f yuv4mpegpipe -i - -s 1920x1080 -c:v libx265 -x265-params "no-sao=1:no-strong-intra-smoothing=1:bframes=8:psy-rd=2:psy-rdoq=5:aq-mode=3:deblock=-1,-1:ref=6" -crf 18 -pix_fmt yuv420p10le -preset slow -map 0 "encode/%%~nxi"

pause
