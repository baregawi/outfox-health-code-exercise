from dataclasses import dataclass

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase):
    pass

class Provider(MappedAsDataclass, Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_ccn = Column(Integer, index=True)
    provider_org_name = Column(String, index=True)
    city = Column(String)
    street_address = Column(String)
    state_fips = Column(String)
    zipcode = Column(String)
    state_abbr = Column(String)
    ruca = Column(String)
    ruca_description = Column(String)
    drg_cd = Column(String)
    drg_description = Column(String)
    total_discharges = Column(Integer)
    avg_submited_cvrd_charge = Column(Float)
    avg_total_payment_amount = Column(Float)
    avg_mdcr_payment_amt = Column(Float)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
