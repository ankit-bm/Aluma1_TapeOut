import gdsfactory as gf
from Racetrack import Racetrack

###############################################################################
# Parameters
###############################################################################
@gf.cell
def AFQH_Lattice( 
    Nx          = 7,
    Ny          = 7,
    LengthRing  = 10,
    BendRadius  = 12,
    WgWidth     = 1,
    Gap         = 1,
    Euler       = 0,
    Layer       = (2,0)
):

    Lattice = gf.Component()
    
    R = Racetrack(LengthX=LengthRing,LengthY=LengthRing,BendRadius=BendRadius,WgWidth=WgWidth,Euler = Euler,Layer=Layer)
        
    for i in range(Nx):
        for j in range(Ny):
            
            if j%2 == 0:
        
                R_Ref = Lattice << R
                RingX = i*(LengthRing + 2*BendRadius + WgWidth + Gap)
                RingY = j*(LengthRing + 2*BendRadius + WgWidth + Gap)
        
                R_Ref.move((RingX, RingY))
                
            else:
                if i%2 == 0:
                    
                    R_Ref = Lattice << R
                    RingX = i*(LengthRing + 2*BendRadius + WgWidth + Gap)
                    RingY = j*(LengthRing + 2*BendRadius + WgWidth + Gap)
                    R_Ref.move((RingX, RingY))
                

    return Lattice