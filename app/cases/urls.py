from django.urls import path
from .views import (
    CreateCaseView,
    UserCasesView,
    AdvocateCasesView,
    CaseDetailView,
    CaseHearingListView,
    CaseHearingCreateView,
    CaseDocumentListView,
    CaseDocumentUploadView,
    CaseDocumentDownloadView,
)

urlpatterns = [

    # ===============================
    # CASES
    # ===============================
    path('cases/', UserCasesView.as_view(), name='user-cases'),             # client cases
    path('cases/advocate/', AdvocateCasesView.as_view(), name='advocate-cases'),
    path('cases/create/', CreateCaseView.as_view(), name='case-create'),
    path('cases/<int:pk>/', CaseDetailView.as_view(), name='case-detail'),

    # ===============================
    # CASE HEARINGS (Nested)
    # ===============================
    path('cases/<int:case_id>/hearings/',CaseHearingListView.as_view(),name='case-hearing-list'),
    path('cases/<int:case_id>/hearings/create/',CaseHearingCreateView.as_view(),name='case-hearing-create'),

    # ===============================
    # CASE DOCUMENTS (Nested)
    # ===============================
    path('cases/<int:case_id>/documents/',CaseDocumentListView.as_view(),name='case-document-list'),
    path('cases/<int:case_id>/documents/upload/',CaseDocumentUploadView.as_view(),name='case-document-upload'),
    path('cases/documents/<int:doc_id>/download/',CaseDocumentDownloadView.as_view(),name='case-document-download'),
]
