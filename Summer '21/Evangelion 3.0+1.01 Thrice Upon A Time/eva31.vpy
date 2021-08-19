"""Evangelion 3.0+1.01 Thrice Upon A Time"""
__author__ = 'Soap'

import vapoursynth as vs
core = vs.core

import os
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
import atomchtools as atf
from cooldegrain import CoolDegrain
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth

def compac(src, enc):
    for _ in range(0, 6):
        frame = random.randint(1, 208646)
        src, enc = vscompare.prep(src, enc, w=1920, h=816, dith=True, yuv444=False)
        vscompare.save(frame, src=src, enc=enc)
        
raw = os.path.join(os.getcwd(), "evaRaw.mkv")
source = lvf.src(raw)
src = depth(source, 16)

height = 762

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)
upscale = join([rescale, plane(src, 1), plane(src, 2)])
    
ref = hvf.SMDegrain(upscale, tr=1, thSAD=84, plane=4)
denoise = mvf.BM3D(upscale, sigma=[2.0, 1.0], ref=ref)

line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(denoise, range=18, y=128, cb=32, cr=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deband = core.std.MaskedMerge(deband, upscale, line_mask)
deband =  lvf.rfs(deband, src, ranges=[(208647, 224305)])
grain = agmod(deband, strength=0.30, size=1, sharp=75, static=True)

final = fvf.Depth(grain, 10)

# compac(src, final)

final.set_output()
