from vapoursynth import core, YUV, GRAY  # You need VapourSynth R37 or later
import fvsfunc as fvf

def Fag3kdb(clp, thry=40, thrc=None, radiusy=12, radiusc=8, grainy=15, grainc=0, dynamic_grainy=False,
               dynamic_grainc=False, mask_thr=2, mask_radius=2, keep_tv_range=True):
    if thrc is None:
        thrc = thry // 2
    clp = fvf.Depth(clp, bits=16)
    mask = fvf.GradFun3(clp, thr_det=mask_thr, mask=mask_radius, bits=16, debug=1)
    U = core.std.ShufflePlanes(clp, 1, GRAY)
    U = U.f3kdb.Deband(range=radiusc, y=thrc, cb=0, cr=0, grainy=grainc, grainc=0,
                       dynamic_grain=dynamic_grainc, keep_tv_range=False, output_depth=16)
    V = core.std.ShufflePlanes(clp, 2, GRAY)
    V = V.f3kdb.Deband(range=radiusc, y=thrc, cb=0, cr=0, grainy=grainc, grainc=0,
                       dynamic_grain=dynamic_grainc, keep_tv_range=False, output_depth=16)
    filtered = core.std.ShufflePlanes([clp,U,V], [0,0,0], YUV)
    filtered = filtered.f3kdb.Deband(range=radiusy, y=thry, cb=0, cr=0, grainy=grainy, grainc=0,
                                     dynamic_grain=dynamic_grainy, keep_tv_range=keep_tv_range, output_depth=16)
    return core.std.MaskedMerge(filtered, clp, mask)
