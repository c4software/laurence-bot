from sqlalchemy import String, TypeDecorator
from sqlalchemy.ext import mutable
import json

class JsonEncodedDict(TypeDecorator):
  """Enables JSON storage by encoding and decoding on the fly."""
  impl = String

  def process_bind_param(self, value, dialect):
    return json.dumps(value)

  def process_result_value(self, value, dialect):
    return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)
