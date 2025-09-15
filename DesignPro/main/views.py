from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, CustomLoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Application, Category
from .forms import ApplicationForm, CategoryForm, StatusForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html', {'user': request.user})

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def is_staff(user):
    return user.is_staff

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('application_list')
    else:
        form = ApplicationForm()

    return render(request, 'create_application.html', {'form': form})


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'application_list.html', {'applications': applications})


@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Заявка успешно удалена!')
        return redirect('application_list')

    return render(request, 'delete_application.html', {'application': application})


@user_passes_test(is_staff)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'create_category.html', {'form': form})


@user_passes_test(is_staff)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


@user_passes_test(is_staff)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect('category_list')

    return render(request, 'delete_category.html', {'category': category})

@login_required
def application_list(request):
    if request.user.is_staff:
        applications = Application.objects.all().order_by('-created_at')
    else:
        applications = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'application_list.html', {'applications': applications})

@login_required
def change_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if not application.can_change_status(request.user):
        return HttpResponseForbidden("У вас нет прав для изменения статуса этой заявки")

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'Статус заявки "{application.name}" изменен на "{application.get_status_display()}"')
            return redirect('application_list')
    else:
        form = StatusForm(instance=application)

    return render(request, 'change_status.html', {
        'form': form,
        'application': application
    })

@user_passes_test(is_staff)
def staff_application_list(request):
    status_filter = request.GET.get('status', '')

    if status_filter:
        applications = Application.objects.filter(status=status_filter).order_by('-created_at')
    else:
        applications = Application.objects.all().order_by('-created_at')

    return render(request, 'staff_application_list.html', {
        'applications': applications,
        'status_filter': status_filter
    })