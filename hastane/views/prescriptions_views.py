from django.shortcuts import render

def prescriptions_view(request):
    return render(request, 'hastane/prescriptions.html')
