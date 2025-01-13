from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import SpyCat, Mission, Target


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']

class TargetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']
        read_only_fields = ['id']

    def validate(self, attrs):
        if self.instance and self.instance.is_completed:
            if 'notes' in attrs and attrs['notes'] != self.instance.notes:
                raise exceptions.ValidationError("Cannot update notes for a completed target.")
        return attrs


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_completed', 'targets']
        read_only_fields = ['id', 'is_completed']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance: Mission, validated_data):
        targets_data = validated_data.pop('targets')
        targets = instance.targets.all()
        for target_data in targets_data:

            target = targets.filter(pk=target_data.get('id'), mission=instance).first()
            if not target:
                raise ValidationError({'detail':'Target not found'})
            else:
                target.notes = target_data.get('notes', target.notes)
                target.is_completed = target_data.get('is_completed', target.is_completed)
                target.save()

        instance.refresh_from_db()
        if all(target.is_completed for target in instance.targets.all()):

            instance.is_completed = True
            instance.cat = None
            instance.save()

        return instance


class MissionAssignSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField()

    class Meta:
        fields = ['mission_id']


class CatAssignSerializer(serializers.Serializer):
    cat_id = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), source='cat', required=True)

    class Meta:
        fields = ['cat_id']
