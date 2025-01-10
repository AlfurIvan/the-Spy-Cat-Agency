from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'mission', 'name', 'country', 'notes', 'is_completed']

    def validate_notes(self, value):
        # Ensure notes cannot be updated if the target is completed
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Cannot update notes on a completed target.")
        return value

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_completed', 'targets']
