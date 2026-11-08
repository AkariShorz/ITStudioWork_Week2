from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivityForm
from .models import Activity


def activity_list(request):
    keyword = request.GET.get("q", "").strip()
    activities = Activity.objects.order_by("start_time")
    if keyword:
        activities = activities.filter(title__icontains=keyword)

    return render(
        request,
        "activities/activity_list.html",
        {"activities": activities, "keyword": keyword},
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


def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    if request.method == "POST":
        activity.delete()
        return redirect("activities:list")

    return render(
        request,
        "activities/activity_confirm_delete.html",
        {"activity": activity},
    )
