import gdsfactory as gf

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
    CHSLayer = (100,0),
    CSLLayer = (102,0)  
):
    
    Die_Frame = gf.Component()
    
    NDies = len(DieFractions)   # derive so they can't disagree

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
        size=(RetLengthX, RetLengthY),  # Size of the die.
        street_width=DiceLaneWidth,  # Width of corner marks for die-sawing.
        street_length=DiceLaneWidth,  # Length of corner marks for die-sawing.
        die_name="",  # Label text.
        text_size=500,  # Label text size.
        text_location="SW",  # Label text compass location e.g. 'S', 'SE', 'SW'
        layer=(2, 0),
        bbox_layer=(3, 0),
        )
    
    Frame.move((RetLengthX/2, RetLengthY/2))
    
    # ------------------------------------------------------------------
    # Dicing Lanes within Reticle
    # ------------------------------------------------------------------

    BottomEdge = DiceLaneWidth
    TopEdge    = RetLengthY - DiceLaneWidth

    XCursor = DiceLaneWidth + DieWidths[0]      # right edge of die 0 = start of first lane
    for j in range(0, NDies-1):

        LeftEdge  = XCursor
        RightEdge = LeftEdge + DiceLaneWidth

        Die_Frame.add_polygon([
            (LeftEdge,  BottomEdge),
            (RightEdge, BottomEdge),
            (RightEdge, TopEdge),
            (LeftEdge,  TopEdge),
            ], layer=(1,0))

        XCursor += DiceLaneWidth + DieWidths[j+1]   # advance past lane + next die
        
    # ------------------------------------------------------------------
    # Deep Etch Blocks
    # ------------------------------------------------------------------

    BottomEdge = DiceLaneWidth + StreetWidth
    TopEdge    = RetLengthY - (DiceLaneWidth + StreetWidth)

    XCursor = DiceLaneWidth                      # left lane before die 0
    for j in range(0, NDies):

        LeftEdge  = XCursor + StreetWidth
        RightEdge = LeftEdge + (DieWidths[j] - 2*StreetWidth)

        Die_Frame.add_polygon([
            (LeftEdge,  BottomEdge),
            (RightEdge, BottomEdge),
            (RightEdge, TopEdge),
            (LeftEdge,  TopEdge),
            ], layer=(5,0))

        XCursor += DieWidths[j] + DiceLaneWidth     # advance past this die + lane
                
    return Die_Frame
