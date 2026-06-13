from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

# --------------------------
# Custom User Model
# --------------------------
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# --------------------------
# Student Profile
# --------------------------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usn = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    year = models.IntegerField()
    gender = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


# --------------------------
# Rooms
# --------------------------
class Room(models.Model):
    room_no = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=1)
    occupants = models.IntegerField(default=0)

    def __str__(self):
        return self.room_no

    def is_full(self):
        return self.occupants >= self.capacity


# --------------------------
# Room Allotment
# --------------------------
class RoomAllotment(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allot_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.user.username} -> {self.room.room_no if self.room else 'None'}"

# --------------------------
# Fee Payment
# --------------------------
class FeePayment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    receipt_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.student.user.username} - ₹{self.amount} - ({self.status})"


# --------------------------
# Complaints
# --------------------------
class Complaint(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, default="Pending")
    resolved = models.BooleanField(default=False)

    def __str__(self):
        status = "Resolved" if self.resolved else "Pending"
        return f"{self.title} ({status})"


# --------------------------
# Room Change Request
# --------------------------
class RoomChangeRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    requested_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.status}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    year = models.PositiveIntegerField()  # e.g., 1, 2, 3, 4
    department = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, default='N/A')
    address = models.TextField(default='N/A')


    def __str__(self):
        return f"{self.user.username} - {self.department} Year {self.year}"
