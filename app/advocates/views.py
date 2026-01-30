from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.accounts.models import User
from app.advocates.models import AdvocateProfile, AssistantLawyer
from .serializers import (
    AdvocateProfileSerializer,
    AdvocateCreateSerializer,
    AdvocateUpdateSerializer,
    AssistantLawyerSerializer
)
from .permissions import IsAdvocate, IsAdminOrReadOnly
from . import services


# -----------------------------
# ADVOCATE PROFILE VIEWS
# -----------------------------

class AdvocateCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        serializer = AdvocateCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        advocate = services.create_advocate_profile(request.user, serializer.validated_data)
        return Response({
            "message": "Advocate profile created successfully ✅",
            "data": AdvocateProfileSerializer(advocate).data
        }, status=status.HTTP_201_CREATED)


class AdvocateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specialization = request.query_params.get('specialization')
        advocates = services.list_verified_advocates(specialization)
        serializer = AdvocateProfileSerializer(advocates, many=True)
        return Response({
            "message": "Advocates fetched successfully ✅",
            "data": serializer.data
        })


class AdvocateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        advocate = services.get_advocate_by_id(pk)
        serializer = AdvocateProfileSerializer(advocate)
        return Response({
            "message": "Advocate profile fetched successfully ✅",
            "data": serializer.data
        })


class AdvocateUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def put(self, request):
        try:
            advocate = request.user.advocate_profile
        except AdvocateProfile.DoesNotExist:
            return Response({"error": "Advocate profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdvocateUpdateSerializer(advocate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        advocate = services.update_advocate_profile(advocate, serializer.validated_data)

        return Response({
            "message": "Advocate profile updated successfully ✅",
            "data": AdvocateProfileSerializer(advocate).data
        })


class AdvocateVerifyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request, pk):
        advocate = services.get_advocate_by_id(pk)
        advocate = services.verify_advocate(advocate)
        return Response({
            "message": f"{advocate.user.username} has been verified successfully ✅",
            "data": AdvocateProfileSerializer(advocate).data
        })


# -----------------------------
# ASSISTANT LAWYER VIEWS
# -----------------------------

class AssignAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        advocate = request.user.advocate_profile
        assistant_user_id = request.data.get('user_id')
        assistant = services.assign_assistant(advocate, assistant_user_id)
        return Response({
            "message": "Assistant lawyer assigned successfully ✅",
            "data": AssistantLawyerSerializer(assistant).data
        })


class ListAssistantsView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def get(self, request):
        advocate = request.user.advocate_profile
        assistants = services.list_assistants(advocate)
        serializer = AssistantLawyerSerializer(assistants, many=True)
        return Response({
            "message": "Assistants fetched successfully ✅",
            "data": serializer.data
        })
