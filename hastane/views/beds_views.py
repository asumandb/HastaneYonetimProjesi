from django.shortcuts import render

def beds_view(request):
    return render(request, 'hastane/beds.html')
