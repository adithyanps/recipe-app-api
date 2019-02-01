from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer,TagDetailSerializer

TAGS_URL =reverse('recipe:tag-list')

def detail_url(tag_id):
    """Return tag detail URL"""
    return reverse('recipe:tag-detail', args=[tag_id])

def sample_tag(user, **params):
    """Create and return a sample tag"""
    defaults = {
        'name':'sample tag',

    }
    defaults.update(params)

    return Tag.objects.create(user=user, **defaults)


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retreiving tags"""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the autherized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@user.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # def test_retrieve_tags(self):
    #     """test retrieving tags"""
    #     Tag.objects.create(user=self.user, name='Vegan')
    #     Tag.objects.create(user=self.user, name='Dessert')
    #
    #     res = self.client.get(TAGS_URL)
    #
    #     tags = Tag.objects.all().order_by('-name')
    #     serializer = TagSerializer(tags, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""

        user2 = get_user_model().objects.create_user(
            'other@user.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='comfort food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""

        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_tag_detail(self):
        """Test viewing a tag detail"""
        tag = sample_tag(user=self.user)

        url = detail_url(tag.id)
        res = self.client.get(url)

        serializer = TagDetailSerializer(tag)
        self.assertEqual(res.data, serializer.data)
