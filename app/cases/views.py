from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Case, CaseHearing, CaseDocument
from .serializers import (
    CaseSerializer,
    CaseCreateSerializer,
    CaseHearingSerializer,
    CaseDocumentSerializer
)
from .permissions import IsAdvocate, IsCaseOwner


# -------------------------------------------------
# Create Case (ADVOCATE)
# -------------------------------------------------
class CreateCaseView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request):
        serializer = CaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        case = serializer.save()

        return Response(
            CaseSerializer(case).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------------------------------
# User Cases
# -------------------------------------------------
class UserCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cases = Case.objects.filter(client=request.user)
        return Response(CaseSerializer(cases, many=True).data)


# -------------------------------------------------
# Advocate Cases
# -------------------------------------------------
class AdvocateCasesView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def get(self, request):
        cases = Case.objects.filter(
            advocate=request.user.advocate_profile
        )
        return Response(CaseSerializer(cases, many=True).data)


# -------------------------------------------------
# Case Detail
# -------------------------------------------------
class CaseDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, pk):
        try:
            case = Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            return Response(
                {"detail": "Case not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, case)
        return Response(CaseSerializer(case).data)


# -------------------------------------------------
# Add Hearing (ADVOCATE)
# -------------------------------------------------
class CaseHearingCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdvocate]

    def post(self, request, case_id):
        case = Case.objects.get(
            id=case_id,
            advocate=request.user.advocate_profile
        )

        serializer = CaseHearingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(case=case)

        return Response(serializer.data, status=201)


# -------------------------------------------------
# View Hearings (CLIENT + ADVOCATE)
# -------------------------------------------------
class CaseHearingListView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, case_id):
        case = Case.objects.get(id=case_id)
        self.check_object_permissions(request, case)

        hearings = case.hearings.all()
        return Response(
            CaseHearingSerializer(hearings, many=True).data
        )


# -------------------------------------------------
# Upload Document (CLIENT + ADVOCATE)
# -------------------------------------------------
class CaseDocumentUploadView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def post(self, request, case_id):
        case = Case.objects.get(id=case_id)
        self.check_object_permissions(request, case)

        serializer = CaseDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            case=case,
            uploaded_by=request.user
        )

        return Response(serializer.data, status=201)


# -------------------------------------------------
# View Documents (CLIENT + ADVOCATE)
# -------------------------------------------------
class CaseDocumentListView(APIView):
    permission_classes = [IsAuthenticated, IsCaseOwner]

    def get(self, request, case_id):
        case = Case.objects.get(id=case_id)
        self.check_object_permissions(request, case)

        docs = case.documents.all()
        return Response(
            CaseDocumentSerializer(docs, many=True).data
        )


# -------------------------------------------------
# Download Document (CLIENT + ADVOCATE)
# -------------------------------------------------
class CaseDocumentDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        try:
            doc = CaseDocument.objects.get(id=doc_id)
        except CaseDocument.DoesNotExist:
            return Response(
                {"detail": "Document not found"},
                status=404
            )

        case = doc.case

        # permission check
        if not (
            case.client == request.user or
            (
                hasattr(request.user, 'advocate_profile') and
                case.advocate == request.user.advocate_profile
            )
        ):
            return Response(
                {"detail": "Access denied"},
                status=403
            )

        return FileResponse(
            doc.document.open('rb'),
            as_attachment=True,
            filename=doc.document.name.split('/')[-1]
        )
