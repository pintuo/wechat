import datetime
from django.utils import timezone
from polls.models import Question

future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))

future_question.was_published_recently()
