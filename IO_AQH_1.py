import numpy as np
import gdsfactory as gf
import gdsfactory.components as gc
from shapely import snap
from Straight import Straight
from Bend import Bend

@gf.cell
def IO_AQH_1(TotLengthX  = 500,
        TotLengthY   = 400,
        InLengthX    = 100,
        InLengthY    = 200,
        MidLengthX   = 20,
        
        CouplingLength = 20,
        BendRadius  = 30,
        WgWidth     = 1.8,
        Layer       = (3,0)
):  
        
        IO_AQH = gf.Component("IOAQH1")

        snap = gf.snap.snap_to_grid

        Projection = np.cos(np.pi/4)

        LengthX1   = snap(InLengthX - 2*BendRadius - MidLengthX - BendRadius*Projection - BendRadius/Projection - CouplingLength/2 * Projection)
       
        LengthY1   = snap(InLengthY - 2*BendRadius + BendRadius*(1-Projection) - CouplingLength/2 * Projection)
        
        LengthY2   = snap(TotLengthY - InLengthY - CouplingLength/2 * Projection - BendRadius/Projection - BendRadius*Projection - BendRadius)
        
        OutLengthX = snap(TotLengthX - InLengthX - CouplingLength/2 * Projection + BendRadius*(1-Projection)  - BendRadius)

        # Components
        # InX    = IO_AQH << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer)
        # Bend1  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        # Y1     = IO_AQH << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)
        # Bend2  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        # X1     = IO_AQH << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer)
        # Bend3  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=45, Layer=Layer)     
        # Bend4  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        # A      = IO_AQH << Straight(Length=CouplingLength, Width=WgWidth, Layer=Layer)
        # Bend5  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=-90, Layer=Layer)
        # Bend6  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=45, Layer=Layer)
        # Y2     = IO_AQH << Straight(Length=LengthY2, Width=WgWidth, Layer=Layer)
        # Bend7  = IO_AQH << Bend(Radius=BendRadius, Width=WgWidth, angle=90, Layer=Layer)
        # OutX   = IO_AQH << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)

        # # Connections
        # Bend1.connect("o1", InX.ports["o2"])
        # Y1.connect("o1", Bend1.ports["o2"])
        # Bend2.connect("o1", Y1.ports["o2"])
        # X1.connect("o1", Bend2.ports["o2"])
        # Bend3.connect("o1", X1.ports["o2"])
        # Bend4.connect("o1", Bend3.ports["o2"])
        # A.connect("o1", Bend4.ports["o2"])
        # Bend5.connect("o1", A.ports["o2"])
        # Bend6.connect("o1", Bend5.ports["o2"])
        # Y2.connect("o1",Bend6.ports["o2"])
        # Bend7.connect("o1",Y2.ports["o2"])
        # OutX.connect("o1", Bend7.ports["o2"])

        # IO_AQH.add_port(name="o1", port=InX.ports["o1"])
        # IO_AQH.add_port(name="o2", port=OutX.ports["o2"])

        #IO_AQH.flatten()

        ########################################################################
        # Cross section
        ########################################################################
        xs = gf.cross_section.cross_section(width=WgWidth,layer=Layer,)

        # Build continuous path
        p = gf.Path()

        # InX
        p.append(gf.path.straight(length=LengthX1))

        # Bend1 (-90)
        p.append(gf.path.arc(radius=BendRadius, angle=-90))

        # Y1
        p.append(gf.path.straight(length=LengthY1))

        # Bend2 (+90)
        p.append(gf.path.arc(radius=BendRadius, angle=90))

        # X1
        p.append(gf.path.straight(length=MidLengthX))

        # Bend3 (+45)
        p.append(gf.path.arc(radius=BendRadius, angle=45))

        # Bend4 (-90)
        p.append(gf.path.arc(radius=BendRadius, angle=-90))

        # Coupling region
        p.append(gf.path.straight(length=CouplingLength))

        # Bend5 (-90)
        p.append(gf.path.arc(radius=BendRadius, angle=-90))

        # Bend6 (+45)
        p.append(gf.path.arc(radius=BendRadius, angle=45))

        # Y2
        p.append(gf.path.straight(length=LengthY2))

        # Bend7 (+90)
        p.append(gf.path.arc(radius=BendRadius, angle=90))

        # OutX
        p.append(gf.path.straight(length=OutLengthX))

        # Extrude into waveguide
        Waveguide = gf.path.extrude(p, cross_section=xs)

        Waveguide_Ref = IO_AQH << Waveguide

        # Add ports
        IO_AQH.add_port("o1", port=Waveguide_Ref.ports["o1"])
        IO_AQH.add_port("o2", port=Waveguide_Ref.ports["o2"])

        IO_AQH.ymax = WgWidth/2

        return IO_AQH
        