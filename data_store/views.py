from django.shortcuts import render,redirect
from .scrapper_file import scrapper
from .models import Datastore
from django.contrib.auth.decorators import login_required

@login_required
def search_key(request):
    if request.method == 'POST':
        product_name = request.POST.get('search')
        if len(product_name)<=0:
            return render(request, 'data_store/search.html')     
        user = request.user
        status = 'Fetching'
        data_store = Datastore.objects.create(search_query=product_name, user=user, status=status)
       
        raw_data = scrapper.delay(product_name, data_store.id)    
        
        
        datastore = Datastore.objects.all().order_by('-id')

        return render(request, 'data_store/dataTable.html', {
            'all_data' : datastore
        })
    return render(request, 'data_store/search.html')

@login_required
def show_data(request):
    if request.method == 'GET':
        datastore = Datastore.objects.all().order_by('-id')
        return render(request, 'data_store/dataTable.html', {
            'all_data' : datastore 
        })

@login_required
def show_individual(request, id):
    datastore = Datastore.objects.filter(id=id).first()
    
    return render(request, 'data_store/individual_data.html', {
        "data_store" : datastore.raw_data,
        "product_name" : datastore.search_query
    })