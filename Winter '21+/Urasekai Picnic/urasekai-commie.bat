@echo off

ffmpeg -i "[AniDL] Ura Sekai Picnic - 10 [WEB 480p 10bit][SubsPlease].mkv" -hide_banner -v quiet -stats -c copy -map 0 -map -0:s -map -0:t "comraw_[AniDL] Ura Sekai Picnic - 10 [WEB 480p 10bit][SubsPlease].mkv"

"C:/Program Files/MKVToolNix\mkvmerge.exe" --output "comraw_[AniDL] Ura Sekai Picnic - 10 [WEB 480p 10bit][SubsPlease].mkv" --no-subtitles --no-track-tags --no-global-tags --no-chapters --language 0:jpn --default-track 0:yes --language 1:jpn --track-name 1:Japanese --default-track 1:yes "[AniDL] Ura Sekai Picnic - 10 [WEB 480p 10bit][SubsPlease].mkv" --split timestamps:7s --title ^"[AniDL] Ura Sekai Picnic [WEB 480p 10bit][Soap]^" --track-order 0:0,0:1

del "*001.mkv"

ren "*002.mkv" "temp.mkv"

ffmpeg -hide_banner -v quiet -stats -i "temp.mkv" -i "../subsUra10.mkv" -map 0 -map -0:t -map 1 -c copy "[AniDL] Ura Sekai Picnic - 10 [WEB 480p 10bit][Commie].mkv"

del "temp.mkv"

del "comraw*.mkv"
