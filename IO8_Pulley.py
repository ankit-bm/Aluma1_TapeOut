import gdsfactory as gf
from Straight import Straight
from Bend import Bend
from Pulley import Pulley

gf.gpdk.PDK.activate()

@gf.cell
def  IO8_Pulley( 
    InLengthX   = 100,
    TotLengthX  = 300,
    TotLengthY  = 50,
    Radius      = 50,
    BendRadius  = 30,
    WgWidth     = 1.8,
    ThetaC      = 40,
    Gap         = 0.3,
    BufY        = 50,   # set this equal to FAGap when calling
    Euler       = 1,
    Layer       = (3,0)
):
    
    IO8_Pulley = gf.Component()
    
    ##################################################################################
    # Defined from Bottom to Up
    ##################################################################################
        
    P0      = Pulley(
        Radius     = Radius,
        WgWidth    = WgWidth,
        ThetaC     = ThetaC,
        BendRadius = BendRadius,
        Gap        = Gap,
        InLengthX  = 0,
        Euler      = Euler,
        Layer      = Layer,
    )

    DXP0    = P0.info["DX"]
    DYP0    = P0.info["DY"]

    InLength_Pulley = (TotLengthY - 2*BendRadius - DXP0 - 2*BufY) / 2

    if InLength_Pulley <= 0:
        raise ValueError("TotLengthY too small for IO8_Pulley")

    P       = Pulley(
        Radius     = Radius,
        WgWidth    = WgWidth,
        ThetaC     = ThetaC,
        BendRadius = BendRadius,
        Gap        = Gap,
        InLengthX  = InLength_Pulley,
        Euler      = Euler,
        Layer      = Layer,
    )

    DXP     = P.info["DX"]
    DYP     = P.info["DY"]

    LengthX    = (InLengthX - BendRadius) + DYP - WgWidth
    OutLengthX = TotLengthX - LengthX - 2*BendRadius
    
    ##################################################################################
    # Components
    ##################################################################################

    InX    = IO8_Pulley << Straight(Length=LengthX, Width=WgWidth, Layer=Layer) 
    Bend1  = IO8_Pulley << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer, Euler=Euler)

    Buf1   = IO8_Pulley << Straight(Length=BufY, Width=WgWidth, Layer=Layer)
    InY    = IO8_Pulley << P
    Buf2   = IO8_Pulley << Straight(Length=BufY, Width=WgWidth, Layer=Layer)
        
    Bend2  = IO8_Pulley << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer, Euler=Euler)
    OutX   = IO8_Pulley << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)
    
    ##################################################################################
    # Connections 
    ##################################################################################

    Bend1.connect("o1", InX.ports["o2"])
    Buf1.connect("o1", Bend1.ports["o2"])
    InY.connect("o1", Buf1.ports["o2"])
    Buf2.connect("o1", InY.ports["o2"])
    Bend2.connect("o1", Buf2.ports["o2"])
    OutX.connect("o1", Bend2.ports["o2"])
    
    IO8_Pulley.ymax = WgWidth/2
    
    IO8_Pulley.add_port(name="o1", port=InX.ports["o1"])
    IO8_Pulley.add_port(name="o2", port=OutX.ports["o2"])
    
    return IO8_Pulley


if __name__ == "__main__":
    c = IO8_Pulley(
        InLengthX  = 200,
        TotLengthX = 500,
        TotLengthY = 180,
        Radius     = 20,
        BendRadius = 20,
        WgWidth    = 1.0,
        ThetaC     = 40,
        Gap        = 0.3,
        BufY       = 25,
        Layer      = (1, 0),
    )

    c.show()
    c.plot()
    c.write_gds("IO8_Pulley_test.gds")
    print("Written IO8_Pulley_test.gds")