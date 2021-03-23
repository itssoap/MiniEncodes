for %%i in (*.mkv) do ffmpeg -v quiet -stats -hide_banner -i "%%i" -c copy -map 0 -map -0:a:1 -map -0:s:1 "3%%i"
pause