from typing import TYPE_CHECKING, List, Union, cast

if TYPE_CHECKING:
    from ome_types.model.ome_2016_06 import (
        Arc,
        Filament,
        GenericExcitationSource,
        Instrument,
        Laser,
        LightEmittingDiode,
    )

    LightSource = Union[
        GenericExcitationSource, LightEmittingDiode, Filament, Arc, Laser
    ]


class InstrumentMixin:
    @property
    def light_source_group(self) -> List["LightSource"]:
        slf = cast("Instrument", self)
        return [
            *slf.arcs,
            *slf.filaments,
            *slf.generic_excitation_sources,
            *slf.lasers,
            *slf.light_emitting_diodes,
        ]
