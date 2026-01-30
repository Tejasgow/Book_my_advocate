from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_invoice(payment):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, 800, "LEGAL SERVICE INVOICE")
    pdf.drawString(50, 760, f"Invoice ID: INV-{payment.id}")
    pdf.drawString(50, 740, f"Client: {payment.client.user.username}")
    pdf.drawString(50, 720, f"Appointment ID: {payment.appointment.id}")
    pdf.drawString(50, 700, f"Amount Paid: ₹{payment.amount}")
    pdf.drawString(50, 680, f"Payment Status: {payment.status}")

    pdf.drawString(50, 640, "Thank you for choosing our legal services.")

    pdf.showPage()
    pdf.save()

    return response
