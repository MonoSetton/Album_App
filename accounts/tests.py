from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import sign_up, logout_view
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


class AccountsUrlsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='password123')
        self.token = default_token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.update_username_url = reverse('update_username')
        self.update_email_url = reverse('update_email')
        self.reset_password_url = reverse('reset_password')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_confirm_url = reverse('password_reset_confirm', args=[self.uidb64, self.token])
        self.password_reset_complete_url = reverse('password_reset_complete')
        self.change_password_url = reverse('change_password')

    def test_signup_url(self):
        self.assertEqual(resolve(self.signup_url).func, sign_up)

    def test_logout_url(self):
        self.assertEqual(resolve(self.logout_url).func, logout_view)