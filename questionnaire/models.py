from django.db import models
import uuid
from django.contrib.auth.models import User

# ✅ 1️⃣ Survey goes FIRST so it’s defined for others to use
class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# ✅ 2️⃣ Participant
class Participant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        default='Other'
    )
    contact_info = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ✅ 3️⃣ Question
class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    QUESTION_TYPES = [
        ('text', 'Text'),
        ('date', 'Date'),
        ('number', 'Number'),
        ('radio', 'Single Choice'),
        ('checkbox', 'Multiple Choice'),
    ]
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


# ✅ 4️⃣ Choice
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question.text} → {self.text}"


# ✅ 5️⃣ Response
class Response(models.Model):
    participant = models.ForeignKey(
        Participant,
        related_name='responses',
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        Survey,  # ← Survey is now defined above
        related_name='responses',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.participant.name} ({self.created_at.date()})"


# ✅ 6️⃣ Answer
class Answer(models.Model):
    response = models.ForeignKey(
        Response,
        related_name='answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    answer_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer to '{self.question.text}'"


# ✅ 7️⃣ AssessorRequest
class AssessorRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    reason = models.TextField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Approved: {self.approved} - Declined: {self.declined}"
