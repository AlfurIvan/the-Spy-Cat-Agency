from rest_framework import serializers
from .models import SpyCat, Mission, Target


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']
        read_only_fields = ['id', 'name', 'breed']


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']

    def validate(self, data):
        # Prevent updating notes for completed targets
        if self.instance and self.instance.is_completed and 'notes' in data:
            raise serializers.ValidationError("Cannot update notes for a completed target.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_completed', 'targets']
        read_only_fields = ['id', 'is_completed']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets', [])
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data[:3]:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        # Update Mission fields
        instance.cat = validated_data.get('cat', instance.cat)
        instance.save()

        # Handle nested targets
        targets_data = validated_data.pop('targets', [])
        existing_targets = instance.targets.all()

        for target_data in targets_data:
            target = existing_targets.filter(name=target_data.get('name')).first()
            print(target)
            if target:
                data = TargetSerializer(instance=target, data=target_data)
                data.is_valid(raise_exception=True)
                data.save()

        if all(target.is_completed for target in instance.targets.all()):
            instance.is_completed = True
            instance.save()

        return instance

class MissionAssignSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField()

    class Meta:
        fields = ['mission_id']
