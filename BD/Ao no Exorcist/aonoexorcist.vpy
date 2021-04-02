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

# Extracting luma plane to apply filters
Y, U, V = kgf.split(src)
Y = depth(Y, 16)

# AA
luma_aa = taa.TAAmbk(Y, aatype='Nnedi3')

denoise = mvf.BM3D(luma_aa, sigma=[3, 0.6, 0.2])

remerge = kgf.join([denoise, U, V])

# Deband
deb = core.f3kdb.Deband(remerge, range=15, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)

# Graining 
grain = kgf.adaptive_grain(deb, 0.25, luma_scaling=8)

# Dithering back to 10bit
final = depth(grain, 10)

# Output
final.set_output()
