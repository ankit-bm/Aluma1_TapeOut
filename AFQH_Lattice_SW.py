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
    GapS        = 1,
    GapW        = 5,
    Euler       = 0,
    Layer       = (2,0)
):

    Lattice = gf.Component()
    
    LxS = LengthRing
    LyS = LengthRing
    
    LxA = LengthRing + (GapW-GapS)
    LyA = LengthRing - (GapW-GapS)

    RS  = Racetrack(LengthX=LxS,LengthY=LyS,BendRadius=BendRadius,WgWidth=WgWidth,Euler = Euler,Layer=Layer)

    RLX = Racetrack(LengthX=LxA,LengthY=LyA,BendRadius=BendRadius,WgWidth=WgWidth,Euler = Euler,Layer=Layer)

    RLY = Racetrack(LengthX=LyA,LengthY=LxA,BendRadius=BendRadius,WgWidth=WgWidth,Euler = Euler,Layer=Layer)
    
    
    for i in range(Nx):
        for j in range(Ny):
            
            if (-1)**(i+j) == 1:
                R_Ref = Lattice << RS
            else:
                if (-1)**j == 1:
                    R_Ref = Lattice << RLX
                else:
                    R_Ref = Lattice << RLY
                        
    
            RingX = i*(LengthRing + 2*BendRadius + WgWidth + GapW/2 + GapS/2)
            RingY = j*(LengthRing + 2*BendRadius + WgWidth + GapW/2 + GapS/2)
    
            R_Ref.move((RingX, RingY))
    

    return AFQH_Lattice