from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import F
from .models import User, StudentProfile, Complaint, FeePayment, Room, RoomChangeRequest



# Student Signup
class StudentSignupForm(UserCreationForm):
    usn = forms.CharField()
    email = forms.EmailField(required=True)
    phone = forms.CharField()
    year = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female')])
    department = forms.CharField()
    parent_name = forms.CharField()
    parent_phone = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username','email','usn','phone','year','gender','department','parent_name','parent_phone','address','password1','password2']


# Student/Admin Login
class StudentLoginForm(AuthenticationForm):
    pass

class AdminLoginForm(AuthenticationForm):
    pass

# Complaint Form
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title','details']

# Fee Payment Form
class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount']

class RoomRequestForm(forms.Form):
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(occupants__lt=F('capacity')),
        label="Select Room",
        empty_label="-- Select Room --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount'] 
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
        }



class FeeApprovalForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['receipt_number', 'status']

class RoomChangeRequestForm(forms.ModelForm):
    class Meta:
        model = RoomChangeRequest
        fields = ['requested_room', 'reason']
        widgets = {
            'requested_room': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your reason for room change here...'
            })
        }