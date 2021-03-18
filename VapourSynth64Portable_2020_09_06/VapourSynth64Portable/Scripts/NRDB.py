import vapoursynth as vs

import importlib


def NRDB(input, deband="", range=None, db_Y=64, db_Cb=0, db_Cr=0, grainY=0, grainC=0, dynamic_grain=False, keep_tv_range=False, nr="", planes=[0], sigma=4.0, sigma2=4.0):
    core = vs.get_core()
    
    src = input
    
    if range is None:
        res = src.width * src.height
    
        if res <= 1024 * 576:
            range = 9
        elif res <= 1280 * 720:
            range = 12
        else:
            range = 15
            
    # let's assume f3kdb doesn't do anything to the chroma planes if Cb and Cr are 0.
    if 1 not in planes:
        db_Cb = 0
    if 2 not in planes:
        db_Cr = 0
            
    
    if len(nr) == 0:
        nred = core.dfttest.DFTTest(clip=src, planes=planes, sigma=sigma, sigma2=sigma2)
    elif nr in ["nop", "nop()"]:
        nred = src
    else:
        if not nr.startswith("core."):
            # How evil is this?
            
            parenthesis = nr.find("(")
            if parenthesis == -1:
                raise RuntimeError("NRDB: no parenthesis found in nr.")
            
            dot = nr.find(".", 0, parenthesis)
            if dot == -1:
                raise RuntimeError("NRDB: no dot found in nr before the first parenthesis.")
            
            module = importlib.import_module(nr[0:dot])
            
            nr = "module" + nr[dot:]
            
        nred = eval(nr.format(clip="src", planes="planes"))
        
        
    noise = core.std.MakeDiff(clipa=src, clipb=nred, planes=planes)
    
    if len(deband) == 0:
        db = core.f3kdb.Deband(nred, range=range, y=db_Y, cb=db_Cb, cr=db_Cr, grainy=grainY, grainc=grainC, sample_mode=2, blur_first=True, dynamic_grain=dynamic_grain, keep_tv_range=keep_tv_range)
    elif deband in ["nop", "nop()"]:
        db = nred
    else:
        if not deband.startswith("core."):
            parenthesis = deband.find("(")
            if parenthesis == -1:
                raise RuntimeError("NRDB: no parenthesis found in deband.")
            
            dot = deband.find(".", 0, parenthesis)
            if dot == -1:
                raise RuntimeError("NRDB: no dot found in deband before the first parenthesis.")
            
            module = importlib.import_module(deband[0:dot])
            
            deband = "module" + deband[dot:]
            
        db = eval(deband.format(clip="nred", planes="planes"))
        
        
    result = core.std.MergeDiff(clipa=db, clipb=noise, planes=planes)
    
    return result
