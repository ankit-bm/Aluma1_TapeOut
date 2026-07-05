import gdsfactory as gf
from Racetrack import Racetrack

@gf.cell
def OneD_Lattice(
        Nx=10, 
        BendRadius = 20,
        LengthX    = 12,
        LengthXL   = 16,
        LengthY    = 12,
        LengthYL   = 16,
        Gap        = 0.5, 
        WgWidth    = 1.8, 
        Euler      = 0,
        Layer      = (2,0) ):
    
    
    Lattice = gf.Component()


    for j in range(1,2*Nx):

        x_pos = (j-1) * (Gap + WgWidth + 2*BendRadius + (LengthX+LengthXL)/2)
       
        if j % 2 == 1:
            SiteRing = Lattice << Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthX, LengthY=LengthY, Euler = Euler, Layer=Layer)
            SiteRing.move((x_pos, 0))
            
        elif j % 2 == 0:
            LinkRing = Lattice << Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthXL, LengthY=LengthYL, Euler = Euler, Layer=Layer)
            LinkRing.move((x_pos, 0))
                            
    # LatticeOffsetX0 =  - 2*np.cos(np.pi/4)*(Gap + WgWidth + 2*BendRadius + (LengthX+LengthXL)/2 )
    # LatticeOffsetY0 =  - 2*np.sin(np.pi/4)*(Gap + WgWidth + 2*BendRadius + (LengthX+LengthXL)/2 )
    
    # Lattice.move((LatticeOffsetX0,LatticeOffsetY0))
                
                
    return Lattice

