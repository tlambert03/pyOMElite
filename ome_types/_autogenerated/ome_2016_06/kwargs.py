from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from datetime import datetime

    import ome_types.model as ome


class RefDict(TypedDict):
    id: str


class AffineTransformDict(TypedDict, total=False):
    a00: float
    a01: float
    a02: float
    a10: float
    a11: float
    a12: float


class AnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None


AnnotationRefDict: TypeAlias = RefDict


class ArcDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    power: float | None
    power_unit: ome.UnitsPower | str
    serial_number: str | None
    type: ome.Arc_Type | str | None


class BinDataDict(TypedDict, total=False):
    big_endian: bool
    compression: ome.BinData_Compression | str
    length: int
    value: bytes


class BinaryFileDict(TypedDict, total=False):
    bin_data: BinDataDict | None
    external: ExternalDict | None
    file_name: str
    mime_type: str | None
    size: int


class BooleanAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: bool


class ChannelDict(TypedDict, total=False):
    acquisition_mode: ome.Channel_AcquisitionMode | str | None
    annotation_refs: list[AnnotationRefDict]
    color: ome.Color | str
    contrast_method: ome.Channel_ContrastMethod | str | None
    detector_settings: DetectorSettingsDict | None
    emission_wavelength: float | None
    emission_wavelength_unit: ome.UnitsLength | str
    excitation_wavelength: float | None
    excitation_wavelength_unit: ome.UnitsLength | str
    filter_set_ref: FilterSetRefDict | None
    fluor: str | None
    id: str
    illumination_type: ome.Channel_IlluminationType | str | None
    light_path: LightPathDict | None
    light_source_settings: LightSourceSettingsDict | None
    name: str | None
    nd_filter: float | None
    pinhole_size: float | None
    pinhole_size_unit: ome.UnitsLength | str
    pockel_cell_setting: int | None
    samples_per_pixel: int | None


ChannelRefDict: TypeAlias = RefDict


class CommentAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: str


class DatasetDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    experimenter_group_ref: ExperimenterGroupRefDict | None
    experimenter_ref: ExperimenterRefDict | None
    id: str
    image_refs: list[ImageRefDict]
    name: str | None


DatasetRefDict: TypeAlias = RefDict


class DetectorDict(TypedDict, total=False):
    amplification_gain: float | None
    annotation_refs: list[AnnotationRefDict]
    gain: float | None
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    offset: float | None
    serial_number: str | None
    type: ome.Detector_Type | str | None
    voltage: float | None
    voltage_unit: ome.UnitsElectricPotential | str
    zoom: float | None


class DetectorSettingsDict(TypedDict, total=False):
    binning: ome.Binning | str | None
    gain: float | None
    id: str
    integration: int | None
    offset: float | None
    read_out_rate: float | None
    read_out_rate_unit: ome.UnitsFrequency | str
    voltage: float | None
    voltage_unit: ome.UnitsElectricPotential | str
    zoom: float | None


class DichroicDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None


DichroicRefDict: TypeAlias = RefDict


class DoubleAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: float


class EllipseDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    radius_x: float
    radius_y: float
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    x: float
    y: float


class ExperimentDict(TypedDict, total=False):
    description: str | None
    experimenter_ref: ExperimenterRefDict | None
    id: str
    microbeam_manipulations: list[MicrobeamManipulationDict]
    type: list[ome.Experiment_value | str]


ExperimentRefDict: TypeAlias = RefDict


class ExperimenterDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    email: str | None
    first_name: str | None
    id: str
    institution: str | None
    last_name: str | None
    middle_name: str | None
    user_name: str | None


class ExperimenterGroupDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    experimenter_refs: list[ExperimenterRefDict]
    id: str
    leaders: list[LeaderDict]
    name: str | None


ExperimenterGroupRefDict: TypeAlias = RefDict
ExperimenterRefDict: TypeAlias = RefDict


class ExternalDict(TypedDict, total=False):
    compression: ome.External_Compression | str
    href: str
    sha1: bytes


class FilamentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    power: float | None
    power_unit: ome.UnitsPower | str
    serial_number: str | None
    type: ome.Filament_Type | str | None


class FileAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    binary_file: BinaryFileDict
    description: str | None
    id: str
    namespace: str | None


class FilterDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    filter_wheel: str | None
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None
    transmittance_range: TransmittanceRangeDict | None
    type: ome.Filter_Type | str | None


FilterRefDict: TypeAlias = RefDict


class FilterSetDict(TypedDict, total=False):
    dichroic_ref: DichroicRefDict | None
    emission_filters: list[FilterRefDict]
    excitation_filters: list[FilterRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None


FilterSetRefDict: TypeAlias = RefDict


class FolderDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    folder_refs: list[FolderRefDict]
    id: str
    image_refs: list[ImageRefDict]
    name: str | None
    roi_refs: list[ROIRefDict]


FolderRefDict: TypeAlias = RefDict


class GenericExcitationSourceDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    map: MapDict | None
    model: str | None
    power: float | None
    power_unit: ome.UnitsPower | str
    serial_number: str | None


class ImageDict(TypedDict, total=False):
    acquisition_date: datetime | None
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    experiment_ref: ExperimentRefDict | None
    experimenter_group_ref: ExperimenterGroupRefDict | None
    experimenter_ref: ExperimenterRefDict | None
    id: str
    imaging_environment: ImagingEnvironmentDict | None
    instrument_ref: InstrumentRefDict | None
    microbeam_manipulation_refs: list[MicrobeamManipulationRefDict]
    name: str | None
    objective_settings: ObjectiveSettingsDict | None
    pixels: PixelsDict
    roi_refs: list[ROIRefDict]
    stage_label: StageLabelDict | None


ImageRefDict: TypeAlias = RefDict


class ImagingEnvironmentDict(TypedDict, total=False):
    air_pressure: float | None
    air_pressure_unit: ome.UnitsPressure | str
    co2_percent: float | None
    humidity: float | None
    map: MapDict | None
    temperature: float | None
    temperature_unit: ome.UnitsTemperature | str


class InstrumentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    arcs: list[ArcDict]
    detectors: list[DetectorDict]
    dichroics: list[DichroicDict]
    filaments: list[FilamentDict]
    filter_sets: list[FilterSetDict]
    filters: list[FilterDict]
    generic_excitation_sources: list[GenericExcitationSourceDict]
    id: str
    lasers: list[LaserDict]
    light_emitting_diodes: list[ome.LightEmittingDiode | str]
    microscope: MicroscopeDict | None
    objectives: list[ObjectiveDict]


InstrumentRefDict: TypeAlias = RefDict


class LabelDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    x: float
    y: float


class LaserDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    frequency_multiplication: int | None
    id: str
    laser_medium: ome.Laser_LaserMedium | str | None
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    pockel_cell: bool | None
    power: float | None
    power_unit: ome.UnitsPower | str
    pulse: ome.Laser_Pulse | str | None
    pump: PumpDict | None
    repetition_rate: float | None
    repetition_rate_unit: ome.UnitsFrequency | str
    serial_number: str | None
    tuneable: bool | None
    type: ome.Laser_Type | str | None
    wavelength: float | None
    wavelength_unit: ome.UnitsLength | str


class LeaderDict(TypedDict, total=False):
    id: str


class LightPathDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    dichroic_ref: DichroicRefDict | None
    emission_filters: list[FilterRefDict]
    excitation_filters: list[FilterRefDict]


class LightSourceDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    power: float | None
    power_unit: ome.UnitsPower | str
    serial_number: str | None


class LightSourceSettingsDict(TypedDict, total=False):
    attenuation: float | None
    id: str
    wavelength: float | None
    wavelength_unit: ome.UnitsLength | str


class LineDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    marker_end: ome.Marker | str | None
    marker_start: ome.Marker | str | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    x1: float
    x2: float
    y1: float
    y2: float


class LongAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: int


class ManufacturerSpecDict(TypedDict, total=False):
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None


class MapDict(TypedDict, total=False):
    ms: list[ome.Map.M | str]


class MapAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: MapDict


class MaskDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    bin_data: BinDataDict
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    height: float
    id: str
    locked: bool | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    width: float
    x: float
    y: float


class MicrobeamManipulationDict(TypedDict, total=False):
    description: str | None
    experimenter_ref: ExperimenterRefDict
    id: str
    light_source_settings_combinations: list[LightSourceSettingsDict]
    roi_refs: list[ROIRefDict]
    type: list[ome.MicrobeamManipulation_value | str]


MicrobeamManipulationRefDict: TypeAlias = RefDict


class MicroscopeDict(TypedDict, total=False):
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None
    type: ome.Microscope_Type | str | None


class OMEDict(TypedDict, total=False):
    binary_only: ome.OME.BinaryOnly | str | None
    creator: str | None
    datasets: list[DatasetDict]
    experimenter_groups: list[ExperimenterGroupDict]
    experimenters: list[ExperimenterDict]
    experiments: list[ExperimentDict]
    folders: list[FolderDict]
    images: list[ImageDict]
    instruments: list[InstrumentDict]
    plates: list[PlateDict]
    projects: list[ProjectDict]
    rights: RightsDict | None
    rois: list[ROIDict]
    screens: list[ScreenDict]
    structured_annotations: StructuredAnnotationsDict | None
    uuid: str | None


class ObjectiveDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    calibrated_magnification: float | None
    correction: ome.Objective_Correction | str | None
    id: str
    immersion: ome.Objective_Immersion | str | None
    iris: bool | None
    lens_na: float | None
    lot_number: str | None
    manufacturer: str | None
    model: str | None
    nominal_magnification: float | None
    serial_number: str | None
    working_distance: float | None
    working_distance_unit: ome.UnitsLength | str


class ObjectiveSettingsDict(TypedDict, total=False):
    correction_collar: float | None
    id: str
    medium: ome.ObjectiveSettings_Medium | str | None
    refractive_index: float | None


class PixelsDict(TypedDict, total=False):
    big_endian: bool | None
    bin_data_blocks: list[BinDataDict]
    channels: list[ChannelDict]
    dimension_order: ome.Pixels_DimensionOrder | str
    id: str
    interleaved: bool | None
    metadata_only: ome.MetadataOnly | str | None
    physical_size_x: float | None
    physical_size_x_unit: ome.UnitsLength | str
    physical_size_y: float | None
    physical_size_y_unit: ome.UnitsLength | str
    physical_size_z: float | None
    physical_size_z_unit: ome.UnitsLength | str
    planes: list[PlaneDict]
    significant_bits: int | None
    size_c: int
    size_t: int
    size_x: int
    size_y: int
    size_z: int
    tiff_data_blocks: list[TiffDataDict]
    time_increment: float | None
    time_increment_unit: ome.UnitsTime | str
    type: ome.PixelType | str


class PlaneDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    delta_t: float | None
    delta_t_unit: ome.UnitsTime | str
    exposure_time: float | None
    exposure_time_unit: ome.UnitsTime | str
    hash_sha1: bytes | None
    position_x: float | None
    position_x_unit: ome.UnitsLength | str
    position_y: float | None
    position_y_unit: ome.UnitsLength | str
    position_z: float | None
    position_z_unit: ome.UnitsLength | str
    the_c: int
    the_t: int
    the_z: int


class PlateDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    column_naming_convention: ome.NamingConvention | str | None
    columns: int | None
    description: str | None
    external_identifier: str | None
    field_index: int | None
    id: str
    name: str | None
    plate_acquisitions: list[PlateAcquisitionDict]
    row_naming_convention: ome.NamingConvention | str | None
    rows: int | None
    status: str | None
    well_origin_x: float | None
    well_origin_x_unit: ome.UnitsLength | str
    well_origin_y: float | None
    well_origin_y_unit: ome.UnitsLength | str
    wells: list[WellDict]


class PlateAcquisitionDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    end_time: datetime | None
    id: str
    maximum_field_count: int | None
    name: str | None
    start_time: datetime | None
    well_sample_refs: list[WellSampleRefDict]


class PointDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    x: float
    y: float


class PolygonDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    points: str
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None


class PolylineDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    marker_end: ome.Marker | str | None
    marker_start: ome.Marker | str | None
    points: str
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None


class ProjectDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    dataset_refs: list[DatasetRefDict]
    description: str | None
    experimenter_group_ref: ExperimenterGroupRefDict | None
    experimenter_ref: ExperimenterRefDict | None
    id: str
    name: str | None


ProjectRefDict: TypeAlias = RefDict


class PumpDict(TypedDict, total=False):
    id: str


class ROIDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    id: str
    name: str | None
    union: ome.ROI.Union | str


ROIRefDict: TypeAlias = RefDict


class ReagentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    id: str
    name: str | None
    reagent_identifier: str | None


ReagentRefDict: TypeAlias = RefDict


class RectangleDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    height: float
    id: str
    locked: bool | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None
    width: float
    x: float
    y: float


class RightsDict(TypedDict, total=False):
    rights_held: str | None
    rights_holder: str | None


class ScreenDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: str | None
    id: str
    name: str | None
    plate_refs: list[ome.Screen.PlateRef | str]
    protocol_description: str | None
    protocol_identifier: str | None
    reagent_set_description: str | None
    reagent_set_identifier: str | None
    reagents: list[ReagentDict]
    type: str | None


class ShapeDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: ome.Color | str | None
    fill_rule: ome.Shape_FillRule | str | None
    font_family: ome.Shape_FontFamily | str | None
    font_size: int | None
    font_size_unit: ome.UnitsLength | str
    font_style: ome.Shape_FontStyle | str | None
    id: str
    locked: bool | None
    stroke_color: ome.Color | str | None
    stroke_dash_array: str | None
    stroke_width: float | None
    stroke_width_unit: ome.UnitsLength | str
    text: str | None
    the_c: int | None
    the_t: int | None
    the_z: int | None
    transform: AffineTransformDict | None


class StageLabelDict(TypedDict, total=False):
    name: str
    x: float | None
    x_unit: ome.UnitsLength | str
    y: float | None
    y_unit: ome.UnitsLength | str
    z: float | None
    z_unit: ome.UnitsLength | str


class StructuredAnnotationsDict(TypedDict, total=False):
    boolean_annotations: list[BooleanAnnotationDict]
    comment_annotations: list[CommentAnnotationDict]
    double_annotations: list[DoubleAnnotationDict]
    file_annotations: list[FileAnnotationDict]
    list_annotations: list[ome.ListAnnotation | str]
    long_annotations: list[LongAnnotationDict]
    map_annotations: list[MapAnnotationDict]
    tag_annotations: list[TagAnnotationDict]
    term_annotations: list[TermAnnotationDict]
    timestamp_annotations: list[TimestampAnnotationDict]
    xml_annotations: list[XMLAnnotationDict]


class TagAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: str


class TermAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: str


class TiffDataDict(TypedDict, total=False):
    first_c: int
    first_t: int
    first_z: int
    ifd: int
    plane_count: int | None
    uuid: ome.TiffData.UUID | str | None


class TimestampAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: datetime


class TransmittanceRangeDict(TypedDict, total=False):
    cut_in: float | None
    cut_in_tolerance: float | None
    cut_in_tolerance_unit: ome.UnitsLength | str
    cut_in_unit: ome.UnitsLength | str
    cut_out: float | None
    cut_out_tolerance: float | None
    cut_out_tolerance_unit: ome.UnitsLength | str
    cut_out_unit: ome.UnitsLength | str
    transmittance: float | None


class WellDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    color: ome.Color | str
    column: int
    external_description: str | None
    external_identifier: str | None
    id: str
    reagent_ref: ReagentRefDict | None
    row: int
    type: str | None
    well_samples: list[WellSampleDict]


class WellSampleDict(TypedDict, total=False):
    id: str
    image_ref: ImageRefDict | None
    index: int
    position_x: float | None
    position_x_unit: ome.UnitsLength | str
    position_y: float | None
    position_y_unit: ome.UnitsLength | str
    timepoint: datetime | None


WellSampleRefDict: TypeAlias = RefDict


class XMLAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: str | None
    description: str | None
    id: str
    namespace: str | None
    value: ome.XMLAnnotation.Value | str
