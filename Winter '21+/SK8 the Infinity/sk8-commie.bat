@echo off

"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "comraw_[AniDL] SK8 the Infinity - 10 [WEB 480p 10bit][SubsPlease].mkv" --no-subtitles --no-track-tags --no-global-tags --no-chapters --language 0:jpn --default-track 0:yes --language 1:jpn --track-name 1:Japanese --default-track 1:yes "[AniDL] SK8 the Infinity - 10 [WEB 480p 10bit][SubsPlease].mkv" --split timestamps:12s --title ^"[AniDL] SK8 the Infinity [WEB 480p 10bit][Soap]^" --track-order 0:0,0:1

del "*001.mkv"

ren "*002.mkv" "temp.mkv"

ffmpeg -hide_banner -v quiet -stats -i "temp.mkv" -i "../subsSk810.mkv" -map 0 -map -0:t -map 1 -c copy "[AniDL] SK8 the Infinity - 10 [WEB 480p 10bit][Commie].mkv"

del "temp.mkv"
