## DBZ S2 Audios


| Have I kept it?   |Audio Name                              |
|----|------------------------------|
|No  |1st is mono                   |
|Yes |Keep this kikuchi             |
|Yes |keep this Johnson Replacement (Till Ep. 67) |
|Yes |Saban/ocean (Till Ep. 67)                  |
|Yes |Smith/Faulconer Score (From Ep. 68)|
|Yes |Original Funi Dub (From Ep. 68)
|Yes |Use R2J Dragon box jpn audio  |
|No  |Remove UUE dubs               |

Audio mappings:
`-map 0:a -map -0:a:0 -map -0:a:5 -c:a libopus -ac 2 -ab 128k`

Muxing:
```cmd
for %%i in (*.mkv) do (
ffmpeg -v quiet -stats -hide_banner -i "%%i" -i "../%%i" -map 0 -map 1:a:4 -map 1:a:1 -map 1:a:2 -map 1:a:3 -map 1:s -map 1:t -c:v copy -c:a libopus -ac 2 -ab 128k -metadata title="[AniDL] Dragon Ball Z [BD 480p 10bit][Soap]" -disposition:a:0 default "a%%i"
"C:/Program Files/MKVToolNix\mkvmerge.exe" -o "b%%i" "a%%i"
del "a%%i"
)
