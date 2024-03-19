from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import home, upload_image, delete_image, image_details, add_comment, delete_comment
from .models import Category, Image, Comment
from .forms import ImageUploadForm, CommentForm
from django.http import JsonResponse


class ImagesUrlsTestCase(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.upload_image_url = reverse('upload_image')
        self.delete_image_url = reverse('delete_image', args=['1'])
        self.image_details_url = reverse('image_details', args=['1'])
        self.add_comment_url = reverse('add_comment', args=['1'])
        self.delete_comment_url = reverse('delete_comment', args=['1'])

    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).func, home)

    def test_upload_image_url(self):
        self.assertEqual(resolve(self.upload_image_url).func, upload_image)

    def test_delete_image_url(self):
        self.assertEqual(resolve(self.delete_image_url).func, delete_image)

    def test_image_details_url(self):
        self.assertEqual(resolve(self.image_details_url).func, image_details)

    def test_add_comment_url(self):
        self.assertEqual(resolve(self.add_comment_url).func, add_comment)

    def test_delete_comment_url(self):
        self.assertEqual(resolve(self.delete_comment_url).func, delete_comment)


class ImagesModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                                         email='test@example.com',
                                                         password='password123')
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2')
        self.image = Image.objects.create(name='Test Image', image='TestImage.png', author=self.user)
        self.image.category.add(self.category1)
        self.image.category.add(self.category2)
        self.comment = Comment.objects.create(body='Test Comment', image=self.image, author=self.user)

    def test_category_model(self):
        self.assertEqual(str(self.category1), 'Test Category 1')
        self.assertEqual(str(self.category2), 'Test Category 2')

    def test_image_model(self):
        self.assertEqual(str(self.image), 'Test Image')

    def test_comment_model(self):
        self.assertEqual(str(self.comment), 'Test Comment')


class ImagesFormsTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_comment_form(self):
        form_data = {
            'body': 'Test Comment'
        }
        form = CommentForm(data=form_data)

        self.assertTrue(form.is_valid())


class ImagesViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='password123')
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2')
        self.image = Image.objects.create(name='Test Image', image='TestImage.png', author=self.user)
        self.image.category.add(self.category1)
        self.image.category.add(self.category2)
        self.comment = Comment.objects.create(body='Test Comment', image=self.image, author=self.user)
        self.client = Client()
        self.home_url = reverse('home')
        self.upload_image_url = reverse('upload_image')
        self.delete_image_url = reverse('delete_image', args=[self.image.id])
        self.image_details_url = reverse('image_details', args=[self.image.id])
        self.add_comment_url = reverse('add_comment', args=[self.comment.id])
        self.delete_comment_url = reverse('delete_comment', args=[self.comment.id])

    def test_home(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.home_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('images', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('search_filter', response.context)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('images/home.html')

    # def test_upload_image_post(self):
    #     self.client.login(username='testuser', password='password123')
    #     response = self.client.post(reverse('upload_image'), format='multipart')
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Image.objects.filter(name='Test Upload Image').exists())
    #     self.assertTrue(Image.objects.filter(name='Test Upload Image')[0].author == self.user)


    def test_upload_image_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.upload_image_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('images/upload_image.html')

    def test_delete_image_post_valid_author(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.delete_image_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Image.objects.filter(name='Test Image').exists())
        self.assertRedirects(response, '/profile/')

    def test_delete_image_post_invalid_author(self):
        self.client.login(username='testuser1', password='password123')
        response = self.client.post(self.delete_image_url, follow=True)

        self.assertEqual(response.status_code, 400)

    def test_delete_image_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.delete_image_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('image', response.context)
        self.assertTemplateUsed(response, 'images/delete_image.html')

    def test_image_details(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.image_details_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('image', response.context)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'images/image_details.html')

    def test_add_comment_post(self):
        self.client.login(username='testuser', password='password123')
        data_comment = {
            'body': 'Test Add Comment',
        }
        response = self.client.post(reverse('add_comment', kwargs={'pk': self.image.id}),
                                    data={
                                        **data_comment
                                    }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(body='Test Add Comment').exists())
        self.assertTrue(Comment.objects.filter(body='Test Add Comment')[0].author == self.user)
        self.assertTrue(Comment.objects.filter(body='Test Add Comment')[0].image == self.image)

    def test_add_comment_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.add_comment_url, follow=True)

        expected_response = JsonResponse({'error': 'Invalid form submission'})
        self.assertEqual(response.content, expected_response.content)

    def test_delete_comment(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.delete_comment_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(body='Test Comment').exists())