# from django.db import models


# class ListField(models.TextField):

#     description = "Stores tags in a single database column."

#     __metaclass__ = models.SubfieldBase

#     def __init__(self, delimiter="|", *args, **kwargs):
#         self.delimiter = delimiter
#         super(ListField, self).__init__(*args, **kwargs)

#     def to_python(self, value):
#         # If it's already a list, leave it
#         if isinstance(value, list):
#             return value

#         # Otherwise, split by delimiter
#         return value.split(self.delimiter)

#     def get_prep_value(self, value):
#         return self.delimiter.join(value)

# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([
#     (
#         [ListField],  # Class(es) these apply to
#         [],          # Positional arguments (not used)
#         {            # Keyword argument
#             "delimiter": ["delimiter", {"default": "|"}],
#         },
#     ),
# ], ["^stockhist\.fields\.ListField"])
