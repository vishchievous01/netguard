from django.shortcuts import render
from .models import AttackEvent
from django.db.models import Count
from django.db.models.functions import TruncHour
from django.http import JsonResponse

def attack_timeline(request):
    events = AttackEvent.objects.order_by("-timestamp")[:50]
    return render(request, "reports/timeline.html", {
        "events": events
    })


def dashboard(request):
    events = AttackEvent.objects.order_by("-timestamp")[:50]

    top_ips = (
        AttackEvent.objects
        .values("ip_address")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    attacks_per_hour = (
        AttackEvent.objects
        .annotate(hour=TruncHour("timestamp"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by("hour")
    )

    attacks_by_country = (
        AttackEvent.objects
        .exclude(country=None)
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    context = {
        "events": events,
        "top_ips": top_ips,
        "attacks_per_hour": list(attacks_per_hour),
        "attacks_by_country": list(attacks_by_country),
    }

    return render(request, "reports/dashboard.html", context)

def api_attacks(request):
    events = AttackEvent.objects.order_by("-timestamp")[:100]

    data = []

    for e in events:
        data.append({
            "time": e.timestamp.strftime("%H:%M:%S"),
            "ip": e.ip_address,
            "event": e.event_type,
            "attempts": e.attempts,
            "blocked": e.blocked,
            "country": e.country,
        })

    return JsonResponse(data, safe=False)


def api_attack_map(request):

    events = AttackEvent.objects.exclude(latitude=None)

    data = []

    for e in events:
        data.append({
            "ip": e.ip_address,
            "lat": e.latitude,
            "lon": e.longitude,
            "country": e.country,
            "city": e.city
        })

    return JsonResponse(data, safe=False)