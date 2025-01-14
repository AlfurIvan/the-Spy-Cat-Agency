import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Mission, SpyCat
from .serializers import MissionSerializer, SpyCatSerializer, MissionAssignSerializer, CatAssignSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @staticmethod
    def validate_breed(breed):
        """Validate the breed using TheCatAPI."""
        url = f"https://api.thecatapi.com/v1/breeds/search?q={breed}"
        response = requests.get(url, headers={"X-API-KEY": settings.CAT_API_KEY})

        if response.status_code != 200:
            raise ValidationError("Unable to validate breed due to an API error.")

        if not response.json():
            raise ValidationError(f"Breed '{breed}' is not recognized.")

        return response.json()[0]['name']

    def perform_create(self, serializer):
        breed = serializer.validated_data.get('breed')
        validated_breed = self.validate_breed(breed)
        serializer.validated_data['breed'] = validated_breed
        serializer.save()

    def perform_update(self, serializer):
        breed = serializer.validated_data.get('breed')
        if breed:
            validated_breed = self.validate_breed(breed)
            serializer.validated_data['breed'] = validated_breed
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'assign_mission':
            return MissionAssignSerializer
        else:
            return self.serializer_class

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
    queryset = Mission.objects.prefetch_related('targets').all()
    serializer_class = MissionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'assign_cat':
            return CatAssignSerializer
        else:
            return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"detail": "Cannot delete a mission assigned to a cat."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
