from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

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

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        mission = self.get_object()
        if mission.is_completed:
            return Response({"error": "Mission is already completed"}, status=status.HTTP_400_BAD_REQUEST)

        if mission.targets.filter(is_completed=False).exists():
            return Response({"error": "Not all targets are completed"}, status=status.HTTP_400_BAD_REQUEST)

        mission.is_completed = True
        mission.save()

        return Response({"success": "Mission marked as completed"}, status=status.HTTP_200_OK)

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        target = self.get_object()

        if target.is_completed:
            return Response({"error": "Target is already completed"}, status=status.HTTP_400_BAD_REQUEST)

        target.is_completed = True
        target.save()

        return Response({"success": "Target marked as completed"}, status=status.HTTP_200_OK)