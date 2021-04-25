@echo off

vspipe --y4m children.vpy --arg key="[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 854x480 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22.5 -pix_fmt yuv420p10le -preset slow "480p/[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv"
vspipe --y4m children.vpy --arg key="[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 1280x720 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22.5 -pix_fmt yuv420p10le -preset slow "720p/[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv"
vspipe --y4m children.vpy --arg key="[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv" - | ffmpeg -v quiet -n -stats -hide_banner -f yuv4mpegpipe -i - -s 1920x1080 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -map 0 -crf 22.5 -pix_fmt yuv420p10le -preset slow "1080p/[WBDP] Children Who Chase Lost Voices from Deep Below [BD][1080p-FLAC-FLAC] [60F869CD].mkv"

pause
