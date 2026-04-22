from .models import DownloadLog
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
from .models import Notes, DownloadLog
from django.shortcuts import redirect


# Create your views here.

@login_required
def download_note(request, note_id, file_no):
    note = Notes.objects.get(id=note_id)

    # log save kar
    DownloadLog.objects.create(
        user=request.user,
        note=note
    )

    # actual file download logic
    return HttpResponse("Downloading...")

@login_required
def view_downloads(request):
    logs = DownloadLog.objects.all().order_by('-downloaded_at')
    return render(request, 'downloads.html', {'logs': logs})

def view_visitors(request):
    visitors = VisitorLog.objects.all().order_by('-visit_time')
    return render(request, 'view_visitors.html', {'visitors': visitors})

def DASHBOARD(request):
    logs = DownloadLog.objects.all().order_by('-downloaded_at')

    return render(request, 'dashboard.html', {
        'logs': logs
    })
    

@login_required
def download_note(request, note_id, file_no):

    note = Notes.objects.get(id=note_id)

    # ✅ IP capture
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # 👉 dynamic file select
    file_field = getattr(note, f'file{file_no}')

    if not file_field:
        return HttpResponse("File not found")

    file_path = file_field.path

    if os.path.exists(file_path):

        # ✅ ONLY ONE LOG (FINAL)
        DownloadLog.objects.create(
            user=request.user,
            note=note,
            ip_address=ip
        )

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response

    return HttpResponse("File not found")

def delete_download_log(request, log_id):
    log = DownloadLog.objects.get(id=log_id)
    log.delete()
    return redirect('view_downloads')

