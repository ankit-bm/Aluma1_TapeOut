import gdsfactory as gf
from AL_Taper import AL_Taper

gf.CONF.max_cellname_length = 35


@gf.cell
def AL_GratingCoupler(Pitch=0.6,DutyCycle =0.4,UniformGrating = True,NPeriod=20,gaps=(0.1,)*20,widths=(0.25,)*20, polarization="te", taper_length=15.0,
                    GCWidthIO=0.6, WgWidthIO=0.7, LengthGC =60,
                    taper_angle=40.0, fiber_angle=10.0,
                    wavelength=1.55, layer: tuple = (2, 0)):

    AL_GC = gf.Component()
    
    if UniformGrating:
        w      = Pitch * DutyCycle
        g      = Pitch - w
        gaps   = (g,) * NPeriod
        widths = (w,) * NPeriod
    # else: gaps and widths passed directly, used as-is

    gc = AL_GC.add_ref(gf.components.grating_coupler_elliptical_arbitrary(
        gaps=gaps, widths=widths, polarization=polarization,
        taper_length=taper_length, taper_angle=taper_angle,
        fiber_angle=fiber_angle, wavelength=wavelength,layer_slab=None,
        cross_section=gf.cross_section.strip(layer=layer, width=GCWidthIO)))

    if GCWidthIO != WgWidthIO:
        tp = AL_GC.add_ref(AL_Taper(WidthEnd=GCWidthIO, WidthStart=WgWidthIO, Length=LengthGC, Layer=layer))
        tp.connect("o1", gc.ports["o1"])
        AL_GC.add_port("o1", port=tp.ports["o2"])
        AL_GC.add_port("o2", port=gc.ports["o2"])
    else:
        AL_GC.add_ports(gc.ports)

    return AL_GC