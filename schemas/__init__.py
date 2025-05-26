from flask import current_app
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError, post_dump
from typing import AbstractSet, Any, Iterable, Mapping, Optional, Sequence, Union

marshmallow_obj = Marshmallow()


class NotEmptyString(fields.String):
	def _deserialize(self, value, attr, data, **kwargs):
		value = super()._deserialize(value, attr, data, **kwargs)
		if not value or value.strip() == "":
			raise ValidationError("参数不能为空!")
		return value


class BaseSchema(marshmallow_obj.Schema):
	def dump(self, obj:Any, *, many:Optional[bool] = None):
		result = super().dump(obj, many=many)
		# current_app.logger.info(f"dump => {self.__class__.__name__} {result}")
		return result

	def load(self, data:Union[Mapping[str, Any], Iterable[Mapping[str, Any]]], *, many:Optional[bool] = None, partial:Union[bool, Sequence[str], AbstractSet[str], None] = None, unknown:Union[str, None] = None):
		result = super().load(data, many=many, partial=partial, unknown=unknown)
		# current_app.logger.info(f"load => {self.__class__.__name__} {result}")
		return result

	@post_dump
	def remove_none_fields(self, data, **kwargs):
		# Remove None fields
		return {k: v for k, v in data.items() if v is not None}