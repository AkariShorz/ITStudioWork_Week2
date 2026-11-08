from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Activity


class ActivityPageTests(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            title="合唱排练",
            description="测试活动简介",
            start_time=timezone.now() + timedelta(days=2),
            location="活动室",
        )

    def test_activity_list_searches_titles(self):
        Activity.objects.create(
            title="机器人分享会",
            description="另一个活动",
            start_time=timezone.now() + timedelta(days=3),
            location="实验室",
        )

        response = self.client.get(reverse("activities:list"), {"q": "  合唱  "})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "合唱排练")
        self.assertNotContains(response, "机器人分享会")

    def test_activity_can_be_edited_with_model_form(self):
        new_start_time = timezone.now() + timedelta(days=5)

        response = self.client.get(
            reverse("activities:edit", args=[self.activity.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "合唱排练")

        response = self.client.post(
            reverse("activities:edit", args=[self.activity.pk]),
            {
                "title": "合唱团彩排",
                "description": "修改后的简介",
                "start_time": new_start_time.isoformat(),
                "location": "礼堂",
            },
        )

        self.assertRedirects(response, reverse("activities:list"))
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.title, "合唱团彩排")
        self.assertEqual(self.activity.description, "修改后的简介")
        self.assertEqual(self.activity.location, "礼堂")

    def test_past_start_time_is_rejected(self):
        past_start_time = timezone.now() - timedelta(days=1)

        response = self.client.post(
            reverse("activities:edit", args=[self.activity.pk]),
            {
                "title": "合唱排练",
                "description": "测试活动简介",
                "start_time": past_start_time.isoformat(),
                "location": "活动室",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "活动开始时间不能早于当前时间。")
        self.activity.refresh_from_db()
        self.assertNotEqual(self.activity.start_time.date(), past_start_time.date())

    def test_activity_delete_requires_confirmation(self):
        delete_url = reverse("activities:delete", args=[self.activity.pk])

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "合唱排练")
        self.assertTrue(Activity.objects.filter(pk=self.activity.pk).exists())

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("activities:list"))
        self.assertFalse(Activity.objects.filter(pk=self.activity.pk).exists())
