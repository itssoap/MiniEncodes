import vapoursynth as vs
core = vs.get_core()

core.max_cache_size=14000
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

dark=[(529, 636),(703, 1008),(1231, 1344),(1588, 2271),(2373, 2459),(2952, 3055),(3719, 3822),(3912, 3965),(4124, 4203),(4485, 4656),(4783, 29528),(34076, 34852),(35026, 41989),(42296, 46752),(46825, 50432),(50539, 52407),(52724, 54344),(54460, 54462),(54512, 54576),(54781, 55366),(58836, 58868),(59901, 60124),(66402,66787),(70253, 70468),(73346, 73560),(78691, 79226),(84570, 85232),(85730, 85834),(86913, 87236),(87476, 90936),(99613, 100018),(100709, 101745),(104298, 104900),(105182,105192),(107990, 108692),(108953, 111811),(112013, 113556),(114088, 114118),(115478, 117262),(118411, 120411),(122814, 123294),(123730, 124715),(127088, 128815),(129008, 129812),(131052, 138993),(141112, 150857),(152275, 157391),(159324, 159863),(160680, 161035)]

# reading file and converting to 16bit
key = key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source)
#src.set_output()
src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)

height = 855
width = (height/9) * 16

# Extracting luma and descaling
descale = lvf.scale.descale(clip=src, upscaler=None, height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3))
descale = depth(descale, 16)

# Denoise
denoise = mvf.BM3D(descale, sigma=[1.0,0,0])
heavy_denoise = mvf.BM3D(descale, sigma=[3.0,0,0])
denoise =  lvf.rfs(denoise, heavy_denoise, ranges=dark)

# AA
aa = taa.TAAmbk(denoise, aatype='Nnedi3')

# Upscaling back
upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = join([upscale, plane(src, 1), plane(src, 2)])
upscale = depth(upscale, 16)

# Dehalo
dehalo = haf.DeHalo_alpha(upscale, darkstr=0)

# Deband
deb = core.f3kdb.Deband(dehalo, range=16, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
light_deb = core.f3kdb.Deband(dehalo, range=16, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
moderate_deb = core.f3kdb.Deband(dehalo, range=18, y=56, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deb = lvf.rfs(deb, moderate_deb, ranges=dark)

# Graining 
grain = kgf.adaptive_grain(clip=deb, strength=0.4, luma_scaling=8)
dyn_gr = kgf.adaptive_grain(clip=deb, strength=3.0, luma_scaling=4, static=False)
grain = lvf.rfs(grain, dyn_gr, ranges=dark)

# Dithering back to 10bit
final = fvf.Depth(grain, 10)

# Output
final.set_output()
