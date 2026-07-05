import numpy as np
import gdsfactory as gf

@gf.cell(check_instances=False)
def Pulley(
    Radius: float = 50,
    WgWidth: float = 1.0,
    ThetaC: float = 40,
    BendRadius: float = 15.0,
    Gap: float = 0.3,
    InLengthX: float = 10.0,
    Euler = 0,
    Layer: tuple = (2, 0),
):
    #------------------------------------------------------------------------
    # Derived geometry
    #------------------------------------------------------------------------
    ArcRadius = Radius + Gap + WgWidth
    HalfTheta_deg = ThetaC / 2.0
    HalfTheta_rad = np.radians(HalfTheta_deg)

    #------------------------------------------------------------------------
    # Path construction
    #------------------------------------------------------------------------
    # S-bend type — Euler for tangent-matched low-loss, circular otherwise
    if Euler == 1:
        sbend_in  = gf.path.euler(radius=BendRadius, angle=+HalfTheta_deg, p=1.0)
        sbend_out = gf.path.euler(radius=BendRadius, angle=+HalfTheta_deg, p=1.0)
    else:
        sbend_in  = gf.path.arc(radius=BendRadius, angle=+HalfTheta_deg)
        sbend_out = gf.path.arc(radius=BendRadius, angle=+HalfTheta_deg)

    # Build path: lead → S-bend → concentric arc (always circular) → S-bend → lead
    p = gf.path.straight(length=InLengthX)
    p += sbend_in
    p += gf.path.arc(radius=ArcRadius, angle=-ThetaC)
    p += sbend_out
    p += gf.path.straight(length=InLengthX)

    #------------------------------------------------------------------------
    # Move path so that arc center-of-curvature sits at origin, then extrude
    #------------------------------------------------------------------------

    # Query actual path endpoint at start of big arc (works for circular and Euler)
    p_pre = gf.path.straight(length=InLengthX)
    p_pre += sbend_in
    x2, y2 = p_pre.points[-1]

    # CoC is perpendicular-right of tangent at (x2, y2)
    coc_x = x2 + ArcRadius * np.sin(HalfTheta_rad)
    coc_y = y2 - ArcRadius * np.cos(HalfTheta_rad)

    # Extrude and place so arc CoC sits at origin
    bus = gf.path.extrude(p, layer=Layer, width=WgWidth)

    c = gf.Component()
    bus_ref = c << bus
    bus_ref.dmove((-coc_x, -coc_y))

    c.add_port(name="o1", port=bus_ref.ports["o1"])
    c.add_port(name="o2", port=bus_ref.ports["o2"])
    
    c.info["DX"] = abs(c.xmax - c.xmin)
    c.info["DY"] = abs(c.ymax - c.ymin)
    
    return c

if __name__ == "__main__":
    c = Pulley()
    c.show()
    c2 = Pulley(Euler=1)
    c2.show()