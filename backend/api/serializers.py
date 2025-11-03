from rest_framework import serializers
from .models import Match, Delivery

#Integrate serializers later
#Demo serializers
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
