import vapoursynth as vs
core = vs.core

import os
import havsfunc as hvf
import lvsfunc as lvf
import kagefunc as kgf
from adptvgrnMod import adptvgrnMod as agmod
from vsutil import plane, join, depth
import stgfunc as stg

def dehalo_clip(src, rescaled) -> vs.VideoNode:
    halo_mask = lvf.mask.halo_mask(rescaled, brz=0.25, rad=1)
    stg.output(halo_mask)
    dehalo = core.std.MaskedMerge(src, rescaled, halo_mask)
    dehalo = hvf.DeHalo_alpha(
                    join([dehalo, plane(src, 1), plane(src, 2)]),
                    darkstr=0, brightstr=0.4
                )
    return dehalo

def deband_clip(denoise, dehalo) -> vs.VideoNode:
    line_mask = kgf.retinex_edgemask(dehalo, sigma=0.5).std.Binarize(16000).rgvs.RemoveGrain(3)
    deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
    deband = core.std.MaskedMerge(dehalo, deband, line_mask)
    return deband


source = "S01E14-Kyoto Sister School Exchange Event - Group Battle 0 -.mkv"
source = lvf.src(source, force_lsmas=True)
src = depth(source, 16)

height = 844

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)

upscale = join([rescale, plane(src, 1), plane(src, 2)])

# mask = core.adg.Mask(core.std.PlaneStats(src), luma_scaling=16)

dehalo = dehalo_clip(src, upscale)

mask = core.adg.Mask(core.std.PlaneStats(dehalo), luma_scaling=48)
mask2 = lvf.mask.detail_mask(dehalo)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=84, plane=4)
denoise = lvf.denoise.bm3d(dehalo, sigma=[0.8, 0], ref=ref)

# line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = deband_clip(denoise, dehalo)

grain = agmod(deband, strength=0.60, size=1, sharp=75, static=True)

final = depth(grain, 10)
stg.output(src)
stg.output(upscale)
stg.output(dehalo)
stg.output(mask)
stg.output(mask2)
stg.output(final)
# stg.output(line_mask)