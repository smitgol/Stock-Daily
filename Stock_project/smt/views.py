from django.shortcuts import render, redirect
from .forms import forr
from .models import trails
# Create your views here.


def home(request):
    form = forr()
    if request.method == 'POST':
        form = forr(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    return render(request, 'index.html', {'form': form})

def index(request):
    fo = trails.objects.all()
    return render(request, 'index.html', {'fo':fo})