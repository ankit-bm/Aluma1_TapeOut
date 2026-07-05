import gdsfactory as gf

@gf.cell
def Bend(Radius = 10, Width = 1, angle = 90, Layer = (1,0), Euler = 0):
    
    if Euler == 1:
        return gf.components.bend_euler(
            radius=Radius,
            width=Width,
            angle=angle,
            layer=Layer,
            allow_min_radius_violation=True,
        )
    else:
        return gf.components.bend_circular(
            radius=Radius,
            width=Width,
            angle=angle,
            layer=Layer,
            allow_min_radius_violation=True,
        )