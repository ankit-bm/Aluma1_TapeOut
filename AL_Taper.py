import gdsfactory as gf
import numpy as np

gf.CONF.max_cellname_length = 35

@gf.cell
def AL_Taper(WidthEnd=0.6, WidthStart=0.2, Length=395, Layer=(2,0),
            TaperType=1, # 1=Linear, 2=Quadratic, 3=Exponential, 4=CubicBezier(P1,P2)
            BezierP1=0.2, BezierP2=0.8, NPoints=41, MarkerOn=False):

    AL_Taper = gf.Component()

    x = np.linspace(0, Length, NPoints)
    t = x / Length

    if TaperType == 1:
        alpha = t
    elif TaperType == 2:
        alpha = t ** 2
    elif TaperType == 3:
        alpha = np.expm1(t) / np.expm1(1)
    elif TaperType == 4:
        alpha = 3*(1-t)**2 * t * BezierP1 + 3*(1-t) * t**2 * BezierP2 + t**3

    y = WidthEnd/2 + alpha * (WidthStart/2 - WidthEnd/2)

    upper = [[x[i],  y[i]] for i in range(NPoints)]
    lower = [[x[i], -y[i]] for i in range(NPoints-1, -1, -1)]

    AL_Taper.add_polygon(upper + lower, layer=Layer)

    AL_Taper.add_port(name="o1", center=(0, 0),      orientation=180, width=WidthEnd,   layer=Layer)
    AL_Taper.add_port(name="o2", center=(Length, 0), orientation=0,   width=WidthStart, layer=Layer)

    if MarkerOn:
        TipX = AL_Taper.xmax
        for i in range(0, 301, 50):
            Marker = AL_Taper << gf.components.rectangle(size=(1, 7), layer=Layer)
            Marker.xmax = TipX - i
            Marker.ymin = 9

    return AL_Taper