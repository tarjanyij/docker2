from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from api.models import Reading, Threshold, AlertRecipient, SensorNameSet
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
    # load sensor name set for this device (fallbacks will be used in template)
    sns = SensorNameSet.objects.filter(device_id=device).first()
    sensor_names = {
        't1': sns.t1_name if sns and sns.t1_name else 'T1',
        't2': sns.t2_name if sns and sns.t2_name else 'T2',
        't3': sns.t3_name if sns and sns.t3_name else 'T3',
        'h1': sns.h1_name if sns and sns.h1_name else 'H1',
        'h2': sns.h2_name if sns and sns.h2_name else 'H2',
        'h3': sns.h3_name if sns and sns.h3_name else 'H3',
    }

    return render(request, 'dashboard.html', {
        'data': data,
        'device': device,
        'devices': devices,
        'start_time': to_local_input(start_time),
        'end_time': to_local_input(end_time),
        'sensor_names': sensor_names,
    })


def sensor_names(request):
    devices = Reading.objects.values_list('device_id', flat=True).distinct()
    device_id = request.GET.get('device') or (devices[0] if devices else '')

    sns = None
    if device_id:
        sns = SensorNameSet.objects.filter(device_id=device_id).first()

    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        t1 = request.POST.get('t1_name','T1')
        h1 = request.POST.get('h1_name','H1')
        t2 = request.POST.get('t2_name','T2')
        h2 = request.POST.get('h2_name','H2')
        t3 = request.POST.get('t3_name','T3')
        h3 = request.POST.get('h3_name','H3')

        obj, created = SensorNameSet.objects.update_or_create(
            device_id=device_id,
            defaults={
                't1_name': t1,
                'h1_name': h1,
                't2_name': t2,
                'h2_name': h2,
                't3_name': t3,
                'h3_name': h3,
            }
        )

        return redirect(f'/sensor-names/?device={device_id}')

    return render(request, 'sensor_names.html', {
        'devices': devices,
        'device_id': device_id,
        'sns': sns,
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
