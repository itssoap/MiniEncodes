import vapoursynth as vs
core = vs.core

import os
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

source = "00002.m2ts"
source = lvf.src(source)
source = depth(source, 16)

op = "00005.m2ts"
op = lvf.src(op)         # this is the OP without credits
op = depth(op, 16)

cred = source[1342:3501] # this is the OP with credits

height = 844

src = source[:1342]+op[:2159]+source[3501:]

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)
#dehalo = hvf.DeHalo_alpha(rescale)
# upscale = insaneAA.rescale(dehalo, dx=src.width, dy=src.height)
# aa = insaneAA.insaneAA(src, external_aa=upscale)
upscale = join([rescale, plane(src, 1), plane(src, 2)])

ref = hvf.SMDegrain(upscale, tr=1, thSAD=84, plane=4)
denoise = mvf.BM3D(upscale, sigma=[2.4, 1.0], ref=ref)

line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(denoise, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deband = core.std.MaskedMerge(deband, upscale, line_mask)

#error = core.std.Expr([cred, op], 'x y - abs')#, format = vs.YUV420P16)
op_fin = atf.ApplyCredits(cred, op[:2159], deband[1342:3501])
op_fin = CoolDegrain(op_fin, thsad=16, thsadc=48, blksize=8, overlap=4)
#error = core.std.MaskedMerge(cred, op, error)
#credits = core.std.Expr([cred, error], 'x 55800 > y 2500 > and 255 0 ?') #, format=vs.GRAY8)
#src = fvf.Depth(Y, 10)

mrg_op = deband[:1342]+op_fin+deband[3501:]
#den_cred = core.knlm.KNLMeansCL(out, d=2, s=2, h=1.4, device_type='cpu')

grain = agmod(mrg_op, strength=0.30, size=1, sharp=75, static=True)

final = fvf.Depth(grain, 10)
#final = core.text.Text(final, text="Final Morex2 Dehalo")
#source.set_output(0)
final.set_output()
