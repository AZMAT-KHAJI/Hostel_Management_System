from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction
import uuid
from .models import User, StudentProfile, Room, RoomAllotment, FeePayment, Complaint, Student, RoomChangeRequest
from .models import StudentProfile


from .models import (
    User,
    StudentProfile,   # keep if you use it
    Student,          # keep if you use it
    Room,
    RoomAllotment,
    FeePayment,
    Complaint,
    RoomChangeRequest,
)

# ---------------------------
# Fee Payment admin
# ---------------------------
@admin.register(FeePayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'receipt_number', 'date')
    list_filter = ('status',)
    actions = ['approve_payments']

    def approve_payments(self, request, queryset):
        for payment in queryset:
            payment.status = 'Approved'
            if not payment.receipt_number:
                payment.receipt_number = f"RCPT-{uuid.uuid4().hex[:8].upper()}"
            payment.save(update_fields=['status', 'receipt_number'])
        self.message_user(request, "Selected payments have been approved and receipt numbers generated.", level=messages.SUCCESS)

    approve_payments.short_description = "Approve selected payments and generate receipt numbers"


# ---------------------------
# Student admin (handles room occupant counts)
# ---------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'year', 'department','address','contact')  # adjust based on fields you have

    def save_model(self, request, obj, form, change):
        """
        When creating or updating a student record, update room occupant counts safely:
         - If changing rooms: decrement old room occupants, increment new room occupants (if capacity allows)
         - If assigning to a room on create: increment new room occupants (if capacity allows)
        """

        new_room = obj.room

        # get old object (if updating)
        old_room = None
        if change and obj.pk:
            try:
                old_obj = Student.objects.get(pk=obj.pk)
                old_room = old_obj.room
            except Student.DoesNotExist:
                old_room = None

        # If the room is changing (or being assigned), check capacity first
        if new_room.occupants >= new_room.capacity:
           messages.error(request, f"Cannot assign: Room {new_room.room_no} is already full.")
           raise ValidationError(f"Room {new_room.room_no} is already full.")



        # Use a transaction to keep counts consistent
        with transaction.atomic():
            # If moving from an old room and it differs from new_room, decrement old room occupant
            if old_room and old_room != new_room:
                old_room.occupants = max(0, old_room.occupants - 1)
                old_room.save(update_fields=['occupants'])

            # If assigning to new_room and it's different from old, increment
            if new_room and (old_room is None or old_room != new_room):
                new_room.occupants = new_room.occupants + 1
                new_room.save(update_fields=['occupants'])

            # Finally save the student object
            super().save_model(request, obj, form, change)


# ---------------------------
# Room Change Request admin
# ---------------------------
@admin.register(RoomChangeRequest)
class RoomChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'requested_room', 'status', 'reason', 'request_date')
    list_filter = ('status',)
    actions = ['approve_request', 'reject_request']

    def approve_request(self, request, queryset):
        """
        Approve selected requests if requested room has capacity.
        This also moves the student from their current room to requested_room
        and updates occupants on both rooms accordingly.
        """
        approved = 0
        rejected = 0
        for req in queryset.select_related('requested_room', 'student__room'):
            target = req.requested_room
            student = req.student
            current = getattr(student, 'room', None)

            if not target:
                req.status = 'Rejected'
                req.save()
                rejected += 1
                continue

            if target.occupants >= target.capacity:
                req.status = 'Rejected'
                req.save()
                rejected += 1
                continue

            # transaction per request
            with transaction.atomic():
                # decrement current room occupants if any and different
                if current and current != target:
                    current.occupants = max(0, current.occupants - 1)
                    current.save(update_fields=['occupants'])

                # assign student to target room
                student.room = target
                student.save(update_fields=['room'])

                # increment target occupants
                target.occupants = target.occupants + 1
                target.save(update_fields=['occupants'])

                req.status = 'Approved'
                req.save()
                approved += 1

        self.message_user(request, f"{approved} request(s) approved, {rejected} request(s) rejected.", level=messages.INFO)

    def reject_request(self, request, queryset):
        updated = queryset.update(status='Rejected')
        self.message_user(request, f"{updated} request(s) rejected.", level=messages.INFO)

    approve_request.short_description = "Approve selected requests"
    reject_request.short_description = "Reject selected requests"


# ---------------------------
# Register other models (no duplicates)
# ---------------------------
admin.site.register(User)
# If both StudentProfile and Student exist keep both; otherwise register the one that exists in your models.py
admin.site.register(StudentProfile)
admin.site.register(Room)
admin.site.register(RoomAllotment)
admin.site.register(Complaint)

# NOTE: Do NOT register FeePayment again here because @admin.register(FeePayment) already registered it above.
