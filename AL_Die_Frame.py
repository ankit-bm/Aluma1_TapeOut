import gdsfactory as gf
gf.gpdk.PDK.activate()

###############################################################################
# Parameters
###############################################################################
@gf.cell
def AL_Die_Frame(
    RetLengthX = 21000,
    RetLengthY = 21000,
    DieFractions = [1.2, 1.2, 1.2, 0.7, 0.7],
    DiceLaneWidth = 100,
    StreetWidth   = 10,
    FrameLayer = (1,0),
):

    Die_Frame = gf.Component()

    NDies = len(DieFractions)

    UsableWidth = RetLengthX - (NDies+1)*DiceLaneWidth
    TotalFraction = sum(DieFractions)
    DieWidths = [UsableWidth * Fraction / TotalFraction for Fraction in DieFractions]

    DieLengthY = (RetLengthX - 2*StreetWidth)

    Die_Frame.info["DieWidths"] = DieWidths
    Die_Frame.info["DieLengthY"] = DieLengthY

    # ------------------------------------------------------------------
    # Die Outline
    # ------------------------------------------------------------------

    Frame = Die_Frame << gf.components.die(
        size=(RetLengthX, RetLengthY),
        street_width=DiceLaneWidth,
        street_length=DiceLaneWidth,
        die_name="",
        text_size=500,
        text_location="SW",
        layer=FrameLayer,
        bbox_layer=None,
    )

    Frame.move((RetLengthX/2, RetLengthY/2))

    # ------------------------------------------------------------------
    # Dicing Lanes within Reticle
    # ------------------------------------------------------------------

    BottomEdge = DiceLaneWidth
    TopEdge    = RetLengthY - DiceLaneWidth

    XCursor = DiceLaneWidth + DieWidths[0]
    for j in range(0, NDies-1):

        LeftEdge  = XCursor
        RightEdge = LeftEdge + DiceLaneWidth

        Die_Frame.add_polygon([
            (LeftEdge,  BottomEdge),
            (RightEdge, BottomEdge),
            (RightEdge, TopEdge),
            (LeftEdge,  TopEdge),
            ], layer=FrameLayer)

        XCursor += DiceLaneWidth + DieWidths[j+1]

    return Die_Frame

# test_AL_Die_Frame.py

if __name__ == "__main__":
    c = AL_Die_Frame()
    print("DieWidths:", c.info["DieWidths"])
    print("DieLengthY:", c.info["DieLengthY"])
    c.write_gds("AL_Die_Frame_test.gds")
    print("Written AL_Die_Frame_test.gds")
    c.show()
    c.plot()