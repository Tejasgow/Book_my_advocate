from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Case, CaseDocument, CaseHearing
from .serializers import (
    CaseSerializer,
    CaseCreateSerializer,
    CaseHearingSerializer,
    CaseDocumentSerializer
)
from .permissions import IsAdvocate, IsCaseOwner
from . import services


# -------------------------------------------------
# CREATE CASE (ADVOCATE)
# -------------------------------------------------
class CreateCaseView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        serializer = CaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        case = services.create_case(serializer)

        return Response(
            CaseSerializer(case).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------------------------------
# CLIENT CASES
# -------------------------------------------------
class UserCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "client_profile"):
            return Response(
                {"error": "Client profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cases = services.get_client_cases(request.user.client_profile)
        return Response(CaseSerializer(cases, many=True).data)


# -------------------------------------------------
# ADVOCATE CASES
# -------------------------------------------------
class AdvocateCasesView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def get(self, request):
        if not hasattr(request.user, "advocate_profile"):
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cases = services.get_advocate_cases(request.user.advocate_profile)
        return Response(CaseSerializer(cases, many=True).data)


# -------------------------------------------------
# CASE DETAIL
# -------------------------------------------------
class CaseDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, pk):
        case = services.get_case(pk)
        if not case:
            return Response(
                {"error": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, case)
        return Response(CaseSerializer(case).data)


# -------------------------------------------------
# ADD HEARING (ADVOCATE)
# -------------------------------------------------
class CaseHearingCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request, case_id):
        try:
            advocate = request.user.advocate_profile
        except AttributeError:
            return Response(
                {"error": "Advocate profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        case = get_object_or_404(
            Case,
            id=case_id,
            advocate=advocate
        )

        serializer = CaseHearingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hearing = services.add_hearing(case, serializer)

        return Response(
            CaseHearingSerializer(hearing).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------------------------------
# VIEW HEARINGS
# -------------------------------------------------
class CaseHearingListView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, case_id):
        case = services.get_case(case_id)
        if not case:
            return Response(
                {"error": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, case)
        hearings = services.list_hearings(case)

        return Response(
            CaseHearingSerializer(hearings, many=True).data
        )


# -------------------------------------------------
# UPLOAD DOCUMENT
# -------------------------------------------------
class CaseDocumentUploadView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def post(self, request, case_id):
        case = services.get_case(case_id)
        if not case:
            return Response(
                {"error": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, case)

        serializer = CaseDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = services.upload_document(
            case,
            request.user,
            serializer
        )

        return Response(
            CaseDocumentSerializer(document).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------------------------------
# VIEW DOCUMENTS
# -------------------------------------------------
class CaseDocumentListView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, case_id):
        case = services.get_case(case_id)
        if not case:
            return Response(
                {"error": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, case)
        documents = services.list_documents(case)

        return Response(
            CaseDocumentSerializer(documents, many=True).data
        )


# -------------------------------------------------
# DOWNLOAD DOCUMENT
# -------------------------------------------------
class CaseDocumentDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        document = get_object_or_404(CaseDocument, id=doc_id)

        response = services.download_document(document, request.user)
        if not response:
            return Response(
                {"error": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        return response


# -------------------------------------------------
# ADMIN DASHBOARD STATS
# -------------------------------------------------
class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "total_cases": Case.objects.count(),
            "open_cases": Case.objects.filter(status="OPEN").count(),
            "in_progress_cases": Case.objects.filter(status="IN_PROGRESS").count(),
            "closed_cases": Case.objects.filter(status="CLOSED").count(),

            "total_hearings": CaseHearing.objects.count(),
            "total_documents": CaseDocument.objects.count(),
        }
        return Response(data)
