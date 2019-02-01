from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@user.com', password='testpass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """test creating a new user with an email is successfull"""
        email = "testuser@gmail.com"
        password = "testuser123"
        user = get_user_model().objects.create_user(
            email=email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalised"""
        email = 'test@GMAIL.COM'
        user  = get_user_model().objects.create_user(email, 'testuser123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testuser123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'testuser@gmail.com',
            'testuser123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the ingredients string representation"""

        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the corect location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
        
