@echo off

for %%i in (*.mkv) do vspipe --y4m dbz.vpy --arg key="%%i" - | ffmpeg -v quiet -stats -n -hide_banner -f yuv4mpegpipe -i - -s 708x480 -c:v libx265 -x265-params "limit-sao=1:bframes=16:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 21 -pix_fmt yuv420p10le -preset slow "encode/%%i"

pause
