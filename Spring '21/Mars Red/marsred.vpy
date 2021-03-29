import vapoursynth as vs
core = vs.get_core()

core.max_cache_size=10000
#core.std.LoadPlugin(path="C:/Users/Administrator/AppData/Local/Programs/VapourSynth/plugins64/Bilateral.dll")
import os
import edi_rpow2
import havsfunc as haf
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
#src.set_output()
src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)

# Crop the black bars
crop = core.std.Crop(src, 0, 0, 138, 138)

# Denoise
denoise = mvf.BM3D(crop, sigma=[3.0, 0.4, 0])

# AA
aa = taa.TAAmbk(denoise, aatype='Nnedi3')
#aa.set_output()

# Scale to perfection
scale = nnedi3_rpow2(aa).resize.Spline36(1920, 804)
scale = depth(scale, 16)

# Deband
deb = core.f3kdb.Deband(scale, range=16, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)

# Graining 
grain = kgf.adaptive_grain(deb, 0.20, luma_scaling=8)

# Dithering back to 10bit
final = fvf.Depth(grain, 10)

# Output
final.set_output()
