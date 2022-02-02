@echo off
timeout 18000
for %%i in (*.mkv) do (echo "%%~ni"
vspipe -c y4m jojo.py --arg key="%%i" - | ffmpeg -hide_banner -v quiet -stats -y -f yuv4mpegpipe -i - -c:v ffv1 -level 3 -threads 8 -pix_fmt yuv420p10le jojo.mkv
ffmpeg -hide_banner -v quiet -stats -i jojo.mkv -s 1280x720 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -crf 22 -pix_fmt yuv420p10le -preset slow -map 0 -movflags faststart "encode720/%%~ni720.mkv"
ffmpeg -hide_banner -v quiet -stats -i jojo.mkv -s 1920x1080 -c:v libx265 -x265-params "limit-sao=1:bframes=8:psy-rd=1.5:psy-rdoq=2:aq-mode=3" -crf 22 -pix_fmt yuv420p10le -preset slow -map 0 -movflags faststart "encode1080/%%~ni1080.mkv"

ffmpeg -hide_banner -v quiet -stats -y -i "encode720/%%~ni720.mkv" -i "%%i" -map 0 -map 1 -map -1:v -c:v copy -c:a copy -map_metadata:g -1 -metadata:s:v title="" -metadata:s:a title="Japanese" "encode720/%%~ni7201.mkv"
ffmpeg -hide_banner -v quiet -stats -y -i "encode1080/%%~ni1080.mkv" -i "%%i" -map 0 -map 1 -map -1:v -c:v copy -c:a copy -map_metadata:g -1 -metadata:s:v title="" -metadata:s:a title="Japanese" "encode1080/%%~ni10801.mkv"

"C:/Program Files/MKVToolNix\mkvmerge.exe" -o "encode720/%%i" "encode720/%%~ni7201.mkv"
"C:/Program Files/MKVToolNix\mkvmerge.exe" -o "encode1080/%%i" "encode1080/%%~ni10801.mkv")
pause