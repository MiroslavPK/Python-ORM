from django.shortcuts import render, redirect
from fruitipediaApp.fruits.models import Fruit
from fruitipediaApp.fruits.forms import CategoryCreateForm, FruitCreateForm, FruitEditForm, FruitDeleteForm



def index(request):
    return render(request, template_name='common/index.html')


def dashboard(request):
    fruits = Fruit.objects.all()

    context = {
        'fruits': fruits
    }

    return render(request, template_name='common/dashboard.html', context=context)


def create_fruit(request):
    if request.method == 'GET':
        form = FruitCreateForm()
    else:
        form = FruitCreateForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('dashboard')
        
    context = {
        'form': form
    }

    return render(request, template_name='fruits/create-fruit.html', context=context)


def details_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()
    
    context = {
        'fruit': fruit
    }
    
    return render(request, template_name='fruits/details-fruit.html', context=context) 


def edit_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()

    if request.method == 'GET':
        form = FruitEditForm(instance=fruit)
    else:
        form = FruitEditForm(request.POST, instance=fruit)

        if form.is_valid():
            form.save()
        
        return redirect('dashboard')

    context = {
        'form': form,
        'fruit': fruit,
    }

    return render(request, template_name='fruits/edit-fruit.html', context=context)


def delete_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()

    if request.method == 'GET':
        form = FruitDeleteForm(instance = fruit)
    else:
        form = FruitDeleteForm(request.POST, instance = fruit)

        if form.is_valid():
            fruit.delete()

            return redirect('dashboard')
    
    context = {
        'form': form,
        'fruit': fruit,
    }

    return render(request, template_name='fruits/delete-fruit.html', context=context)


def create_category(request):
    if request.method == 'GET':
        form = CategoryCreateForm()
    else:
        form = CategoryCreateForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('dashboard')
    
    context = {
        'form': form,
    }

    return render(request, template_name='categories/create-category.html', context=context)