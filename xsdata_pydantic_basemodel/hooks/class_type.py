from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic_basemodel.compat import PydanticBaseModel

class_types.register("pydantic-basemodel", PydanticBaseModel())
