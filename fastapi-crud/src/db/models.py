from sqlalchemy import Column, Integer, String

from db.database import Base

# from sqlalchemy.sql.sqltypes import Date, Integer, String


class TBLRoads(Base):
    """from roads_schema.csv

    table object goes into the database

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "roads"
    id = Column(Integer, primary_key=True, index=True)
    DiscrpAgID = Column(String(80))
    # DiscrpAgID = Column(VARCHAR(80))
    # DateUpdate = Column()
    # username = Column(String)
    # email = Column(String)
    # password = Column(String)


# DiscrpAgID,VARCHAR,80,
# DateUpdate,TIMESTAMPTZ,,
# Effective,TIMESTAMPTZ,,
# Expire,TIMESTAMPTZ,,
# RCL_NGUID,VARCHAR,254,PRIMARY KEY UNIQUE NOT NULL
# RCL_COMID,VARCHAR,254,DEFAULT NULL
# AdNumPre_L,VARCHAR,16,
# AdNumPre_R,VARCHAR,16,
# FromAddr_L,INT,,
# ToAddr_L,INT,,
# FromAddr_R,INT,,
# ToAddr_R,INT,,
# Parity_L,VARCHAR,1,
# Parity_R,VARCHAR,1,
# Name,VARCHAR,80,
# St_PreMod,VARCHAR,15,
# St_PreDir,VARCHAR,9,
# St_PreTyp,VARCHAR,50,
# St_PreSep,VARCHAR,20,
# St_Name,VARCHAR,60,
# St_PosTyp,VARCHAR,50,
# St_PosDir,VARCHAR,9,
# St_PosMod,VARCHAR,25,
# St_RtType,INT,,
# St_RtNum,VARCHAR,25,
# MSAGComm_R,VARCHAR,30,
# Country_L,VARCHAR,2,
# Country_R,VARCHAR,2,
# State_L,VARCHAR,2,
# State_R,VARCHAR,2,
# County_L,VARCHAR,40,
# County_R,VARCHAR,40,
# AddCode_L,VARCHAR,6,
# AddCode_R,VARCHAR,6,
# IncMuni_L,VARCHAR,100,
# IncMuni_R,VARCHAR,100,
# UnincCom_L,VARCHAR,100,
# UnincCom_R,VARCHAR,100,
# NbrhdCom_L,VARCHAR,100,
# NbrhdCom_R,VARCHAR,100,
# PostCode_L,VARCHAR,7,
# PostCode_R,VARCHAR,7,
# PostComm_L,VARCHAR,40,
# PostComm_R,VARCHAR,40,
# RoadClass,VARCHAR,15,
# FunClass,INT,,
# OneWay,VARCHAR,2,
# SpeedLimit,INT,,
# Valid_L,VARCHAR,1,
# Valid_R,VARCHAR,1,
# Geometry,"GEOMETRY(MultiLineString,4326)",,
