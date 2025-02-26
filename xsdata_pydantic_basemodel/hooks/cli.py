from xsdata.codegen.writer import CodeWriter

from xsdata_pydantic_basemodel.generator import PydanticBaseGenerator

CodeWriter.register_generator("pydantic-basemodel", PydanticBaseGenerator)
