from django.contrib import admin
from .models import Question, Choice, Response, Answer, Participant

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(Answer)
admin.site.register(Participant)
