"""Aeluma 1 Layout

"""

import gdsfactory as gf
gf.CONF.max_cellname_length = 35
gf.gpdk.PDK.activate()

import numpy as np
import pandas as pd

from AL_Die_Frame import AL_Die_Frame
from AL_Layers import AL_Layers

# 2D Devices
# from AFQH_Device import AFQH_Device
# from AQH_CB_Device import AQH_CB_Device
# from AQH_Device_Rot import AQH_Device_Rot

# from OneD_Device import OneD_Device

# from ADF_RIO import ADF_RIO
# from APF_Pulley import APF_Pulley
# from APF_Modulated import APF_Modulated

# from DirCoupler_Device import DirCoupler_Device


###########################################################################################
# Device Configurations
###########################################################################################
# ConfigFile        = "Device_Config.xlsx"
# ADF_25_Config     = pd.read_excel(ConfigFile, sheet_name="ADF_25")


@gf.cell
def TOP():

    Top = gf.Component()

###########################################################################################
# Die Outline and Frame
###########################################################################################
    RetLengthX    = 21000
    RetLengthY    = 21000
    NDies         = 4
    DiceLaneWidth = 100
    StreetWidth   = 10 

    AL_Die_Frame_Ref = Top << AL_Die_Frame(RetLengthX=RetLengthX, RetLengthY=RetLengthY, NDies=NDies, DiceLaneWidth = DiceLaneWidth, StreetWidth=StreetWidth, CHSLayer=AL_Layers.CHS, CSLLayer=AL_Layers.CSL)

    print(AL_Die_Frame_Ref.info)
    # DieLengthX = AL_Die_Frame_Ref.info["DieLengthX"]
    # DieLengthY = AL_Die_Frame_Ref.info["DieLengthY"]

    # TaperLength = 400
    
    # TotLengthY  = DieLengthY - 2*TaperLength + 2*(StreetWidth+5)

    # StartY0     = TaperLength - 5
    # StartY      = StartY0
    
###########################################################################################
# Common Parameters for 2D and 1D Devices
###########################################################################################

    BendRadius   = 25
    WgWidth      = 1.2
    FArrayGap    = 30

    LengthSR     = 12.0
    eta          = 0.110



###########################################################################################
# return
###########################################################################################
    
    return Top

###########################################################################################
# Script entry-point
###########################################################################################
if __name__ == "__main__":
    c = TOP()
    c.write_gds("AL_Test_0.gds")
    print("Written gds")
    c.show()