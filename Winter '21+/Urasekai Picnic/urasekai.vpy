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
# here, key is a cli-argument
key = key.decode()
source = os.path.join(os.getcwd(), key) 
src = lvf.src(source)

# Setting fps (needed) and dithering to 16bit data
src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)

height = 844
width = (height/9) * 16

# Extracting luma and descaling
descale = lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3))
descale = depth(descale, 16)
 
# Denoise
denoise = mvf.BM3D(descale, sigma=1.8)

# AA
aa = taa.TAAmbk(denoise, aatype='Nnedi3')

# Upscaling back
upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = join([upscale, plane(src, 1), plane(src, 2)])
upscale = depth(upscale, 16)

# Deband
deb = core.f3kdb.Deband(upscale, range=15, y=56, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)

# Graining 
grain = kgf.adaptive_grain(deb, 0.3)

# Dithering back to 10bit
final = depth(deb, 10)

# Output
final.set_output()
