@echo off

"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "yamraw.mkv" --no-subtitles --no-track-tags --no-global-tags "[AniDL] Vivy - Fluorite Eye's Song -  04  [WEB 1080p 10bit][SubsPlease].mkv" --split timestamps:12s --track-order 0:0

del "*001.mkv"

ren "*002.mkv" "temp.mkv"

ffmpeg -hide_banner -v quiet -stats -i "temp.mkv" -i "../subsVivy04.mkv" -map 0 -map -0:a -map -0:t -map 1 -c copy "[AniDL] Vivy - Fluorite Eye's Song - 04 [WEB 1080p 10bit][YameteTomete].mkv"

del "temp.mkv"
