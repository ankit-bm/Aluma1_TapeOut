import gdsfactory as gf

from Racetrack import Racetrack
import numpy as np

@gf.cell
def AQH_Lattice(
        Nx = 8, 
        Ny = 8, 
        BendRadius = 20.0,
        LengthSR   = 12.0,
        eta        = 0.110,
        Gap        = 0.5, 
        WgWidth    = 1.8, 
        Euler      = 1,
        Layer      = (2,0) ):
    
    
    Lattice = gf.Component()
    Layer1 = (1, 0)  # Define Layer 1
    Layer2 = (2, 0)  # Define Layer 2
    
    LengthLR = LengthSR + eta
    
    NyD = Nx - Ny

    SR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthSR, LengthY=LengthSR, Euler = Euler, Layer=Layer)
    
    LR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthLR, LengthY=LengthLR, Euler = Euler, Layer=Layer)
    
    
    for j in range(NyD,2*Nx+1-NyD):
            
            Y0 = (j-1) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)

            if j <= Nx:
                for i in np.arange(Nx-j+1, Nx+j-1+2,2):
                    X0 = (i-Nx) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                    SiteRing = Lattice << SR
                    SiteRing.move((X0, Y0)) 
            else:
                for i in np.arange(j-Nx+1, 3*Nx-j-1+2,2):
                    X0 = (i-Nx) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                    SiteRing = Lattice << SR
                    SiteRing.move((X0, Y0)) 
                    
                    
            if j < Nx and j % 2 == 0:
                for i in np.arange(Nx-j, Nx+j+2,2):
                    X0 = (i-Nx) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                    LinkRing = Lattice << LR
                    LinkRing.move((X0, Y0)) 
            elif j == Nx and j % 2 == 0:
                for i in np.arange(Nx-j+2, Nx+j,2):
                    X0 = (i-Nx) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                    LinkRing = Lattice << LR
                    LinkRing.move((X0, Y0))              
            elif j % 2 == 0:
                for i in np.arange(j-Nx, 3*Nx-j+2,2):
                    X0 = (i-Nx) * (Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                    LinkRing = Lattice << LR
                    LinkRing.move((X0, Y0))
                    
                  
                    
    DeltaX = (Nx/2 - 1/2) * 2 * (Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2)
    DeltaY = (Ny/2 - 1/2) * 2 * (Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) 
    
    Lattice.move((DeltaX,-DeltaY))
 
    return Lattice


