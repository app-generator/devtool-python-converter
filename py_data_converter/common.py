# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

django_fields = {
    'boolean': 'models.BooleanField()\n',
    'integer': 'models.IntegerField()\n',
    'string': "models.OneToOneField()\n",
    'number': 'models.FloatField()\n',
    'UUIDField': "model.UUIDField()\n",
    'URLField': "model.URLField()\n",
    'TimeField': "model.TimeField()\n",
    'TextField': "model.TextField()\n",
    'SmallIntegerField': "model.SmallIntegerField()\n",
    'SmallAutoField': "model.SmallAutoField()\n",
    'SlugField': "model.SlugField()\n",
    'PositiveSmallIntegerField': "model.PositiveSmallIntegerField()\n",
    'PositiveIntegerField': "model.PositiveIntegerField()\n",
    'PositiveBigIntegerField': "model.PositiveBigIntegerField()\n",
    'JSONField': "model.JSONField()\n",
    'IntegerField': "model.IntegerField()\n",
    'ImageField': "model.ImageField()\n",
    'GenericIPAddressField': "model.GenericIPAddressField()\n",
    'FloatField': "model.FloatField()\n",
    'FilePathField': "model.FilePathField()\n",
    'FileField': "model.FileField()\n",
    'EmailField': "model.EmailField()\n",
    'DurationField': "model.DurationField()\n",
    'DecimalField': "model.DecimalField()\n",
    'DateTimeField': "model.DateTimeField()\n",
    'DateField': "model.DateField()\n",
    'CharField': "model.CharField()\n",
    'BooleanField': "model.BooleanField()\n",
    'BinaryField': "model.BinaryField()\n",
    'BigIntegerField': "model.BigIntegerField()\n",
    'BigAutoField': "model.BigAutoField()\n",
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

}
