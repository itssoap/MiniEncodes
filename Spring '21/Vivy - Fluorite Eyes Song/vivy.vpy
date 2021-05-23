import vapoursynth as vs
core = vs.get_core(threads=8)

core.max_cache_size=32000
#core.std.LoadPlugin(path="C:/Users/Administrator/AppData/Local/Programs/VapourSynth/plugins64/Bilateral.dll")
import os
import edi_rpow2
import havsfunc as hvf
import mvsfunc as mvf
#import fag3kdb
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth

# reading file and converting to 16bit
key = key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)
src = src.resize.Spline36(range_in_s="full", range_s="limited")
#src.set_output()

height = 810
width = (height/9) * 16

# Extracting luma and descaling
descale = lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3))
descale = depth(descale, 16)

ref = hvf.SMDegrain(descale, tr=1, thSAD=300, plane=4)
denoise = mvf.BM3D(descale, sigma=[4, 1.2, 0.6], ref=ref)

# AA
aa = taa.TAAmbk(descale, aatype='Nnedi3')


# Upscaling back
upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = join([upscale, plane(src, 1), plane(src, 2)])
upscale = depth(upscale, 16)
# Deband
deb = core.f3kdb.Deband(upscale, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)

# Graining 
grain = kgf.adaptive_grain(deb,0.30, luma_scaling=8)

# Dithering back to 10bit
final = depth(grain, 10)

# Output
final.set_output()
