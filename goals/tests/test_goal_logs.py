from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from goals.models import Goal, GoalLog

class GoalLogTests(APITestCase):
    fixtures = ["user.json", "goal.json", "goal_log.json"]

    def setUp(self):
        self.user = User.objects.get(username='sean')
        self.url = reverse('goal-logs-list')

    def test_create_goal_log(self):
        """
        Ensure we can create a new goal log object.
        """
        self.client.force_authenticate(user=self.user)
        goal = Goal.objects.filter(user=self.user).last()
        pre_test_log_count = GoalLog.objects.filter(goal=goal).count()
        data = {
                "goal": goal.pk,
                "date_added": "2021-02-08",
                "duration": 90,
                "notes": ""
                }
        response = self.client.post(self.url, data, format='json')
        post_test_log_count = GoalLog.objects.filter(goal=goal).count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(pre_test_log_count+1, post_test_log_count)


    def test_can_not_create_goal_not_authenticated(self):
        """
        Ensure we can not create a new goal log object without authentication.
        """
        goal = Goal.objects.filter(user=self.user).last()
        pre_test_log_count = GoalLog.objects.filter(goal=goal).count()
        data = {
                "goal": goal.pk,
                "date_added": "2021-02-08",
                "duration": 90,
                "notes": ""
                }
        response = self.client.post(self.url, data, format='json')
        post_test_log_count = GoalLog.objects.filter(goal=goal).count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(pre_test_log_count, post_test_log_count)

    def test_get_goal_log(self):
        """
        Ensure we can get a goal log object.
        """
        self.client.force_authenticate(user=self.user)
        goal_log = GoalLog.objects.filter(goal__user=self.user).last()
        url_detail = reverse('goal-logs-detail', args=[goal_log.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_can_not_get_goal_log_no_auth(self):
        """
        Ensure you need to log in to use this api.
        """
        goal_log = GoalLog.objects.filter(goal__user=self.user).last()
        url_detail = reverse('goal-logs-detail', args=[goal_log.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_cant_not_get_goal_log_not_owner(self):
        """
        Ensure goal logs are private, you must be owner or admin to access.
        """
        self.client.force_authenticate(user=self.user)
        not_user = User.objects.get(username='lauren')
        goal_log = GoalLog.objects.filter(goal__user=not_user).last()
        url_detail = reverse('goal-logs-detail', args=[goal_log.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_goal_log(self):
        """
        Test can update a goal log.
        """
        self.client.force_authenticate(user=self.user)
        goal_log = GoalLog.objects.filter(goal__user=self.user).last()
        url_detail = reverse('goal-logs-detail', args=[goal_log.pk])
        data = {
                "notes": "new note"
                }
        response = self.client.patch(url_detail, data, format='json')
        updated_goal_log = GoalLog.objects.filter(goal__user=self.user).last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(goal_log.notes, updated_goal_log.notes)

    def test_get_goal_log_list(self):
        """
        Ensure we can get goal log object list and it only includes owner.
        """
        self.client.force_authenticate(user=self.user)
        user_goal_logs = GoalLog.objects.filter(goal__user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_goal_logs), len(response.data))

    def test_get_goal_log_list_for_one_goal(self):
        """
        Ensure we can goal log object list for a specific goal.
        """
        pass
