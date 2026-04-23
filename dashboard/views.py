from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from api.models import Reading, Threshold, AlertRecipient
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    device = request.GET.get('device', 'Munkacsy Szerverszoba')
    start_time_str = request.GET.get('start_time', '')
    end_time_str = request.GET.get('end_time', '')

    # Ha nincs megadva időintervallum, akkor az utolsó 1 óra
    if not start_time_str or not end_time_str:
            end_time = timezone.now()
            start_time = end_time - timedelta(hours=1)
    else:
        try:
            # A HTML `datetime-local` mező általában helyi időt ad vissza (naive),
            # ezért tegyük tz-aware-re a helyi zónával.
            start_time = timezone.datetime.fromisoformat(start_time_str)
            end_time = timezone.datetime.fromisoformat(end_time_str)
            if timezone.is_naive(start_time):
                    start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
            if timezone.is_naive(end_time):
                    end_time = timezone.make_aware(end_time, timezone.get_current_timezone())
        except Exception:
                end_time = timezone.now()
                start_time = end_time - timedelta(hours=1)

    # Szűrés eszköz és időintervallum alapján
    data = Reading.objects.filter(device_id=device, created_at__gte=start_time, created_at__lte=end_time).order_by('-created_at')

    # Megkapjuk az összes device_id-t - csak az utolsó 1 órából gyorsabban
    devices = Reading.objects.filter(created_at__gte=timezone.now()-timedelta(hours=1)).values_list('device_id', flat=True).distinct()

    def to_local_input(dt):
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        local_dt = timezone.localtime(dt)
        return local_dt.strftime('%Y-%m-%dT%H:%M')

    return render(request, 'dashboard.html', {
        'data': data,
        'device': device,
        'devices': devices,
        'start_time': to_local_input(start_time),
        'end_time': to_local_input(end_time)
    })

def settings(request):
  devices=Reading.objects.values_list('device_id',flat=True).distinct()

  if request.method == 'POST':
    action = request.POST.get('action')
    device_id = request.POST.get('device_id')
    sensor = request.POST.get('sensor')

    if action == 'set_threshold':
        threshold_value = float(request.POST.get('threshold_value'))
        Threshold.objects.update_or_create(
            device_id=device_id,
            sensor=sensor,
            defaults={'threshold_value': threshold_value, 'enabled': True}
        )
        messages.success(request, f'Küszöbérték beállítva: {sensor} = {threshold_value}')

    elif action == 'add_recipient':
        email = request.POST.get('email')
        AlertRecipient.objects.get_or_create(
            device_id=device_id,
            sensor=sensor,
            email=email
        )
        messages.success(request, f'Email cím felvéve: {email}')

    elif action == 'delete_recipient':
        email = request.POST.get('email')
        AlertRecipient.objects.filter(
            device_id=device_id,
            sensor=sensor,
            email=email
        ).delete()
        messages.success(request, f'Email cím törölve: {email}')

    elif action == 'delete_threshold':
        Threshold.objects.filter(
            device_id=device_id,
            sensor=sensor
        ).delete()
        messages.success(request, f'Küszöbérték törölve: {sensor}')

    return redirect('settings')

  thresholds=Threshold.objects.all()
  recipients=AlertRecipient.objects.all()
 
  return render(request,'settings.html',{
    'devices':devices,
    'thresholds':thresholds,
    'recipients':recipients,
    'sensor_choices':Threshold.SENSOR_CHOICES
})
