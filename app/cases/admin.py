from django.contrib import admin
from .models import Case, CaseHearing, CaseDocument


# -----------------------------
# Case Admin
# -----------------------------
@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id','title','client','advocate','status','created_at','updated_at')
    list_filter = ('status', 'created_at', 'advocate')
    search_fields = ('title','description','client__user__username','advocate__user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# -----------------------------
# Case Hearing Admin
# -----------------------------
@admin.register(CaseHearing)
class CaseHearingAdmin(admin.ModelAdmin):
    list_display = ('id','case','hearing_date','hearing_time','court_name','created_at')
    list_filter = ('hearing_date','court_name','case__advocate')
    search_fields = ('case__title','case__client__user__username','case__advocate__user__username','court_name')
    readonly_fields = ('created_at',)
    ordering = ('-hearing_date',)


# -----------------------------
# Case Document Admin
# -----------------------------
@admin.register(CaseDocument)
class CaseDocumentAdmin(admin.ModelAdmin):
    list_display = ('id','case','uploaded_by','document','description','created_at')
    list_filter = ('case__advocate','uploaded_by')
    search_fields = ('case__title','uploaded_by__user__username','description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
