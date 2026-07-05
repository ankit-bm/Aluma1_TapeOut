import gdsfactory as gf
import gdsfactory.components as gc
from Straight import Straight
from Bend import Bend

@gf.cell
def IO_2D_1(TotLengthX  = 500,
        TotLengthY   = 400,
        InLengthX    = 100,
        InLengthY    = 200,
        MidLengthX   = 20,
        CouplingLengthY = 20,
        BendRadius  = 30,
        WgWidth     = 1.8,
        Layer       = (3,0)
):

        
        LengthX1   = InLengthX - 3*BendRadius - MidLengthX
        LengthY1   = InLengthY - 3*BendRadius - CouplingLengthY/2
        
        LengthY2   = TotLengthY - 6*BendRadius - LengthY1 - CouplingLengthY
        
        OutLengthX = TotLengthX - LengthX1 - 2*BendRadius

        

        IO_2D_1 = gf.Component()

        # Components

        InX    = IO_2D_1 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer)
        Bend1  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        Y1     = IO_2D_1 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)
        Bend2  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        X1     = IO_2D_1 << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer)
        Bend3  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        Y2     = IO_2D_1 << Straight(Length=CouplingLengthY, Width=WgWidth, Layer=Layer)
        Bend4  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        X2     = IO_2D_1 << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer)
        Bend5  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        Y3     = IO_2D_1 << Straight(Length=LengthY2, Width=WgWidth, Layer=Layer)
        Bend6  = IO_2D_1 << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        OutX   = IO_2D_1 << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)

        # Connections
        Bend1.connect("o1", InX.ports["o2"])
        Y1.connect("o1", Bend1.ports["o2"])
        Bend2.connect("o1", Y1.ports["o2"])
        X1.connect("o1", Bend2["o2"])
        Bend3.connect("o1", X1["o2"])
        Y2.connect("o1", Bend3["o2"])
        Bend4.connect("o1", Y2["o2"])
        X2.connect("o1", Bend4["o2"])
        Bend5.connect("o1", X2["o2"])
        Y3.connect("o1", Bend5["o2"])
        Bend6.connect("o1", Y3["o2"])
        OutX.connect("o1", Bend6["o2"])

        IO_2D_1.add_port(name="o1", port=InX.ports["o1"])
        IO_2D_1.add_port(name="o2", port=OutX.ports["o2"])

        IO_2D_1.ymax = WgWidth/2

        return IO_2D_1
