from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from nssapp.models import CustomUser, UserReg, Notes
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

User = get_user_model()


def Index(request):
    return render(request, 'index.html')


@login_required(login_url='/')
def BASE(request):
    return render(request, 'base.html')


def DASHBOARD(request):
    user_admin = request.user
    try:
        user_reg = UserReg.objects.get(admin=user_admin)
    except UserReg.DoesNotExist:
        messages.error(request, "User registration details not found.")
        return render(request, 'dashboard.html')

    uploadedsub_count = Notes.objects.filter(nsuser=user_reg).count()
    user_notes = Notes.objects.filter(nsuser=user_reg)

    total_files = 0
    for note in user_notes:
        if note.file1:
            total_files += 1
        if note.file2:
            total_files += 1
        if note.file3:
            total_files += 1
        if note.file4:
            total_files += 1

    context = {
        'uploadedsub_count': uploadedsub_count,
        'total_files': total_files,
    }

    return render(request, 'dashboard.html', context)


def LOGIN(request):
    return render(request, 'login.html')


def doLogout(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('login')


def USERSIGNUP(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exist')
            return redirect('usersignup')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exist')
            return redirect('usersignup')

        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic,
        )
        user.set_password(password)
        user.save()

        nsuser = UserReg(
            admin=user,
            mobilenumber=mobno,
        )
        nsuser.save()

        messages.success(request, 'Signup Successfully')
        return redirect('usersignup')

    return render(request, 'signup.html')


@login_required(login_url='/')
def PROFILE(request):
    if request.method == "POST":
        customuser = CustomUser.objects.get(id=request.user.id)

        customuser.first_name = request.POST.get('first_name')
        customuser.last_name = request.POST.get('last_name')

        if 'profile_pic' in request.FILES:
            customuser.profile_pic = request.FILES['profile_pic']

        customuser.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    user = CustomUser.objects.get(id=request.user.id)
    nsuser = UserReg.objects.get(admin_id=request.user.id)

    return render(request, 'profile.html', {
        "user": user,
        "nsuser": nsuser
    })


def CHANGE_PASSWORD(request):
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']

        user = User.objects.get(id=request.user.id)

        if user.check_password(current):
            user.set_password(new_pas)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, 'Current password wrong')
            return redirect("change_password")

    return render(request, 'change-password.html')


def ADD_NOTES(request):
    if request.method == "POST":
        userreg = UserReg.objects.get(admin_id=request.user.id)

        notes = Notes(
            notestitle=request.POST.get('notestitle'),
            subject=request.POST.get('subject'),
            notesdesc=request.POST.get('notesdesc'),
            file1=request.FILES.get('file1'),
            file2=request.FILES.get('file2'),
            file3=request.FILES.get('file3'),
            file4=request.FILES.get('file4'),
            nsuser=userreg,
        )
        notes.save()

        messages.success(request, 'Notes Added Successfully')
        return redirect("add_notes")

    return render(request, 'add-notes.html')


@login_required(login_url='/')
def MANAGE_NOTES(request):
    userreg = UserReg.objects.get(admin_id=request.user.id)
    data_list = Notes.objects.filter(nsuser=userreg)

    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')

    try:
        data_list = paginator.page(page_number)
    except:
        data_list = paginator.page(1)

    return render(request, 'manage-notes.html', {'data_list': data_list})


@login_required(login_url='/')
def DELETE_NOTES(request, id):
    Notes.objects.get(id=id).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('manage_notes')


@login_required(login_url='/')
def VIEW_NOTES(request, id):
    data_notes = Notes.objects.get(id=id)
    return render(request, 'update_notes.html', {"data_notes": data_notes})


@login_required(login_url='/')
def EDIT_NOTES(request):
    if request.method == "POST":
        data = Notes.objects.get(id=request.POST.get('notes_id'))

        data.notestitle = request.POST.get('notestitle')
        data.subject = request.POST.get('subject')
        data.notesdesc = request.POST.get('notesdesc')

        for i in range(1, 5):
            file = request.FILES.get(f'file{i}')
            if file:
                setattr(data, f'file{i}', file)

        data.save()
        messages.success(request, "Updated successfully")
        return redirect('manage_notes')

    return render(request, 'manage-notes.html')


# 🔥 FINAL SEARCH FUNCTION (FIXED)
def SEARCH_NOTES(request):
    userreg = UserReg.objects.get(admin_id=request.user.id)

    search = request.GET.get('search', '')

    if search:
        data_list = Notes.objects.filter(
            Q(notestitle__icontains=search) |
            Q(subject__icontains=search),
            nsuser=userreg
        )
    else:
        data_list = Notes.objects.none()

    return render(request, 'search.html', {
        'data_list': data_list
    })


@login_required(login_url='/')
def NOTES_DETAILS(request):
    data_list = Notes.objects.all()
    paginator = Paginator(data_list, 10)

    page_number = request.GET.get('page')

    try:
        data_list = paginator.page(page_number)
    except:
        data_list = paginator.page(1)

    return render(request, 'notes.html', {"data_list": data_list})