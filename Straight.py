import gdsfactory as gf

@gf.cell
def Straight(Length=10, Width = 1, Layer=(1, 0)):
    
    c = gf.Component()

    snap = gf.snap.snap_to_grid
    
    c.add_polygon([(0, 0), (Length, 0), (Length, Width), (0, Width)], layer=Layer)
    
    c.add_port(name="o1", center=(snap(0), snap(Width / 2)), width=Width, orientation=180, layer=Layer)
    
    c.add_port(name="o2", center=(snap(Length), snap(Width / 2)), width=Width, orientation=0, layer=Layer)
    
    return c
