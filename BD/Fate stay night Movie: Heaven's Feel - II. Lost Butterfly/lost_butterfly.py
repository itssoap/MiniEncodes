"""Fate Stay Night Heaven's Feel II. Lost Butterfly"""
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
core.max_cache_size = 40000
raw = os.path.join(os.getcwd(), " ".join(sys.argv[1:]))
masked = [(6873, 6988), (7014, 7122), (7152, 7266), (7298, 7403), (7431, 7533), (7560, 7653), (7680, 7792), (7818, 7906), (7933, 8011), (8034, 8101), (8122, 8227), (8251, 8349), (8372, 8501), (35048, 35305), (166713, 166800), (167471, 167628), (167793, 167971), (167999, 168144)]

def compac(src, enc):
    for i in [13355, 79259, 85924, 90630, 97819]:
        frame = i
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
    b = 1/3
    c = 1/3

    #descale and upscale
    descale = depth(lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=b, c=c)), 16)
    dehalo = hvf.DeHalo_alpha(descale, darkstr=0)
    #dehalo = mvf.BM3D(dehalo, sigma=[3.2, 0.8])
    upscale = insaneAA.rescale(dehalo, dx=src.width, dy=src.height)
    aa = insaneAA.insaneAA(src, external_aa=upscale)
    upscale = join([aa, plane(src, 1), plane(src, 2)])

    #denoising
    ref_a = hvf.SMDegrain(upscale, tr=1, thSAD=64, plane=4)
    den_a = mvf.BM3D(upscale, sigma=[3.2, 0.8], ref=ref_a)
    ref_b = hvf.SMDegrain(upscale, tr=1, thSAD=128, plane=4)
    den_b = mvf.BM3D(upscale, sigma=[1.8, 0.8], ref=ref_b)
    adaptive_mask = kgf.adaptive_grain(upscale, luma_scaling=8, show_mask=True)
    denoise = core.std.MaskedMerge(den_a, den_b, adaptive_mask)

    #Edge-detection and debanding
    line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
    deband = core.f3kdb.Deband(denoise, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
    deband = core.std.MaskedMerge(deband, upscale, line_mask)

    #Add grain and exclude few frames from output
    grain = agmod(deband, strength=0.20, size=1, sharp=75, static=True)
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
            "-map", "0", "-pix_fmt", "yuv420p10le", "lostFiltered.mkv"
            ]
    process = subprocess.Popen(ffmpeg_args, stdin=subprocess.PIPE)
    clip.output(process.stdin, y4m=True, progress_update=lambda value, endvalue: print(f"\rVapourSynth: {value}/{endvalue} ~ {100 * value // endvalue}% || Encoder: ", end=""))
    process.communicate()
    print("FFV1 process ends")


if __name__ == '__main__':
    filtered = filter_chain(raw)
    encode_chain(filtered)
