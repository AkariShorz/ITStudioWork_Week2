from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from .models import Activity


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "description", "start_time", "location"]

    def clean_start_time(self):
        start_time = self.cleaned_data["start_time"]
        if start_time < timezone.now():
            raise ValidationError("活动开始时间不能早于当前时间。")
        return start_time
