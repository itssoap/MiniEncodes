for %%i in (*.mkv) do ffmpeg -i "%%i" -i "../%%i" -hide_banner -v quiet -stats -n -map 0 -map 1 -map -1:v -c:v copy -c:a aac -ab 128k "1%%i"

pause