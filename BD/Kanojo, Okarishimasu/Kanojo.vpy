import vapoursynth as vs
core = vs.get_core()

core.max_cache_size=10000
#core.std.LoadPlugin(path="C:/Users/Administrator/AppData/Local/Programs/VapourSynth/plugins64/Bilateral.dll")
import edi_rpow2
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import vsTAAmbk as taa
import fag3kdb
import vsTAAmbk as taa
key = key.decode()
#source = os.path.join('C:/Users\Administrator\Downloads\[ReinForce] Kanojo Okarishimasu (BDRip 1920x1080 x264 FLAC)\', key) 
src = lvf.src(key)
src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = fvf.Depth(src, 16)
#Deband
clip = taa.TAAmbk(src, aatype='Nnedi3')
clip = fag3kdb.Fag3kdb(clip, radiusy=12, radiusc=8, grainy=50, grainc=50, mask_thr=2, mask_radius=3, keep_tv_range=True)

deb = core.f3kdb.Deband(clip, range=15, y=56, grainy=0, grainc=0, output_depth=16)
# Graining 

deb = kgf.adaptive_grain(deb, 0.30)
# Dithering back to 10bit
final = fvf.Depth(deb, 10)

# Output
final.set_output()
