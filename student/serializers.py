
from rest_framework import serializers

from student.models import info


class Studentser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=info
        fields=['Email','fullname']