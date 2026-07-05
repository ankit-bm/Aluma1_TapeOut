import gdsfactory as gf

from Racetrack import Racetrack
import numpy as np

@gf.cell
def IQH_Lattice(
        Nx = 8, 
        Ny = 8, 
        BendRadius = 20,
        LengthSRX  = 12,
        LengthSRY  = 10,
        eta        = 0.08,
        alpha      = 0.08,
        Gap        = 0.5, 
        WgWidth    = 1.2, 
        Euler      = 1,
        Layer      = (2,0) ):
    
    
    #Layer1 = Layer  # Define Layer 1
    #Layer2 = Layer  # Define Layer 2

    Lattice = gf.Component()
    
    MaxX = 2*Nx - 1
    MaxY = 2*Ny - 1
    
    CenterX0  = 0
    CenterY0  = 0
    
    LengthLRX = LengthSRY
    LengthLRY = LengthSRX + 2*eta

    SR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthSRX, LengthY=LengthSRY, Euler = Euler, Layer=Layer)

    LR = Racetrack(BendRadius=BendRadius, WgWidth = WgWidth, LengthX=LengthLRX, LengthY=LengthLRY, Euler = Euler, Layer=Layer)

    
    for j in range(1,MaxY+1):
        
        for i in range(1,MaxX+1):
            
            CenterX = CenterX0 + ((i-1)*(LengthSRX/2+LengthLRX/2+2*BendRadius+Gap+WgWidth))
     
            CenterY = CenterY0 + ((j-1)*(LengthSRY/2+LengthLRY/2+2*BendRadius+Gap+WgWidth)) 


            if j%2 == 1:   
                if i%2 == 1:
                    
                    SiteRing = Lattice << SR
                    SiteRing.move((CenterX, CenterY)) 
                    
                else:
                    CenterY = CenterY + alpha * (j-1)/2
                    LinkRing = Lattice << LR
                    LinkRing.move((CenterX, CenterY)) 
          

            elif j%2 == 0:
     
                if i%2 == 1:   
                    LinkRing = Lattice << LR
                    LinkRing.move((CenterX, CenterY)) 
        
                      
                        
    return Lattice


