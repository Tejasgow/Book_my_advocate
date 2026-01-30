from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import Case, CaseHearing, CaseDocument


# -------------------------------------------------
# Utils
# -------------------------------------------------
def send_sms(phone, message):
    if phone:
        print(f"SMS to {phone}: {message}")


# -------------------------------------------------
# Case Services
# -------------------------------------------------
def create_case(serializer):
    case = serializer.save()

    client_user = case.client.user
    advocate_user = case.advocate.user

    # Client notification
    if client_user.email:
        send_mail(
            "New Case Created ✅",
            f"Hi {client_user.username}, your case '{case.title}' has been created.",
            settings.DEFAULT_FROM_EMAIL,
            [client_user.email]
        )
    send_sms(client_user.phone, f"Your case '{case.title}' has been created ✅")

    # Advocate notification
    if advocate_user.email:
        send_mail(
            "New Case Assigned ✅",
            f"A new case '{case.title}' has been assigned to you.",
            settings.DEFAULT_FROM_EMAIL,
            [advocate_user.email]
        )
    send_sms(advocate_user.phone, f"New case '{case.title}' assigned to you ✅")

    return case


def get_client_cases(client_profile):
    return Case.objects.filter(client=client_profile)


def get_advocate_cases(advocate_profile):
    return Case.objects.filter(advocate=advocate_profile)


def get_case(pk):
    return get_object_or_404(Case, pk=pk)


# -------------------------------------------------
# Hearing Services
# -------------------------------------------------
def add_hearing(case, serializer):
    hearing = serializer.save(case=case)

    client_user = case.client.user
    if client_user.email:
        send_mail(
            "New Hearing Scheduled 📅",
            f"Hearing scheduled on {hearing.hearing_date} at {hearing.hearing_time}.",
            settings.DEFAULT_FROM_EMAIL,
            [client_user.email]
        )
    send_sms(client_user.phone, "New hearing scheduled ✅")

    return hearing


def list_hearings(case):
    return case.hearings.all()


# -------------------------------------------------
# Document Services
# -------------------------------------------------
def upload_document(case, user, serializer):
    document = serializer.save(
        case=case,
        uploaded_by=user
    )

    client_user = case.client.user
    advocate_user = case.advocate.user

    notify_user = advocate_user if user == client_user else client_user

    if notify_user.email:
        send_mail(
            "New Case Document Uploaded 📄",
            f"A new document was uploaded for case '{case.title}'.",
            settings.DEFAULT_FROM_EMAIL,
            [notify_user.email]
        )
    send_sms(notify_user.phone, "New case document uploaded ✅")

    return document


def list_documents(case):
    return case.documents.all()


def download_document(doc, user):
    case = doc.case

    if not (
        (hasattr(user, 'client_profile') and case.client == user.client_profile) or
        (hasattr(user, 'advocate_profile') and case.advocate == user.advocate_profile)
    ):
        return None

    return FileResponse(
        doc.document.open('rb'),
        as_attachment=True,
        filename=doc.document.name.split('/')[-1]
    )
