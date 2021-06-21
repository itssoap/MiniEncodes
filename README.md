# MiniEncodes

I will try compiling all my scripts if possible. Feel free to use them.

### Setting up FFmpeg (and most of the other binaries you might need, like qaac, and also, ffmpegF is just the full-version of ffmpeg):
1. Download the complete package from here: [MEGA](https://mega.nz/folder/Jt1mRB6B#72UQtEMFATwdhsLJba7PmA)
2. Unarchive it and add the bin folder within it to PATH.

### Setting up VapourSynth:
1. Download Portable VapourSynth from here: [MEGA](https://mega.nz/folder/B9kABBxZ#LAztIxaWNLGR4WxRtgdqqg) 
2. Add Python38 folder from Python38.7z to C:/Users/Administrator/AppData/Roaming/Python/
(replace Administrator in step 2 with your username)
3. Add following locations to your PATH: [Click here](https://github.com/Soaibkhan38/MiniEncodes/blob/main/Folders%20to%20add%20to%20path%20for%20VS.txt)

### Installing on Arch (cause if u gonna use Linux, use this and not a Debian distro), run:
1. `pacman-key --init`
2. `pacman-key --populate`
3. `pacman-key --refresh-keys`
4. `pacman -Sy archlinux-keyring`
5. `pacman -Syu`
6. `pacman -S python`      | While installing, make sure that its the latest version
7. `pacman -S vapoursynth` | While installing, make sure that the Vapoursynth version and the python version are compatible with each other
8. Check installation by running `vspipe`
