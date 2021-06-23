"""Fate Stay Night Heaven's Feel I. Presage Flower"""
__author__ = 'Soap'

import vapoursynth as vs
import os
import sys
import subprocess
import random

import havsfunc as hvf
import mvsfunc as mvf
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import insaneAA
import vsTAAmbk as taa
from adptvgrnMod import adptvgrnMod as agmod
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth
import vscompare

core = vs.core
core.max_cache_size = 32000
raw = os.path.join(os.getcwd(), " ".join(sys.argv[1:]))
masked = [(600, 645), (9763, 9849), (11417, 11529), (13408, 13527), (15594, 15735), (18494, 18644), (21835, 21894), (24802, 24879), (25114, 25229), (28592, 28710), (30304, 30349), (34957, 35040), (39021, 39160), (39232, 39379), (39750, 39883), (39983, 40118), (41268, 41438), (41496, 41650), (41705, 41838), (41999, 42114), (42145, 42273), (42330, 42454), (42490, 42583), (155646, 155705)]

def compac(src, enc):
    for _ in range(0, 6):
        frame = random.randint(1, 173000)
        src, enc = vscompare.prep(src, enc, w=1920, h=1080, dith=True, yuv444=False)
        vscompare.save(frame, src=src, enc=enc)

def filter_chain(clip):
    # print(clip.decode('utf-8'))
    src = lvf.src(clip)
    src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
    src = depth(src, 16)

    #params
    height = 855
    width = (height/9)*16
    b = 0.26
    c = 0.37

    #descale and upscale
    descale = depth(lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=b, c=c)), 16)
    dehalo = hvf.DeHalo_alpha(descale, darkstr=0)
    upscale = nnedi3_rpow2(dehalo).resize.Spline36(src.width, src.height)
    upscale = join([upscale, plane(src, 1), plane(src, 2)])

    #denoising
    ref_a = hvf.SMDegrain(upscale, tr=1, thSAD=64, plane=4)
    den_a = mvf.BM3D(upscale, sigma=[4, 1.2], ref=ref_a)
    ref_b = hvf.SMDegrain(upscale, tr=1, thSAD=128, plane=4)
    den_b = mvf.BM3D(upscale, sigma=[2.4, 0.8], ref=ref_b)
    adaptive_mask = kgf.adaptive_grain(upscale, luma_scaling=8, show_mask=True)
    denoise = core.std.MaskedMerge(den_a, den_b, adaptive_mask)

    #Edge-detection and debanding
    line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
    deband = core.f3kdb.Deband(denoise, range=18, y=56, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
    deband = core.std.MaskedMerge(deband, upscale, line_mask)

    #Add grain and exclude few frames from output
    grain = agmod(deband, strength=0.30, size=1, sharp=75, static=True)
    final = depth(lvf.rfs(grain, src, ranges=masked), 10)

    #generate comps 
    compac(src, final)

    return final


def encode_chain(clip: vs.VideoNode)-> None:
    """Output to ffv1"""
    print("\n\nFFV1 encode starts")
    ffmpeg_args = [
            "ffmpeg", "-hide_banner", "-v", "quiet", "-stats",
            "-f", "yuv4mpegpipe", "-i", "-",
            "-c:v", "ffv1", "-level", "3", "-threads", "8",
            "-map", "0", "-pix_fmt", "yuv420p10le", "presageFiltered.mkv"
            ]
    process = subprocess.Popen(ffmpeg_args, stdin=subprocess.PIPE)
    clip.output(process.stdin, y4m=True, progress_update=lambda value, endvalue: print(f"\rVapourSynth: {value}/{endvalue} ~ {100 * value // endvalue}% || Encoder: ", end=""))
    process.communicate()
    print("FFV1 process ends")


if __name__ == '__main__':
    filtered = filter_chain(raw)
    encode_chain(filtered)
