from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Objective_Correction(Enum):
    UV = "UV"
    PLAN_APO = "PlanApo"
    PLAN_FLUOR = "PlanFluor"
    SUPER_FLUOR = "SuperFluor"
    VIOLET_CORRECTED = "VioletCorrected"
    ACHRO = "Achro"
    ACHROMAT = "Achromat"
    FLUOR = "Fluor"
    FL = "Fl"
    FLUAR = "Fluar"
    NEOFLUAR = "Neofluar"
    FLUOTAR = "Fluotar"
    APO = "Apo"
    PLAN_NEOFLUAR = "PlanNeofluar"
    OTHER = "Other"
