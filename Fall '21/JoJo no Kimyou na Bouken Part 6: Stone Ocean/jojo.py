import os
import vapoursynth as vs
import lvsfunc as lvf
from vsutil import depth, plane, join
import kagefunc as kgf
import havsfunc as hvf
import mvsfunc as mvf
from adptvgrnMod import adptvgrnMod as agmod
core = vs.core
core.max_cache_size = 32*2**10
core.num_threads = 8

source = os.path.join(os.getcwd(), key) 
src = lvf.src(source, force_lsmas=True)
src1 = depth(src, 16)
src = core.dfttest.DFTTest(src1, sigma=12, sigma2=12)

# src = lvf.deblock.autodb_dpir(src1.std.SetFrameProp('_Matrix', intval=1), cuda=False)

src = hvf.SMDegrain(src, tr=1, thSAD=64, plane=4)
src = lvf.denoise.bm3d(src, sigma=[4, 0.5], ref=src)

# src.set_output(0)
h = 900
b = 1/3
c = 1/3

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=h, kernel=lvf.kernels.Mitchell()), 16)
upscale = join([rescale, plane(src, 1), plane(src, 2)])
# upscale.set_output(1)

aa = lvf.aa.transpose_aa(upscale, eedi3=False, rep=6)
upscale = aa

line_mask1 = kgf.retinex_edgemask(upscale)
line_mask2 = kgf.retinex_edgemask(upscale).std.Binarize(16000).rgvs.RemoveGrain(3)
line_mask3 = kgf.retinex_edgemask(upscale).std.Binarize(16000).rgvs.RemoveGrain(3).std.Minimum()
line_mask4 = kgf.retinex_edgemask(upscale).std.Binarize(16000).rgvs.RemoveGrain(3).std.Minimum().std.Inflate()

# line_mask1.set_output(2)
# line_mask2.set_output(3)
# line_mask3.set_output(4)
# line_mask4.set_output(5)

dehalo = core.std.MaskedMerge(src1, upscale, line_mask3)
dehalo = join([dehalo, plane(src, 1), plane(src, 2)])
# dehalo.set_output(6)

dehalo = hvf.DeHalo_alpha(dehalo, rx=1.2, darkstr=0.4, brightstr=1)
# dehalo.set_output(7)

deband = core.f3kdb.Deband(dehalo, range=16, y=64, cb=32, cr=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = agmod(deband, strength=0.25, size=0.50, static=True, luma_scaling=6)

# grain.set_output(4)
final = depth(grain, 10)
final.set_output()
