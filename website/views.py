from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

from django.contrib.auth.decorators import user_passes_test

'''def home(request):
    return render (request, 'home.html')'''


'''def home(request):
    if request.method == 'POST':
        # Get the username and password from the submitted form data
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's built-in authentication function to check if the user is valid
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If the user is valid, log them in and redirect to a success page
            login(request, user)
            return redirect("home")
        else:
            # If the user is not valid, return an error message
            error_message = 'Invalid username or password.'
            return render(request, 'home.html', {'error_message': error_message})
    else:
        # If the request method is not POST, render the login form
        return render(request, 'home.html')'''


def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Siz tizimga kirdingiz!")
            return redirect("home")
        else:
            messages.warning(request, "Xatolik, boshqattan urinib ko'ring!")
            return redirect("home")
    else:
        return render(request, "home.html", {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz!")
    return redirect("home")


def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've been registered in")
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")

    return render(request, "register.html", {"form": form})


def record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, "record.html", {"record": record})
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        del_record = Record.objects.get(id=pk)
        del_record.delete()
        messages.success(request, "You deleted the record")
        return redirect("home")
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if form.is_valid():
            add_record = form.save()
            messages.success(request, f"Record {add_record.first_name} was added")
            return redirect("home")
        return render(request, "add_record.html", {"form": form})
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            updated_record = form.save()
            messages.success(request, f"Record '{updated_record.first_name}' was added")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.error(request, "You have to login")
        return redirect("home")


def superuser_or_permission_required(permission):
    def decorator(view_func):
        @user_passes_test(lambda user: user.is_superuser or user.has_perm(permission))
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator