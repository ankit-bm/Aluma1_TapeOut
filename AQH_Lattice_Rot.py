import gdsfactory as gf

from Racetrack import Racetrack
import numpy as np

@gf.cell(check_instances=False)
def AQH_Lattice_Rot(
        Nx = 8, 
        Ny = 8, 
        BendRadius = 20.0,
        LengthSR   = 12.0,
        eta        = 0.110,
        Gap        = 0.5, 
        WgWidth    = 1.8, 
        Euler      = 1,
        Layer      = (2,0) ):
    
    
    #Layer1 = (1, 0)  # Define Layer 1
    #Layer2 = (2, 0)  # Define Layer 2

    Lattice = gf.Component()

    LengthLR = LengthSR + eta
    
    NyD = Nx - Ny

    SR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthSR, LengthY=LengthSR, Euler = Euler, Layer=Layer)
    
    LR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthLR, LengthY=LengthLR, Euler = Euler, Layer=Layer)
    
    
    for j in range(2*Ny+1):
        for i in range(2*Nx+1):
        
                X0 = (i) * np.cos(np.deg2rad(45))*(Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)
                Y0 = (j) * np.cos(np.deg2rad(45))*(Gap + WgWidth + 2*BendRadius + (LengthSR+LengthLR)/2)

                if i%2 == 1 and j%2 == 1:
                    SiteRing = Lattice << SR
                    SiteRing.rotate(45,(0,0))
                    SiteRing.move((X0, Y0)) 
                elif i%2 == 0 and j%2 == 0 and (i+j)%4 == 0: 
                    if (i == 0 and j == 0) or (i == 2*Nx and j == 0):
                        pass
                    else:
                        LinkRing = Lattice << LR
                        LinkRing.rotate(45,(0,0))
                        LinkRing.move((X0, Y0)) 
               
                    
    DeltaX = np.cos(np.deg2rad(45)) * (Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2)
    DeltaY = np.cos(np.deg2rad(45)) * (Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) 
    
    Lattice.move((-DeltaX,-DeltaY))

    Lattice.flatten()
 
    return Lattice


