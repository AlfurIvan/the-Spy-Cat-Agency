from rest_framework import serializers
from .models import SpyCat, Mission, Target


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']
        read_only_fields = ['name', 'breed']

from rest_framework import serializers
from .models import SpyCat, Mission, Target


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']
        read_only_fields = ['id']

    def validate(self, attrs):
        if self.instance and self.instance.is_completed:
            if 'notes' in attrs and attrs['notes'] != self.instance.notes:
                raise serializers.ValidationError("Cannot update notes for a completed target.")
        return attrs


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat_id = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), source='cat', allow_null=True, required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat_id', 'is_completed', 'targets']
        read_only_fields = ['id', 'is_completed']

    def create(self, validated_data):
        print('\n\n\n\\n\n\nBUUULLLLLSHHHIIIIIIT\n\n\n\n\n\n')
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    # def update(self, instance, validated_data):
    #     if instance.is_completed:
    #         raise serializers.ValidationError("Cannot update a completed mission.")
    #     targets_data = validated_data.pop('targets', [])
    #     instance.cat = validated_data.get('cat', instance.cat)
    #     instance.save()
    #     # Update or create targets
    #     for target_data in targets_data:
    #         target_id = target_data.get('id')
    #         if target_id:
    #             target = Target.objects.get(id=target_id, mission=instance)
    #             for attr, value in target_data.items():
    #                 setattr(target, attr, value)
    #             target.save()
    #         else:
    #             Target.objects.create(mission=instance, **target_data)
    #     return instance

class MissionAssignSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField()

    class Meta:
        fields = ['mission_id']
