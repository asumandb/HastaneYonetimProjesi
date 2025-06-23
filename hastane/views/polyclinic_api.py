from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..models.clinic_model import Clinic
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def polyclinic_api(request):
    if request.method == "GET":
        clinics = Clinic.objects.all().values('id', 'name')
        return JsonResponse(list(clinics), safe=False)
    elif request.method == "POST":
        data = request.POST or json.loads(request.body.decode())
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Poliklinik adı gerekli.'}, status=400)
        clinic = Clinic.objects.create(name=name)
        return JsonResponse({'id': clinic.id, 'name': clinic.name}, status=201) 