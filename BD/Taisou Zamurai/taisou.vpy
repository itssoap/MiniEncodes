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
#src.set_output()

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)

height = 844
width = (height/9) * 16

# Extracting luma and descaling
descale = lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3))
descale = depth(descale, 16)
#descale.set_output()

# Denoising and AA
ref = hvf.SMDegrain(descale, tr=1, thSAD=300, plane=4)
denoise = mvf.BM3D(descale, sigma=[3.4, 1.0], ref=ref)
aa = taa.TAAmbk(denoise, aatype='Nnedi3')

#aa = fvf.AutoDeblock(aa)

# Upscaling back
upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = join([upscale, plane(src, 1), plane(src, 2)])
upscale = depth(upscale, 16)
#upscale.set_output()

# Deband
deb = core.f3kdb.Deband(upscale, range=15, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)

# Graining 
grain = kgf.adaptive_grain(deb, 1.30)

# Dithering back to 10bit
final = depth(grain, 10)

# Output
final.set_output()
