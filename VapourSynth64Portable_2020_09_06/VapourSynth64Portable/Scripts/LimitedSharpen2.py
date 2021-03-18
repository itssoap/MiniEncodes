import vapoursynth as vs

import muvsfunc


def LimitedSharpen2(clp, ss_x=1.0, ss_y=1.0, dest_x=None, dest_y=None, Smode=4, strength=None, radius=2, Lmode=1, wide=False, overshoot=1, soft=False, edgemode=0, special=False, aSharpS=0.5, aWThresh=0.75, exborder=0):
    core = vs.get_core()
    
    # Avisynth's Round function doesn't do quite the same thing as Python's round function.
    def AvisynthRound(value):
        if value < 0:
            return -int(-value + 0.5)
        else:
            return int(value + 0.5)
    
    
    def UnsharpMask(clip, strength=64, radius=3, threshold=8):
        """Ported by Myrsloik"""
        
        core = vs.get_core()
        
        maxvalue = (1 << clip.format.bits_per_sample) - 1
        
        threshold = threshold * maxvalue // 255
        blurclip = clip.std.Convolution(matrix=[1] * (radius * 2 + 1), planes=0, mode='v')
        blurclip = blurclip.std.Convolution(matrix=[1] * (radius * 2 + 1), planes=0, mode='h')
        
        expressions = ['x y - abs {} > x y - {} * x + x ?'
                                                .format(threshold, strength / 128)]
                                                
        if clip.format.color_family != vs.GRAY:
            expressions.append("")
            
        return core.std.Expr(clips=[clip, blurclip], expr=expressions)
    
    
    if clp.format is None:
        raise RuntimeError("LimitedSharpen2: clips with variable format are not supported.")
    
    if clp.format.color_family == vs.RGB:
        raise RuntimeError("LimitedSharpen2: RGB clips are not supported.")
    
    if clp.format.sample_type == vs.FLOAT:
        raise RuntimeError("LimitedSharpen2: float clips are not supported.")
    
    if clp.format.bits_per_sample > 16:
        raise RuntimeError("LimitedSharpen2: bit depths over 16 are not supported.")
    
    if clp.width == 0 or clp.height == 0:
        raise RuntimeError("LimitedSharpen2: clips with variable dimensions are not supported.")
    
    
    maxvalue = (1 << clp.format.bits_per_sample) - 1
    halfvalue = 1 << (clp.format.bits_per_sample - 1)
    
        
    ox = clp.width
    oy = clp.height
    
    if dest_x is None:
        dest_x = ox
    if dest_y is None:
        dest_y = oy
        
    if strength is None:
        if Smode == 1:
            strength = 160
        else:
            strength = 100
    else:
        if Smode == 2 and strength > 100:
            strength = 100
            
    if overshoot < 0:
        overshoot = 0
        
    overshoot = overshoot * maxvalue // 255
    
        
    xxs = AvisynthRound(ox * ss_x / 8) * 8
    yys = AvisynthRound(oy * ss_y / 8) * 8
    
    smx = dest_x
    smy = dest_y
    if exborder != 0:
        smx = AvisynthRound(dest_x / exborder / 4) * 4
        smy = AvisynthRound(dest_y / exborder / 4) * 4
        
    
    # Simpler than writing planes=0 everywhere.
    last = core.std.ShufflePlanes(clips=clp, planes=0, colorfamily=vs.GRAY)
    
    if ss_x != 1.0 or ss_y != 1.0:
        last = core.resize.Lanczos(clip=last, width=xxs, height=yys)
        
    tmp = last
    
    vertical = core.std.Convolution(clip=tmp, divisor=2, matrix=[ 5,  10,  5,
                                                                  0,   0,  0,
                                                                 -5, -10, -5])
    horizontal = core.std.Convolution(clip=tmp, divisor=2, matrix=[ 5, 0,  -5,
                                                                   10, 0, -10,
                                                                    5, 0,  -5])
    edge = core.std.Expr(clips=[vertical, horizontal], expr="x y max")
    edge = core.std.Levels(clip=edge, min_in=0, max_in=halfvalue, gamma=0.86, min_out=0, max_out=maxvalue)
    
    bright_limit = tmp
    if soft:
        bright_limit = muvsfunc.Blur(clip=bright_limit, amountH=1.0)
        
    dark_limit = core.std.Minimum(clip=bright_limit)
    bright_limit = core.std.Maximum(clip=bright_limit)
    
    if wide:
        dark_limit = dark_limit.std.Inflate().std.Deflate().std.Minimum()
        bright_limit = bright_limit.std.Deflate().std.Inflate().std.Maximum()
        
    if special:
        minmaxavg = core.std.MaskedMerge(clipa=dark_limit, clipb=bright_limit, mask=tmp)
    else:
        minmaxavg = core.std.Expr(clips=[bright_limit, dark_limit], expr="x y + 2 /")
        
    if Smode == 1:
        normsharp = UnsharpMask(clip=last, strength=strength, radius=radius, threshold=0)
    elif Smode == 2:
        normsharp = muvsfunc.Sharpen(clip=last, amountH=strength / 100.0)
    elif Smode == 3:
        normsharp = core.std.Expr(clips=[tmp, minmaxavg], expr="x x y - {strength} * +".format(strength=strength / 100.0))
    else:
        normsharp = core.asharp.ASharp(clip=last, t=aSharpS, d=0, b=0)
        normsharp = core.warp.AWarpSharp2(clip=normsharp, depth=1, blur=3, type=1, thresh=aWThresh * 256)
        
    if Lmode == 1:
        last = core.std.Expr(clips=[bright_limit, normsharp], expr="y x {overshoot} + < y x {overshoot} + ?".format(overshoot=overshoot))
        last = core.std.Expr(clips=[dark_limit, last], expr="y x {overshoot} - > y x {overshoot} - ?".format(overshoot=overshoot))
    else:
        last = core.std.Expr(clips=[bright_limit, normsharp], expr="y x {overshoot} + < y x y x - {overshoot} - 1 2 / pow + {overshoot} + ?")
        last = core.std.Expr(clips=[dark_limit, last], expr="y x {overshoot} - > y x x y - {overshoot} - 1 2 / pow - {overshoot} - ?")
        
    if edgemode == 0:
        pass
    else:
        edge = muvsfunc.Blur(clip=edge.std.Inflate().std.Inflate(), amountH=1.0)
        
        if edgemode == 1:
            last = core.std.MaskedMerge(clipa=tmp, clipb=last, mask=edge)
        else:
            last = core.std.MaskedMerge(clipa=last, clipb=tmp, mask=edge)
            
    if ss_x != 1.0 or ss_y != 1.0 or dest_x != ox or dest_y != oy:
        last = core.resize.Lanczos(clip=last, width=dest_x, height=dest_y)
        
    ex = core.std.BlankClip(clip=last, width=smx, height=smy, color=maxvalue, length=1)
    ex = core.std.AddBorders(clip=ex, left=2, right=2, top=2, bottom=2, color=0)
    ex = muvsfunc.Blur(clip=ex, amountH=1.3)
    ex = core.std.Minimum(clip=ex)
    ex = muvsfunc.Blur(clip=ex, amountH=1.3)
    ex = core.resize.Bicubic(clip=ex, width=dest_x, height=dest_y, filter_param_a=1.0, filter_param_b=0.0)
    ex = core.std.Loop(clip=ex, times=last.num_frames)
    
    tmp = core.resize.Lanczos(clip=clp, width=dest_x, height=dest_y)
    
    if tmp.format.color_family != vs.GRAY:
	    last = core.std.ShufflePlanes(clips=[last, tmp], planes=[0, 1, 2], colorfamily=tmp.format.color_family)
    
    if exborder != 0:
        last = core.std.MaskedMerge(clipa=tmp, clipb=last, mask=ex, planes=0)
        
    return last
