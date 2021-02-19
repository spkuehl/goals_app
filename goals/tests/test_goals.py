from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from goals.models import Goal, GoalLog

class GoalTests(APITestCase):
    fixtures = ["user.json", "goal.json", "goal_log.json"]

    def setUp(self):
        self.user = User.objects.get(username='lauren')
        self.user2 = User.objects.get(username='sean')
        self.url_list = reverse('goals-list')

    def test_create_goal(self):
        """
        Ensure we can create a new goal object.
        """
        self.client.force_authenticate(user=self.user)
        pre_test_count = Goal.objects.count()
        data = {
                "check_in_frequency": [],
                "reminder_frequency": [],
                "name": "Practice Chess",
                "active": "true",
                "user": self.user.id
                }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), pre_test_count+1)
        self.assertEqual(Goal.objects.last().name, 'Practice Chess')

    def test_can_not_create_goal_no_auth(self):
        """
        Ensure we can not create a new goal object without authentication.
        """
        pre_test_count = Goal.objects.count()
        data = {
                "check_in_frequency": [],
                "reminder_frequency": [],
                "name": "Practice Chess",
                "active": "true",
                "user": self.user.id
                }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Goal.objects.count(), pre_test_count)

    def test_get_goal(self):
        """
        Ensure we can update a goal object.
        """
        self.client.force_authenticate(user=self.user)
        goal = Goal.objects.filter(user=self.user).last()
        url_detail = reverse('goals-detail', args=[goal.pk])
        response = self.client.get(url_detail)
        updated_goal = Goal.objects.filter(user=self.user).last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_get_goal_no_auth(self):
        """
        Ensure we can not a goal object if no authentication.
        """
        goal = Goal.objects.last()
        url_detail = reverse('goals-detail', args=[goal.pk])
        response = self.client.get(url_detail)
        updated_goal = Goal.objects.filter(user=self.user).last()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_not_get_goal_not_owner(self):
        """
        Ensure we can not a goal object if not goal owner.
        """
        self.client.force_authenticate(user=self.user)
        goal = Goal.objects.filter(user=self.user2).last()
        url_detail = reverse('goals-detail', args=[goal.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_goal(self):
        """
        Ensure we can update a goal object.
        """
        self.client.force_authenticate(user=self.user)
        goal = Goal.objects.filter(user=self.user).last()
        url_detail = reverse('goals-detail', args=[goal.pk])
        data = {
                "name": "Practice piano",
                }
        response = self.client.patch(url_detail, data, format='json')
        updated_goal = Goal.objects.filter(user=self.user).last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(goal.name, updated_goal.name)

    def test_get_goal_list(self):
        """
        Ensure we can get goal object list and it only includes owner.
        """
        self.client.force_authenticate(user=self.user2)
        user_goals = Goal.objects.filter(user=self.user2)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_goals), len(response.data))

    def test_get_goal_log_list_one_goal(self):
        """
        Ensure we can get goal logs for a goal.
        """
        self.client.force_authenticate(user=self.user2)
        goal = Goal.objects.filter(user=self.user2).last()
        goal_log_count_from_db = GoalLog.objects.filter(goal=goal).count()
        url = reverse('goals-goal-log-list', args=[goal.pk])
        response = self.client.get(url, format='json')
        goal_log_count_from_api = len(response.data)
        self.assertEqual(goal_log_count_from_db, goal_log_count_from_api)
