from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import sign_up, logout_view, profile, update_username, update_email, change_password
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, UpdateUsername, UpdateEmail, ChangePasswordForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.test.client import RequestFactory


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

    def test_profile_url(self):
        self.assertEqual(resolve(self.profile_url).func, profile)

    def test_update_username_url(self):
        self.assertEqual(resolve(self.update_username_url).func, update_username)

    def test_update_email_url(self):
        self.assertEqual(resolve(self.update_email_url).func, update_email)

    def test_reset_password_url(self):
        self.assertEqual(resolve(self.reset_password_url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url(self):
        self.assertEqual(resolve(self.password_reset_done_url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url(self):
        self.assertEqual(resolve(self.password_reset_confirm_url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url(self):
        self.assertEqual(resolve(self.password_reset_complete_url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_change_password_url(self):
        self.assertEqual(resolve(self.change_password_url).func, change_password)


class AccountsFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='password123')
        self.factory = RequestFactory()

    def test_register_valid_form(self):
        form_data = {
            'username': 'testformusername',
            'email': 'testformemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        form = RegisterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_register_invalid_form(self):
        form_data = {
            'username': '',
            'email': 'testformemail',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_username_valid_form(self):
        form_data = {
            'username': 'testformusername'
        }
        form = UpdateUsername(form_data)

        self.assertTrue(form.is_valid())

    def test_update_username_invalid_form(self):
        form_data = {
            'username': ''
        }
        form = UpdateUsername(form_data)

        self.assertFalse(form.is_valid())

    def test_update_email_valid_form(self):
        form_data = {
            'email': 'testformemail@gmail.com'
        }
        form = UpdateEmail(form_data)

        self.assertTrue(form.is_valid())

    def test_update_email_invalid_form(self):
        form_data = {
            'email': 'testformemail'
        }
        form = UpdateEmail(form_data)

        self.assertFalse(form.is_valid())

    def test_change_password_valid_form(self):
        request = self.factory.get('/')
        request.user = self.user
        form_data = {
            'oldpassword': 'password123',
            'newpassword1': 'testnewpassword',
            'newpassword2': 'testnewpassword'
        }
        form = ChangePasswordForm(form_data, request=request)

        self.assertTrue(form.is_valid())

    def test_change_password_form_invalid_old_password(self):
        request = self.factory.get('/')
        request.user = self.user
        form_data = {
            'oldpassword': 'invalidpassword',
            'newpassword1': 'testnewpassword',
            'newpassword2': 'testnewpassword'
        }
        form = ChangePasswordForm(form_data, request=request)

        self.assertFalse(form.is_valid())

    def test_change_password_form_invalid_confirm_password(self):
        request = self.factory.get('/')
        request.user = self.user
        form_data = {
            'oldpassword': 'password123',
            'newpassword1': 'testnewpassword1',
            'newpassword2': 'testnewpassword2'
        }
        form = ChangePasswordForm(form_data, request=request)

        self.assertFalse(form.is_valid())


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='password123')
        self.client = Client()
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.change_password_url = reverse('change_password')
        self.update_username_url = reverse('update_username')
        self.update_email_url = reverse('update_email')

    def test_signup_post(self):
        data_register_form = {
            'username': 'testsignup',
            'email': 'testsignupemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        response = self.client.post(self.signup_url, data={
            **data_register_form
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testsignup').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, '/')

    def test_signup_get(self):
        response = self.client.get(self.signup_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('registration/signup.html')

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.logout_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, '/login/?next=%2F')

    def test_change_password_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.change_password_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_change_password_post_valid_form(self):
        self.client.login(username='testuser', password='password123')
        test_form_data = {
            'oldpassword': 'password123',
            'newpassword1': 'testnewpassword',
            'newpassword2': 'testnewpassword'
        }
        response = self.client.post(self.change_password_url, data=test_form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser')[0].check_password("testnewpassword"))
        self.assertRedirects(response, '/login/?next=%2F')

    def test_change_password_post_invalid_old_password_form(self):
        self.client.login(username='testuser', password='password123')
        test_form_data = {
            'oldpassword': 'invalidoldpassword',
            'newpassword1': 'testnewpassword',
            'newpassword2': 'testnewpassword'
        }
        response = self.client.post(self.change_password_url, data=test_form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_change_password_post_invalid_new_password_same_as_old_form(self):
        self.client.login(username='testuser', password='password123')
        test_form_data = {
            'oldpassword': 'password123',
            'newpassword1': 'password123',
            'newpassword2': 'password123'
        }
        response = self.client.post(self.change_password_url, data=test_form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_update_username_post_valid_form(self):
        self.client.login(username='testuser', password='password123')
        test_data = {
            'username': 'testupdateusername'
        }
        response = self.client.post(self.update_username_url, data=test_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testupdateusername').exists())
        self.assertRedirects(response, '/profile/')

    def test_update_username_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.update_username_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_username.html')
        self.assertIn('form', response.context)

    def test_update_email_post_valid_form(self):
        self.client.login(username='testuser', password='password123')
        test_data = {
            'email': 'testupdateemail@gmail.com'
        }
        response = self.client.post(self.update_email_url, data=test_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='testupdateemail@gmail.com').exists())
        self.assertRedirects(response, '/profile/')

    def test_update_email_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.update_email_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_email.html')
        self.assertIn('form', response.context)