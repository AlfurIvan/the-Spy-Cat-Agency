import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Mission, SpyCat
from .serializers import MissionSerializer, SpyCatSerializer, MissionAssignSerializer, TargetSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer
    allowed_methods = ('get', 'post', 'patch', 'delete')

    def create(self, request, *args, **kwargs):
        breed = request.data.get('breed')
        url = f"https://api.thecatapi.com/v1/breeds/search?q={breed}"
        response = requests.get(url, headers={"X-API-KEY": settings.CAT_API_KEY})

        if response.status_code != 200:
            raise ValidationError("Unable to validate breed due to an API error.")

        if not response.json():
            raise ValidationError(f"Breed '{breed}' is not recognized.")

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'assign_mission':
            return MissionAssignSerializer
        else:
            return SpyCatSerializer

    @action(detail=True, methods=['post'])
    def assign_mission(self, request, pk=None):
        cat = self.get_object()
        mission_id = request.data.get("mission_id")

        try:
            mission = Mission.objects.get(id=mission_id)
        except Mission.DoesNotExist:
            return Response({"error": "Mission not found"}, status=status.HTTP_404_NOT_FOUND)

        if mission.cat is not None:
            return Response({"error": "Mission already assigned to another cat"}, status=status.HTTP_400_BAD_REQUEST)

        cat.mission = mission
        cat.save()
        mission.cat = cat
        mission.save()

        return Response({"success": "Mission assigned successfully"}, status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.prefetch_related('targets').all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"detail": "Cannot delete a mission assigned to a cat."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        if mission.is_completed:
            return Response({"detail": "Cannot assign a cat to a completed mission."}, status=status.HTTP_400_BAD_REQUEST)
        cat_id = request.data.get('cat_id')
        if not cat_id:
            return Response({"detail": "Cat ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        mission.cat_id = cat_id
        mission.save()
        return Response(self.get_serializer(mission).data)


    def update(self, request, *args, **kwargs):
        mission = self.get_object()
        targets_data = request.data.get('targets', [])

        # Update or validate targets
        for target_data in targets_data:
            target_name = target_data.get("name")
            target_instance = mission.targets.filter(name=target_name).first()
            print("WTFFFFFFFFFFFFF -0")

            if target_instance:
                # Update the existing target
                print("WTFFFFFFFFFFFFF")
                target_serializer = TargetSerializer(target_instance, data=target_data, partial=True)
                print("WTFFFFFFFFFFFFF 2")
                target_serializer.is_valid(raise_exception=True)
                print("WTFFFFFFFFFFFFF 3")
                target_serializer.save()
            else:
                # Handle creation or raise an error
                raise ValidationError(f"Target with name '{target_name}' does not exist in this mission.")

        # Update mission fields
        serializer = self.get_serializer(mission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.select_related('mission').all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        if target.mission.is_completed:
            return Response({"detail": "Cannot update a target in a completed mission."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        target = self.get_object()
        if target.is_completed:
            return Response({"detail": "Target is already completed."}, status=status.HTTP_400_BAD_REQUEST)
        target.is_completed = True
        target.save()

        # Check if all targets in the mission are completed
        mission = target.mission
        if all(t.is_completed for t in mission.targets.all()):
            mission.is_completed = True
            mission.save()

        return Response(self.get_serializer(target).data)