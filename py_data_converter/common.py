# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

django_fields = {
    'boolean': 'models.BooleanField()\n',
    'integer': 'models.IntegerField()\n',
    'string': "models.CharField()\n",
    'number': 'models.FloatField()\n',
    'UUIDField': "models.UUIDField()\n",
    'URLField': "models.URLField()\n",
    'TimeField': "models.TimeField()\n",
    'TextField': "models.TextField()\n",
    'SmallIntegerField': "models.SmallIntegerField()\n",
    'SmallAutoField': "models.SmallAutoField()\n",
    'SlugField': "models.SlugField()\n",
    'PositiveSmallIntegerField': "models.PositiveSmallIntegerField()\n",
    'PositiveIntegerField': "models.PositiveIntegerField()\n",
    'PositiveBigIntegerField': "models.PositiveBigIntegerField()\n",
    'JSONField': "models.JSONField()\n",
    'IntegerField': "models.IntegerField()\n",
    'ImageField': "models.ImageField()\n",
    'GenericIPAddressField': "models.GenericIPAddressField()\n",
    'FloatField': "models.FloatField()\n",
    'FilePathField': "models.FilePathField()\n",
    'FileField': "models.FileField()\n",
    'EmailField': "models.EmailField()\n",
    'DurationField': "models.DurationField()\n",
    'DecimalField': "models.DecimalField()\n",
    'DateTimeField': "models.DateTimeField()\n",
    'DateField': "models.DateField()\n",
    'CharField': "models.CharField()\n",
    'BooleanField': "models.BooleanField()\n",
    'BinaryField': "models.BinaryField()\n",
    'BigIntegerField': "models.BigIntegerField()\n",
    'BigAutoField': "models.BigAutoField()\n",
}

flask_fields = {
    'boolean': 'db.Column(db.Boolean)\n',
    'integer': 'db.Column(db.Integer)\n',
    'string': "db.Column(db.String())\n",
    'number': 'db.Column(db.Float)\n',
    'Text': "db.Column(db.Text)\n",
    'DateTime': "db.Column(db.DateTime)\n",
    'Boolean': "db.Column(db.Boolean)\n",
    'PickleType': "db.Column(db.PickleType)\n",
    'LargeBinary': "db.Column(db.LargeBinary)\n",
    'Integer': "db.Column(db.Integer)\n",
    'Float': "db.Column(db.Float)\n",
    'String': "db.Column(db.String())\n",

    # ForeignKey
}


def get_django_model(model_dict):
    codes = ""
    for attribute_name in model_dict:
        if attribute_name.lower() == 'id':
            continue
        codes = codes + f"\t{attribute_name} = "
        attribute = model_dict[attribute_name]
        attribute_type = attribute['type']
        if attribute_type == 'OneToOneField':
            codes = codes + f"models.OneToOneField({attribute_type}_ID)\n"
        elif attribute_type == 'ManyToManyField':
            codes = codes + f"models.ManyToManyField({attribute_type}_ID)\n"
        elif attribute_type == 'ForeignKey':
            codes = codes + f"models.ForeignKey({attribute_type}_ID)\n"
        elif attribute_type in django_fields:
            codes = codes + django_fields[attribute_type]
        else:
            codes = codes + f"models.ForeignKey({attribute_type})\n"
    return codes


def get_flask_model(model_dict):
    codes = ""
    for attribute_name in model_dict:
        if attribute_name.lower() == 'id':
            continue
        codes = codes + f"\t{attribute_name} = "
        attribute = model_dict[attribute_name]
        attribute_type = attribute['type']
        if attribute_type in flask_fields:
            codes = codes + flask_fields[attribute_type]
        else:
            # foreignkey
            codes = codes + f"db.column(db.Integer, db.ForeignKey({attribute_type}.ID))\n"

    return codes
