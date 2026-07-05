import gdsfactory as gf
import gdsfactory.components as gc
from Straight import Straight
from Bend import Bend

@gf.cell
def IO_2D_3(TotLengthX     = 300, 
        InLengthY       = 250,
        MidLengthX      = 100,
        CouplingLengthY = 25,
        FAGap           = 50,
        BendRadius      = 10,
        WgWidth         = 1.8,
        Layer           = (3,0)
):

    
        TotLengthY = InLengthY + CouplingLengthY/2 + BendRadius
        
        InLengthX = TotLengthX - MidLengthX - 3*BendRadius
        TopLengthX = MidLengthX + FAGap
        OutLengthX  = TotLengthX - TopLengthX - 3*BendRadius

        LengthY1 = InLengthY - 3*BendRadius - CouplingLengthY/2
        LengthY3 = InLengthY + CouplingLengthY/2 - BendRadius - FAGap

        IO_2D_3 = gf.Component()

        InX    = IO_2D_3 << Straight(Length=InLengthX , Width=WgWidth, Layer=Layer)
        Bend1  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        UpY    = IO_2D_3 << Straight(Length=LengthY1,Width=WgWidth, Layer=Layer)
        Bend2  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        MidX   = IO_2D_3 << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer)
        Bend3  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        DownY  = IO_2D_3 << Straight(Length=CouplingLengthY,Width=WgWidth, Layer=Layer)
        Bend4  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        TopX   = IO_2D_3 << Straight(Length=TopLengthX , Width=WgWidth, Layer=Layer)
        Bend5  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        DownY2 = IO_2D_3 << Straight(Length=LengthY3,Width=WgWidth, Layer=Layer)
        Bend6  = IO_2D_3 << Bend(Radius=BendRadius, Width=WgWidth,angle=-90, Layer=Layer)
        OutX   = IO_2D_3 << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)  # ← uses derived OutLengthX

        Bend1.connect("o2",  InX.ports["o2"])
        UpY.connect("o1",  Bend1.ports["o1"])
        Bend2.connect("o1",  UpY.ports["o2"])
        MidX.connect("o1",   Bend2.ports["o2"])
        Bend3.connect("o1",  MidX.ports["o2"])
        DownY.connect("o1", Bend3.ports["o2"])
        Bend4.connect("o1",  DownY.ports["o2"])
        TopX.connect("o1",   Bend4.ports["o2"])
        Bend5.connect("o1",  TopX.ports["o2"])
        DownY2.connect("o1", Bend5.ports["o2"])
        Bend6.connect("o1",  DownY2.ports["o2"])
        OutX.connect("o1",   Bend6.ports["o2"])

        IO_2D_3.add_port(name="o1", port=InX.ports["o1"])
        IO_2D_3.add_port(name="o2", port=OutX.ports["o2"])
        
        #IO_2D_3.mirror_y(0)
        #IO_2D_3.movey(TotLengthY)

        IO_2D_3.ymin = -WgWidth/2 

        return IO_2D_3