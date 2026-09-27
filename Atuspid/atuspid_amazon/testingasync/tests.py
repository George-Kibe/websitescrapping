from unittest import mock

from django.test import TestCase
from django.urls import reverse

from . import views

PAGE = '<article class="product_pod"><h3><a title="A Light in the Attic" href="#">A Light...</a></h3></article>'


class BookViewTests(TestCase):
    def test_book_titles(self):
        self.assertEqual(views.book_titles(PAGE), ["A Light in the Attic"])

    @mock.patch("testingasync.views.fetch", new_callable=mock.AsyncMock, return_value=PAGE)
    def test_books_fetches_every_page(self, fetch):
        response = self.client.get(reverse("async_books"))
        self.assertEqual(fetch.await_count, len(views.BOOK_PAGES))
        self.assertEqual(response.json()[views.BOOK_PAGES[0]], ["A Light in the Attic"])
