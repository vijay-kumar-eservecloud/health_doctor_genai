# database/models.py
from sqlalchemy import Column, Integer, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HealthStatic(Base):
    __tablename__ = "health_static"

    Patient_Number = Column(BigInteger, primary_key=True, index=True)
    Blood_Pressure_Abnormality = Column(Integer)
    Level_of_Hemoglobin = Column(Float)
    Genetic_Pedigree_Coefficient = Column(Float)
    Age = Column(Integer)
    BMI = Column(Float)
    Sex = Column(Integer)
    Pregnancy = Column(Integer)
    Smoking = Column(Integer)
    salt_content_in_the_diet = Column(Float)
    alcohol_consumption_per_day = Column(Float)
    Level_of_Stress = Column(Integer)
    Chronic_kidney_disease = Column(Integer)
    Adrenal_and_thyroid_disorders = Column(Integer)


class StepsDaily(Base):
    __tablename__ = "steps_daily"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    Patient_Number = Column(BigInteger, ForeignKey("health_static.Patient_Number", ondelete="CASCADE"), index=True)
    Day_Number = Column(Integer)
    Physical_activity = Column(Integer)
