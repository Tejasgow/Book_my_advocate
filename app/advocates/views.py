from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.shortcuts import get_object_or_404
from django.utils import timezone

from app.advocates.models import AdvocateProfile
from .serializers import (
    AdvocateProfileSerializer,
    AdvocateCreateSerializer,
    AdvocateUpdateSerializer,
    AssistantLawyerSerializer,
    AdvocateIDUploadSerializer,
    AssistantLawyerCreateSerializer,
)
from .permissions import (
    IsAdvocate,
    IsAdmin,
    CanCreateAdvocateProfile,
)
from . import services


# =================================================
# ADVOCATE PROFILE VIEWS
# =================================================

class AdvocateCreateView(APIView):
    permission_classes = [IsAuthenticated, CanCreateAdvocateProfile]

    def post(self, request):
        if hasattr(request.user, "advocate_profile"):
            return Response(
                {"error": "Advocate profile already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = AdvocateCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        advocate = serializer.save()

        return Response(
            {
                "message": "Advocate profile created successfully ✅",
                "data": AdvocateProfileSerializer(advocate).data,
            },
            status=status.HTTP_201_CREATED,
        )
class AdvocateListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = AdvocateProfile.objects.filter(
            is_verified=True,
            is_active=True,
        )

        specialization = request.query_params.get("specialization")
        city = request.query_params.get("city")

        if specialization:
            queryset = queryset.filter(specialization=specialization)

        if city:
            queryset = queryset.filter(city__iexact=city)

        serializer = AdvocateProfileSerializer(queryset, many=True)

        return Response(
            {
                "message": "Verified advocates fetched successfully ✅",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class AdvocateDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        advocate = get_object_or_404(
            AdvocateProfile,
            id=pk,
            is_verified=True,
            is_active=True,
        )

        serializer = AdvocateProfileSerializer(advocate)

        return Response(
            {
                "message": "Advocate profile fetched successfully ✅",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class AdvocateUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def patch(self, request):
        advocate = getattr(request.user, "advocate_profile", None)

        if not advocate:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AdvocateUpdateSerializer(
            advocate,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Advocate profile updated successfully ✅",
                "data": AdvocateProfileSerializer(advocate).data,
            },
            status=status.HTTP_200_OK,
        )
class AdvocateUploadOfficialIDView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        advocate = getattr(request.user, "advocate_profile", None)

        if not advocate:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AdvocateIDUploadSerializer(
            advocate,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Official ID uploaded successfully ✅ Awaiting verification"
            },
            status=status.HTTP_200_OK,
        )

class AdvocateVerifyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        advocate = get_object_or_404(AdvocateProfile, id=pk)

        if advocate.is_verified:
            return Response(
                {"error": "Advocate already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not advocate.official_id_card:
            return Response(
                {"error": "Official ID not uploaded"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        advocate.is_verified = True
        advocate.verified_at = timezone.now()
        advocate.verified_by = request.user
        advocate.save(update_fields=["is_verified", "verified_at", "verified_by"])

        return Response(
            {
                "message": "Advocate verified successfully ✅",
                "data": AdvocateProfileSerializer(advocate).data,
            },
            status=status.HTTP_200_OK,
        )


# =================================================
# ASSISTANT LAWYER VIEWS
# =================================================
class AssignAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        advocate = getattr(request.user, "advocate_profile", None)

        if not advocate:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AssistantLawyerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assistant = services.assign_assistant(
            advocate=advocate,
            assistant_user_id=serializer.validated_data["user_id"],
        )

        return Response(
            {
                "message": "Assistant assigned successfully ✅",
                "data": AssistantLawyerSerializer(assistant).data,
            },
            status=status.HTTP_201_CREATED,
        )

class ListAssistantsView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def get(self, request):
        advocate = getattr(request.user, "advocate_profile", None)

        if not advocate:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        assistants = advocate.assistants.select_related("user").all()

        serializer = AssistantLawyerSerializer(assistants, many=True)

        return Response(
            {
                "message": "Assistants fetched successfully ✅",
                "count": assistants.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
