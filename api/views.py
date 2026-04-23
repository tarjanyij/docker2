import json,os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reading, Threshold, AlertRecipient, AlertStatus

@csrf_exempt
def ingest(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST only"}, status=405)

        if request.headers.get("X-API-KEY") != os.getenv('API_KEY'):
            return JsonResponse({"error": "unauthorized"}, status=401)

        data = json.loads(request.body)
        device_id = data.get("device_id", "unknown")

        Reading.objects.create(
            device_id=device_id,
            t1=data["sensor1"]["temperature"],
            h1=data["sensor1"]["humidity"],
            t2=data["sensor2"]["temperature"],
            h2=data["sensor2"]["humidity"],
            t3=data.get("sensor3", {}).get("temperature"),
            h3=data.get("sensor3", {}).get("humidity"),
        )

        # Küszöbértékek ellenőrzése
        sensors_data = {
            't1': data["sensor1"]["temperature"],
            'h1': data["sensor1"]["humidity"],
            't2': data["sensor2"]["temperature"],
            'h2': data["sensor2"]["humidity"],
            't3': data.get("sensor3", {}).get("temperature"),
            'h3': data.get("sensor3", {}).get("humidity"),
        }
        check_thresholds(device_id, sensors_data)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def check_thresholds(device_id, sensors_data):
    thresholds = Threshold.objects.filter(device_id=device_id, enabled=True)
    for threshold in thresholds:
        sensor_value = sensors_data.get(threshold.sensor)
        if sensor_value is None:
            continue

        # AlertStatus lekérése vagy létrehozása
        alert_status, created = AlertStatus.objects.get_or_create(
            device_id=device_id,
            sensor=threshold.sensor
        )

        # Küszöbérték túllépése?
        if sensor_value > threshold.threshold_value:
            if not alert_status.is_alerted:
                # Riasztás küldése
                recipients = AlertRecipient.objects.filter(
                    device_id=device_id,
                    sensor=threshold.sensor
                ).values_list('email', flat=True)
                if recipients:
                    send_alert_email(device_id, threshold.sensor, sensor_value, threshold.threshold_value, recipients)

                # AlertStatus frissítése
                alert_status.is_alerted = True
                alert_status.last_alert_time = timezone.now()
                alert_status.save()
        else:
            # Érték már normális
            if alert_status.is_alerted:
                alert_status.is_alerted = False
                alert_status.last_reset_time = timezone.now()
                alert_status.save()

def send_alert_email(device_id, sensor, sensor_value, threshold_value, recipients):
    sensor_labels = {
        't1': 'Hőmérséklet 1',
        'h1': 'Páratartalom 1',
        't2': 'Hőmérséklet 2',
        'h2': 'Páratartalom 2',
        't3': 'Hőmérséklet 3',
        'h3': 'Páratartalom 3'
    }
    sensor_label = sensor_labels.get(sensor, sensor)

    subject = f'IoT Riasztás: {device_id} - {sensor_label}'
    message = f'''
Eszköz: {device_id}
Szenzor: {sensor_label}
Aktuális érték: {sensor_value:.2f}
Küszöbérték: {threshold_value:.2f}

Idő: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
    '''

    try:
        send_mail(
            subject,
            message,
            os.getenv('DEFAULT_FROM_EMAIL', 'noreply@iot-dashboard.local'),
            list(recipients),
            fail_silently=False
        )
    except Exception as e:
        print(f'Email küldési hiba: {e}')