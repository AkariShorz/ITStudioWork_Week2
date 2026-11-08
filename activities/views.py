from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivityForm
from .models import Activity


def activity_list(request):
    activities = Activity.objects.order_by("start_time")
    return render(
        request,
        "activities/activity_list.html",
        {"activities": activities},
    )


def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("activities:list")
    else:
        form = ActivityForm(instance=activity)

    return render(
        request,
        "activities/activity_form.html",
        {"form": form, "activity": activity},
    )
