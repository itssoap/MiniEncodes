@echo off

vspipe --y4m springsong.vpy --arg key="%~nx1" - | ffmpeg -hide_banner -v quiet -stats -n -f yuv4mpegpipe -i - -s 1920x1080 -c:v libx265 -x265-params "log-level=error:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3" -crf 21.5 -pix_fmt yuv420p10le -preset slow -map 0 -movflags faststart "1%~nx1"
vspipe --y4m springsong.vpy --arg key="%~nx1" - | ffmpeg -hide_banner -v quiet -stats -n -f yuv4mpegpipe -i - -s 1280x720 -c:v libx265 -x265-params "log-level=error:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3" -crf 21.5 -pix_fmt yuv420p10le -preset slow -map 0 -movflags faststart "2%~nx1"
vspipe --y4m springsong.vpy --arg key="%~nx1" - | ffmpeg -hide_banner -v quiet -stats -n -f yuv4mpegpipe -i - -s 854x480 -c:v libx265 -x265-params "log-level=error:no-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=4:aq-mode=3" -crf 21.5 -pix_fmt yuv420p10le -preset slow -map 0 -movflags faststart "3%~nx1"

ffmpeg -hide_banner -v quiet -stats -y -i "1%~nx1" -i "%~nx1" -map 0 -map 1 -map -1:v -map -1:a:0 -c:v copy -c:a aac -ac 2 -ab 192k -map_metadata:g -1 -metadata title="[AniDL] Fate Stay Night - Heaven's Feel - III. Spring Song [BD 1080p 10bit][Soap]" -metadata:s:v title="" -metadata:s:a title="Japanese" "11%~nx1"
ffmpeg -hide_banner -v quiet -stats -y -i "2%~nx1" -i "%~nx1" -map 0 -map 1 -map -1:v -map -1:a:0 -c:v copy -c:a aac -ac 2 -ab 192k -map_metadata:g -1 -metadata title="[AniDL] Fate Stay Night - Heaven's Feel - III. Spring Song [BD 720p 10bit][Soap]" -metadata:s:v title="" -metadata:s:a title="Japanese" "12%~nx1"
ffmpeg -hide_banner -v quiet -stats -y -i "3%~nx1" -i "%~nx1" -map 0 -map 1 -map -1:v -map -1:a:0 -c:v copy -c:a aac -ac 2 -ab 192k -map_metadata:g -1 -metadata title="[AniDL] Fate Stay Night - Heaven's Feel - III. Spring Song [BD 480p 10bit][Soap]" -metadata:s:v title="" -metadata:s:a title="Japanese" "13%~nx1"

"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "1080p/%~nx1" --language 1:jpn --track-name 1:Japanese --default-track 1:yes --sub-charset 2:UTF-8 --language 2:eng --track-name ^"2:English subs^" --default-track 2:yes --language 0:und --default-track 0:yes "11%~nx1" --track-order 0:0,0:1,0:2
"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "720p/%~nx1" --language 1:jpn --track-name 1:Japanese --default-track 1:yes --sub-charset 2:UTF-8 --language 2:eng --track-name ^"2:English subs^" --default-track 2:yes --language 0:und --default-track 0:yes "12%~nx1" --track-order 0:0,0:1,0:2
"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "480p/%~nx1" --language 1:jpn --track-name 1:Japanese --default-track 1:yes --sub-charset 2:UTF-8 --language 2:eng --track-name ^"2:English subs^" --default-track 2:yes --language 0:und --default-track 0:yes "13%~nx1" --track-order 0:0,0:1,0:2

pause
