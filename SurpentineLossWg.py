import gdsfactory as gf

from Bend import Bend
from Straight import Straight
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

@gf.cell
def SurpentineLossWg(
    WgWidth      = 0.5,
    InLengthX    = 100,
    BendRadiusIO = 25.0,
    NCurves      = 1,
    DeviceID     = "LossWG",
    TaperOn      = False,
    Euler        = 0,
    LabelX       = 0,
    LabelY       = 10,
    Layer        = (2, 0),
    GCParams : dict = dict(
        Pitch          = 0.716,
        DutyCycle      = 0.700,
        NPeriod        = 25,
        taper_length   = 15.0,
        taper_angle    = 40.0,
        fiber_angle    = 10.0,
        wavelength     = 1.55,
        LengthGC       = 100,
        UniformGrating = True,
    ),
    ECParams : dict = dict(
        Length     = 395,
        TaperType  = 1,
        MarkerOn   = True,)
):
    c = gf.Component()

    InX       = c << Straight(Length=InLengthX, Width=WgWidth, Layer=Layer)
    prev_port = InX.ports["o2"]

    for i in range(NCurves):
        angle = -90 if i % 2 == 0 else 90
        B1 = c << Bend(Radius=BendRadiusIO, Width=WgWidth, angle=angle,  Euler=Euler, Layer=Layer)
        B2 = c << Bend(Radius=BendRadiusIO, Width=WgWidth, angle=angle,  Euler=Euler, Layer=Layer)
        Mx = c << Straight(Length=InLengthX, Width=WgWidth, Layer=Layer)
        B1.connect("o1", prev_port)
        B2.connect("o1", B1.ports["o2"])
        Mx.connect("o1", B2.ports["o2"])
        prev_port = Mx.ports["o2"]

    ########################################################################################
    # Tapers / Grating
    ########################################################################################

    if TaperOn:
        Coupler = AL_Taper(WidthStart=WgWidth, Layer=Layer, **ECParams)
    else:
        Coupler = AL_GratingCoupler(GCWidthIO=0.6, WgWidthIO=WgWidth, layer=Layer, **GCParams)
    CPort = "o1"

    C1 = c << Coupler
    C1.connect(C1.ports[CPort], InX.ports["o1"])
    C2 = c << Coupler
    C2.connect(C2.ports[CPort], prev_port)

    c.add_port(name="IN",  port=InX.ports["o1"])
    c.add_port(name="OUT", port=prev_port)

    ###########################################################################
    # Device Info
    ###########################################################################

    DID = c << gf.components.text_rectangular(text=DeviceID, size=1, layer=Layer)
    DID.move((InX.xmin - LabelX, InX.ymax + LabelY))

    return c