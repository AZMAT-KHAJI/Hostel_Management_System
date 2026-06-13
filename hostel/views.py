from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.db.models import F
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .models import StudentProfile, Complaint, FeePayment, RoomChangeRequest
from .forms import RoomChangeRequestForm
from django.http import HttpResponse
from .models import FeePayment
from django.utils import timezone

def home(request):
    return render(request, 'hostel/home.html')


def admin_dashboard(request):
    # Example: fetch data for dashboard stats
    total_students = StudentProfile.objects.count()
    total_rooms = Room.objects.count()
    empty_rooms = Room.objects.filter(occupants__lt=models.F('capacity')).count()
    complaints_pending = Complaint.objects.filter(resolved=False).count()

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'empty_rooms': empty_rooms,
        'complaints_pending': complaints_pending,
    }
    return render(request, 'hostel/admin_dashboard.html', context)

def student_dashboard(request):
    # Get logged-in student profile
    student = get_object_or_404(StudentProfile, user=request.user)
    
    # Fetch student's complaints and fee payments
    complaints = Complaint.objects.filter(student=student)
    fees = FeePayment.objects.filter(student=student)
    try:
        room_allotment = RoomAllotment.objects.get(student=student)
        assigned_room = room_allotment.room.room_no
    except RoomAllotment.DoesNotExist:
        assigned_room = "Not Assigned"
    context = {
        'student': student,
        'complaints': complaints,
        'fees': fees,
        'assigned_room' : assigned_room
    }
    return render(request, 'hostel/student_dashboard.html', context)


# STUDENT SIGNUP
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.email = form.cleaned_data['email']
            user.save()
            StudentProfile.objects.create(
                user=user,
                usn=form.cleaned_data['usn'],
                phone=form.cleaned_data['phone'],
                year=form.cleaned_data['year'],
                gender=form.cleaned_data['gender'],
                department=form.cleaned_data['department'],
                parent_name=form.cleaned_data['parent_name'],
                parent_phone=form.cleaned_data['parent_phone'],
                address=form.cleaned_data['address']
            )
            return redirect('student_login')
    else:
        form = StudentSignupForm()
    return render(request,'hostel/student_signup.html',{'form':form})

# STUDENT LOGIN
def student_login(request):
    form = StudentLoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user())
        return redirect('student_dashboard')
    return render(request,'hostel/student_login.html',{'form':form})


# ADMIN LOGIN
def admin_login(request):
    form = AdminLoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user())
        return redirect('admin_dashboard')
    return render(request,'hostel/admin_login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('student_login') 

@login_required
def submit_complaint(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = student
            complaint.save()
            return redirect('student_dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'hostel/complaint_form.html', {'form': form})

@login_required
def pay_fee(request):
    student = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student = student
            fee.status = 'Pending'
            fee.save()
            return redirect('student_dashboard')
    else:
        form = FeePaymentForm()
    return render(request, 'hostel/pay_fee.html', {'form': form})


@login_required
def request_room(request):
    student = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']

            if room.occupants >= room.capacity:
                return render(request, 'hostel/request_room.html', {
                    'form': form,
                    'error': 'This room is already full!'
                })

            # Check if student already has a room
            allotment, created = RoomAllotment.objects.get_or_create(student=student)
            
            if not created:
                # Moving from old room: decrement occupants
                old_room = allotment.room
                if old_room and old_room != room:
                    old_room.occupants = max(0, old_room.occupants - 1)
                    old_room.save()

                allotment.room = room
                allotment.allot_date = timezone.now()
                allotment.save()
            else:
                allotment.room = room
                allotment.allot_date = timezone.now()
                allotment.save()

            # Increment occupants for new room
            room.occupants += 1
            room.save()

            return redirect('student_dashboard')
    else:
        form = RoomRequestForm()

    return render(request, 'hostel/request_room.html', {'form': form})


@login_required
def view_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/rooms.html', {'rooms': rooms})

@login_required
def view_receipt(request, fee_id):
    fee = get_object_or_404(FeePayment, id=fee_id, student__user=request.user)
    return render(request, 'hostel/receipt.html', {'fee': fee})


@login_required
def approve_fee(request, fee_id):
    if not request.user.is_admin:
        return redirect('student_dashboard')

    fee = FeePayment.objects.get(id=fee_id)
    if request.method == 'POST':
        form = FeeApprovalForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = FeeApprovalForm(instance=fee)

    return render(request, 'hostel/approve_fee.html', {'form': form, 'fee': fee})

@login_required
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    fees = FeePayment.objects.filter(student=student)
    return render(request, 'hostel/student_dashboard.html', {
        'student': student,
        'fees': fees
    })

def student_dashboard(request):
    # Get logged-in student profile
    student = get_object_or_404(StudentProfile, user=request.user)
    
    # Fetch student's complaints and fee payments
    complaints = Complaint.objects.filter(student=student)
    fees = FeePayment.objects.filter(student=student)
    
    context = {
        'student': student,
        'complaints': complaints,
        'fees': fees,
    }
    return render(request, 'hostel/student_dashboard.html', context)

@login_required
def payment_status(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    payments = FeePayment.objects.filter(student=student)
    return render(request, 'hostel/payment_status.html', {'payments': payments})

@login_required
def room_change_request(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = RoomChangeRequestForm(request.POST)
        if form.is_valid():
            room_request = form.save(commit=False)
            room_request.student = student
            room_request.status = 'Pending'  # initially pending
            room_request.save()
            return redirect('student_dashboard')
    else:
        form = RoomChangeRequestForm()
    return render(request, 'hostel/room_change_form.html', {'form': form})

@login_required
def student_profile(request):
    student = get_object_or_404(StudentProfile, user=request.user)


    # Get most recent room allotment (if any)
    allotment = RoomAllotment.objects.filter(student=student).order_by('-allot_date').first()

    context = {
        'student': student,
        'name' : student.user.username,
        'room': allotment.room if allotment else None,
        'email': student.user.email,  # email from User model
        'contact': student.phone,
        'Roll No' : student.usn,
    }
    return render(request, 'hostel/student_profile.html', context)

@login_required
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)

    complaints = Complaint.objects.filter(student=student)
    fees = FeePayment.objects.filter(student=student)

    try:
        room_allotment = RoomAllotment.objects.get(student=student)
        assigned_room = room_allotment.room.room_no
    except RoomAllotment.DoesNotExist:
        assigned_room = None

    return render(request, 'hostel/student_dashboard.html', {
        'student': student,
        'complaints': complaints,
        'fees': fees,
        'assigned_room': assigned_room
    })
