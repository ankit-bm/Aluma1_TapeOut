import gdsfactory as gf
import numpy as np
from gdsfactory.path import smooth

@gf.cell
def ModulatedRing(Radius=100,
                WgWidth=10,
                A=[2.5],
                M=[5],
                NPoints= 360*100,
                Layer = (1, 0)
):

    theta = np.linspace(0, 2*np.pi, NPoints)
    R_inner_base   = Radius - WgWidth
    R_outer_const  = Radius 

    A_list = np.atleast_1d(A)
    M_list = np.atleast_1d(M)

    # sum of cosines
    modulation = np.zeros_like(theta)
    for i, (Ai, Mi) in enumerate(zip(A_list, M_list)):

        if Mi == 0:
            modulation += Ai # No modulation for M=0
        else:

            modulation += Ai * np.cos(2*Mi * theta + (2*np.pi/len(M_list))*i)  # Normalized modulation

    R_inner       = R_inner_base - modulation

    x_inner = R_inner * np.cos(theta)
    y_inner = R_inner * np.sin(theta)
    x_outer = R_outer_const * np.cos(theta[::-1])
    y_outer = R_outer_const * np.sin(theta[::-1])

    x_poly = np.concatenate([x_inner, x_outer])
    y_poly = np.concatenate([y_inner, y_outer])

    Points = np.stack([x_poly, y_poly], axis=1)

    MRing = gf.Component()
    MRing.add_polygon(Points, layer=Layer)

    return MRing