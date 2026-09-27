from unittest import mock

from bs4 import BeautifulSoup
from django.test import TestCase, override_settings
from django.urls import reverse

from .scraper import next_page_url, parse_coupons, parse_search_results


class ParserTests(TestCase):
    def test_parse_coupons(self):
        soup = BeautifulSoup(
            """
            <div class="coupon" data-promoid="ABC">
              <div class="coupon-description">Desk lamp</div>
              <img class="coupon-image" src="https://img/1.jpg">
              <span class="a-color-success">Save $5</span>
            </div>
            """,
            "lxml",
        )
        [deal] = parse_coupons(soup)
        self.assertEqual(deal.link, "https://www.amazon.com/promotion/psp/ABC")
        self.assertIn("Coupon: $5", deal.details)

    def test_parse_search_results(self):
        soup = BeautifulSoup(
            """
            <div data-component-type="s-search-result">
              <h2><a href="/dp/X">Keyboard</a></h2><img class="s-image" src="https://img/2.jpg">
              <span class="a-price"><span class="a-offscreen">$20.00</span></span>
            </div>
            """,
            "lxml",
        )
        [deal] = parse_search_results(soup)
        self.assertEqual(deal.title, "Keyboard")
        self.assertIsNone(next_page_url(soup))


@override_settings(TELEGRAM_BOT_TOKEN="token", TELEGRAM_CHAT_ID="-1")
class ViewTests(TestCase):
    def test_home_lists_jobs(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("run_job", args=["daily-deals"]))
        self.assertContains(response, "csrfmiddlewaretoken")

    @mock.patch("offersapp.views.start_job")
    def test_run_job_starts_in_background_and_redirects(self, start_job):
        response = self.client.post(reverse("run_job", args=["coupons"]), follow=True)
        start_job.assert_called_once_with("coupons")
        self.assertRedirects(response, reverse("home"))
        self.assertContains(response, "sending results to Telegram")

    def test_run_job_requires_post(self):
        self.assertEqual(self.client.get(reverse("run_job", args=["coupons"])).status_code, 405)

    def test_unknown_job_is_404(self):
        self.assertEqual(self.client.post(reverse("run_job", args=["nope"])).status_code, 404)

    @override_settings(TELEGRAM_BOT_TOKEN="")
    @mock.patch("offersapp.views.start_job")
    def test_missing_telegram_config_shows_error(self, start_job):
        response = self.client.post(reverse("run_job", args=["coupons"]), follow=True)
        start_job.assert_not_called()
        self.assertContains(response, "Set TELEGRAM_BOT_TOKEN")
