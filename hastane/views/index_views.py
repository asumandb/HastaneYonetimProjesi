from django.shortcuts import render
from django.views.generic import TemplateView

def index_view(request):
    """
    Ana sayfa view'ı - Hastane tanıtım sayfasını gösterir
    """
    context = {
        'page_title': 'Hastane Yönetim Sistemi - Ana Sayfa',
        'hospital_name': 'Hastane Yönetim',
    }
    return render(request, 'index.html', context)

class IndexView(TemplateView):
    """
    Ana sayfa için class-based view
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Hastane Yönetim Sistemi - Ana Sayfa',
            'hospital_name': 'Hastane Yönetim',
        })
        return context
