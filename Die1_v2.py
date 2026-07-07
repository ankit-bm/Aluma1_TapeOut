# Die1_v2.py
import gdsfactory as gf
import pandas as pd
import os

from AL_Layers import AL_Layers
from SurpentineLossWg import SurpentineLossWg
from Single_Ring_Block_EC import Single_Ring_Block_EC

gf.gpdk.PDK.activate()
gf.CONF.max_cellname_length = 35

ConfigFile = "Device_Config_Rings.xlsx"

@gf.cell
def Die1(DieWidth = 4488, DieHeight = 20780, TaperLength = 400, Layer = AL_Layers.CHS,):

    D      = gf.Component()
    
    StartX = 0
    StartY = 80
    FAGap  = 25
    
    Debug = True
    DebugFrame = True
    
    TotLengthX_EC = DieWidth - 2*TaperLength + 10

    if DebugFrame:
        die_outline = D << gf.components.rectangle(size=(DieWidth, DieHeight), layer=Layer)
        
    EC_RowStart = 0
    EC_RowEnd = 3
    MaxY = DieHeight - 80

    #---------------------------------------------------------------------------
    # EC Ring Blocks
    #---------------------------------------------------------------------------

    BlockParams = dict(
        ConfigFile   = ConfigFile,
        InLengthX0   = 500,
        TotLengthX   = TotLengthX_EC,
        FAGap        = FAGap,
        BendRadiusIO = 15,
        BufLength    = 30,
        OffsetX_APF  = {"15": 40, "20": 40, "30": 40, "40": 40},
        OffsetY_APF  = {"15": 40, "20": 70, "30": 70, "40": 90},
        OffsetX_APFP = {"15": 40, "20": 40, "30": 40, "40": 40},
        OffsetY_APFP = {"15": 40, "20": 80, "30": 80, "40": 80},
        OffsetX_ADF  = {"15": 80, "20": 60, "30": 60, "40": 11},
        OffsetY_ADF  = {"15": 50, "20": 100, "30": 85, "40": 125},
        Layer        = AL_Layers.X1P,
        NPerRowAPF   = {"15": 10, "20": 8,  "30": 6,  "40": 5},
        NPerRowAPFP  = {"15": 8,  "20": 6,  "30": 5,  "40": 4},
        NPerRowADF   = {"15": 6,  "20": 5,  "30": 4,  "40": 3},
    )

    EC_Config_Blocks = pd.read_excel(ConfigFile, sheet_name="ECParams")
    print(EC_Config_Blocks)
    print(EC_Config_Blocks.columns.tolist())

    EC_Config_Blocks = EC_Config_Blocks.iloc[EC_RowStart:EC_RowEnd]

    BlockGapY = 50
    NextY     = StartY

    NextBlockNo = None

    for j, row in EC_Config_Blocks.iterrows():
        BlockNo  = int(row["BlockNo"])
        ECParams = dict(
            WidthStart = float(row["WidthStart"]),
            TaperType  = int(row["Type"]),
            MarkerOn   = True,
        )

        RadiusVec = (15, 20, 30, 40)
        if BlockNo == 3:
            RadiusVec = (15,20)          # only radius-15,20 row for this block

        Path = f"EC_RingBlock_B{BlockNo}.gds"

        if not Debug and os.path.exists(Path):
            print(f"B{BlockNo} loaded from saved gds")
            Block = gf.import_gds(Path)
        else:
            print(f"B{BlockNo} computing...")
            Block = Single_Ring_Block_EC(ECParams=ECParams, BlockID=f"B{BlockNo}", RadiusVec=RadiusVec, **BlockParams)
            Block.write_gds(Path)

        BlockH = Block.ymax - Block.ymin

        if NextY + BlockH > MaxY:
            NextBlockNo = BlockNo
            break

        B = D << Block
        B.xmin = StartX
        B.ymin = NextY
        NextY  = B.ymax + BlockGapY

    if NextBlockNo is not None:
        print(f"Die1 stopped at height {NextY}. Start Die2 from BlockNo = {NextBlockNo}")
    elif EC_RowEnd == 3:
        print("Die1 has Block 3 (radius=15,20 only). Die2 should add Block 3 with RadiusVec=(30,40)")
        
    #------------------------------
    # Loss Characterization Wg
    #------------------------------

    LossWgParams = [
        dict(TaperType=1, MarkerOn=True),
        dict(TaperType=2, MarkerOn=True),
        dict(TaperType=3, MarkerOn=True),
    ]

    NCurveVec   = [(0,1), (2,1),(4,1)]  # (NCurves, NRepeat)
    LossWgGapY  = 25
    WgWidthLoss = 0.6
    LossInLengthX = TotLengthX_EC - 10
    MaxY        = DieHeight - 100

    LossNextY = NextY + BlockGapY - 100

    for ECParams in LossWgParams:
        for N, NRepeat in NCurveVec:
            for _ in range(NRepeat):
                if LossNextY >= MaxY:
                    break
                LossLength = (N + 1) * LossInLengthX
                LW = D << SurpentineLossWg(
                    WgWidth      = WgWidthLoss,
                    InLengthX    = LossInLengthX,
                    BendRadiusIO = 15,
                    NCurves      = N,
                    TaperOn      = True,
                    Euler        = 0,
                    LabelX       = 0,
                    LabelY       = 8,
                    Layer        = AL_Layers.X1P,
                    ECParams     = dict(Length=400, **ECParams),
                    DeviceID     = f"L{LossLength}T{ECParams['TaperType']}",
                )
                LW.xmin   = StartX
                LW.ymin   = LossNextY
                LossNextY = LW.ymax + LossWgGapY

    NextY = LossNextY


    #------------------------------
    # Return
    #------------------------------

    return D

if __name__ == "__main__":
    c = Die1()
    c.write_gds("Die1_test6.gds")
    print("Written Die1_test6.gds")
    c.show()
    c.plot()