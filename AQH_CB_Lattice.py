import gdsfactory as gf

from Racetrack import Racetrack
import numpy as np

@gf.cell
def AQH_CB_Lattice(
       Nx = 8, 
       Ny = 8, 
       BendRadius = 20,
       LengthSR   = 12,
       eta        = 0.110,
       Gap        = 0.5, 
       WgWidth    = 1.8, 
       Euler      = 1,
       Layer      = (2,0) ):
    
    
    # Layer1 = (1, 0)  # Define Layer 1
    # Layer2 = (2, 0)  #
    
    Lattice = gf.Component()
    
    MaxX = 2*Nx - 1
    MaxY = 2*Ny - 1
    
    LengthLR = LengthSR + eta
    
    CenterX0  = 0;
    CenterY0  = 0;
    
    SR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthSR, LengthY=LengthSR, Euler = Euler, Layer=Layer)
    LR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthLR, LengthY=LengthLR, Euler = Euler, Layer=Layer)
    
    
    for j in range(1,MaxY+1):
        
        for i in range(1,MaxX+1):
            
            CenterX = CenterX0 + ((i-1)*(LengthSR/2+LengthLR/2+2*BendRadius+Gap+WgWidth))
     
            CenterY = CenterY0 + ((j-1)*(LengthSR/2+LengthLR/2+2*BendRadius+Gap+WgWidth)) 

            if j%2 == 1:   
                if i%2 == 1:
                    
                    LinkRing = Lattice << LR
                    LinkRing.move((CenterX, CenterY)) 
                    
                else:
                    
                    SiteRing = Lattice << SR
                    SiteRing.move((CenterX, CenterY)) 
          

            elif j%2 == 0:
     
                if i%2 == 1:   
                    SiteRing = Lattice << SR
                    SiteRing.move((CenterX, CenterY)) 
                    
                                        
    Lattice.movey(-(LengthLR/2 + LengthSR/2 + 2*BendRadius + Gap + WgWidth))
    
    return Lattice


