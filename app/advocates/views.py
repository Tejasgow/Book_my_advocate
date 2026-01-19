from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import AdvocateProfile
from .serializers import AdvocateProfileSerializer, AdvocateCreateSerializer
from .permissions import IsAdvocate

# ------------------------
# Create Advocate Profile
# ------------------------
class AdvocateCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]
    
    def post(self, request):
        serializer = AdvocateCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            advocate = serializer.save()
            return Response({
                "message": "Advocate profile created successfully ✅",
                "data": AdvocateProfileSerializer(advocate).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------------------------------------
# List Advocates (verified only, optional specialization filter)
# -------------------------------------------------------------
class AdvocateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specialization = request.query_params.get('specialization')
        queryset = AdvocateProfile.objects.filter(verified=True)
        if specialization:
            queryset = queryset.filter(specialization__iexact=specialization.upper())
        serializer = AdvocateProfileSerializer(queryset, many=True)
        return Response({
            "message": "Advocates fetched successfully ✅",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# -----------------------------
# Single Advocate Detail
# -----------------------------
class AdvocateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        advocate = get_object_or_404(AdvocateProfile, pk=pk, verified=True)
        serializer = AdvocateProfileSerializer(advocate)
        return Response({
            "message": "Advocate profile fetched successfully ✅",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

