import glob
from subprocess import run
import psutil

def finishing(i):
    run("\"C:/Program Files/MKVToolNix/mkvmerge.exe\" -o \"b"+i+"\" \"a"+i+"\"", shell=True)
    run("rem *.wav", shell=True)
    run("rem *.aac", shell=True)

def processing(file):
    file = file.replace("&", "^&")
    i = file
    run("echo "+file, shell=True)
    run("ffmpeg -y -hide_banner -v quiet -stats -i \"../"+file+"\" -map 0:a:0 Japanese.wav", shell=True)
    for p in psutil.process_iter():
        try:
            if "Japanese.wav" in str(p.open_files()):
                print(p.name())
                print("^^^^^^^^^^^^^^^^^")
                p.kill()
        except:
            continue
    run("qaac64 -V 73 Japanese.wav -o Jap.aac", shell=True)
    if str(file) == "S01ED-Yume Ja Nai [Hatena].mkv" or file == "S01OP-Shanghai Honey [ORANGE RANGE].mkv":
        run("ffmpeg -y -hide_banner -v quiet -stats -i \""+i+"\" -i \"Jap.aac\" -i \"../"+i+"\" -map 0 -map 1 -map 2 -map -2:v -map -2:a -c copy -map_metadata:g -1 -metadata title=\"[AniDL] Taisou Zamurai [BD 480p 10bit][Soap]\" -metadata:s:v title=\"\" -metadata:s:a title=\"Japanese\" \"a"+i+"\"", shell=True)
    else:
        run("ffmpeg -y -hide_banner -v quiet -stats -i \"../"+i+"\" -map 0:a:1 English.wav", shell=True)
        for p in psutil.process_iter():
            try:
                if "English.wav" in str(p.open_files()):
                    print(p.name())
                    print("^^^^^^^^^^^^^^^^^")
                    p.kill()
            except:
                continue
        run("qaac64 -V 73 English.wav -o Eng.aac", shell=True)
        run("ffmpeg -y -hide_banner -v quiet -stats -i \""+i+"\" -i \"Jap.aac\" -i \"Eng.aac\" -i \"../"+i+"\" -map 0 -map 1 -map 2 -map 3 -map -3:v -map -3:a -c copy -map_metadata:g -1 -metadata title=\"[AniDL] Taisou Zamurai [BD 480p 10bit][Soap]\" -metadata:s:v title=\"\" -metadata:s:a:0 title=\"Japanese\" -metadata:s:a:1 title=\"English\" \"a"+i+"\"", shell=True)
    finishing(i)

def main():
    files = glob.glob('*.mkv')
    for i in files:
        processing(i)
        
if __name__ == '__main__':
    main()
