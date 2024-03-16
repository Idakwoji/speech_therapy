# create_dummy_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.models import Admin, Therapist, Assistant, Client, UserProfile

class Command(BaseCommand):
    help = 'Creates dummy users for testing purposes'

    def handle(self, *args, **kwargs):
        # Create dummy therapists
        admin_user = User.objects.create_user(username="mootje2000", password="BlueSky789")
        admin_profile = UserProfile.objects.create(user=admin_user, is_admin=True)
        Admin.objects.create(user_profile=admin_profile)
        
        therapist1_user = User.objects.create_user(username='therapist1', password='password123')
        therapist1_profile = UserProfile.objects.create(user=therapist1_user, is_therapist=True)
        therapist1 = Therapist.objects.create(user_profile=therapist1_profile)

        assistant1_therapist1_user = User.objects.create_user(username="assistant1_1", password='password123')
        assistant1_therapist1_profile = UserProfile.objects.create(user=assistant1_therapist1_user, is_assistant=True)
        assistant1_1 = Assistant.objects.create(user_profile=assistant1_therapist1_profile, therapist=therapist1)

        assistant2_therapist1_user = User.objects.create_user(username="assistant2_1", password='password123')
        assistant2_therapist1_profile = UserProfile.objects.create(user=assistant2_therapist1_user, is_assistant=True)
        assistant2_1 = Assistant.objects.create(user_profile=assistant2_therapist1_profile, therapist=therapist1)

        therapist2_user = User.objects.create_user(username='therapist2', password='password123')
        therapist2_profile = UserProfile.objects.create(user=therapist2_user, is_therapist=True)
        therapist2 = Therapist.objects.create(user_profile=therapist2_profile)

        assistant1_therapist2_user = User.objects.create_user(username="assistant1_2", password='password123')
        assistant1_therapist2_profile = UserProfile.objects.create(user=assistant1_therapist2_user, is_assistant=True)
        assistant1_2 = Assistant.objects.create(user_profile=assistant1_therapist2_profile, therapist=therapist2)

        assistant2_therapist2_user = User.objects.create_user(username="assistant2_2", password='password123')
        assistant2_therapist2_profile = UserProfile.objects.create(user=assistant2_therapist2_user, is_assistant=True)
        assistant2_2 = Assistant.objects.create(user_profile=assistant2_therapist2_profile, therapist=therapist2)

        therapist3_user = User.objects.create_user(username='therapist3', password='password123')
        therapist3_profile = UserProfile.objects.create(user=therapist3_user, is_therapist=True)
        therapist3 = Therapist.objects.create(user_profile=therapist3_profile)

        assistant1_therapist3_user = User.objects.create_user(username="assistant1_3", password='password123')
        assistant1_therapist3_profile = UserProfile.objects.create(user=assistant1_therapist3_user, is_assistant=True)
        assistant1_3 = Assistant.objects.create(user_profile=assistant1_therapist3_profile, therapist=therapist3)

        assistant2_therapist3_user = User.objects.create_user(username="assistant2_3", password='password123')
        assistant2_therapist3_profile = UserProfile.objects.create(user=assistant2_therapist3_user, is_assistant=True)
        assistant2_3 = Assistant.objects.create(user_profile=assistant2_therapist3_profile, therapist=therapist3)

        # Create dummy clients linked to therapists
        client1_user = User.objects.create_user(username='client1', password='password123')
        client1_profile = UserProfile.objects.create(user=client1_user, is_client=True)
        Client.objects.create(user_profile=client1_profile, assigned_therapist=therapist1, assigned_assistant=assistant1_1)

        client2_user = User.objects.create_user(username='client2', password='password123')
        client2_profile = UserProfile.objects.create(user=client2_user, is_client=True)
        Client.objects.create(user_profile=client2_profile, assigned_therapist=therapist1, assigned_assistant=assistant2_1)

        client3_user = User.objects.create_user(username='client3', password='password123')
        client3_profile = UserProfile.objects.create(user=client3_user, is_client=True)
        Client.objects.create(user_profile=client3_profile, assigned_therapist=therapist1, assigned_assistant=assistant2_1)
        
        client4_user = User.objects.create_user(username='client4', password='password123')
        client4_profile = UserProfile.objects.create(user=client4_user, is_client=True)
        Client.objects.create(user_profile=client4_profile, assigned_therapist=therapist2, assigned_assistant=assistant1_2)
        
        client5_user = User.objects.create_user(username='client5', password='password123')
        client5_profile = UserProfile.objects.create(user=client5_user, is_client=True)
        Client.objects.create(user_profile=client5_profile, assigned_therapist=therapist2, assigned_assistant=assistant2_2)
        
        client6_user = User.objects.create_user(username='client6', password='password123')
        client6_profile = UserProfile.objects.create(user=client6_user, is_client=True)
        Client.objects.create(user_profile=client6_profile, assigned_therapist=therapist3, assigned_assistant=assistant1_3)
        
        client7_user = User.objects.create_user(username='client7', password='password123')
        client7_profile = UserProfile.objects.create(user=client7_user, is_client=True)
        Client.objects.create(user_profile=client7_profile, assigned_therapist=therapist3)

