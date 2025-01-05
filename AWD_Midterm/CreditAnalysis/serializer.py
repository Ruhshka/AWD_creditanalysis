from rest_framework import serializers
from .models import CreditAnalysis

#Convert and transform all the data into JSON
class CreditAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAnalysis
        fields = '__all__'