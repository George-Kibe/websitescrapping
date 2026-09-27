import logging
import threading

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .scraper import JOBS, Browser, TelegramSender

log = logging.getLogger(__name__)

JOB_LABELS = {
    "coupons": "Coupons",
    "daily-deals": "Today's deals",
    "multiple-deals": "Discounted search results",
}


def home(request):
    return render(request, "offersapp/home.html", {"jobs": JOB_LABELS})


def _run_job(job_name: str) -> None:
    """Run one scraping job; executed on a background thread."""
    sender = TelegramSender(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)
    try:
        with Browser() as browser:
            JOBS[job_name](browser, sender)
    except Exception:
        log.exception("Job %s failed", job_name)


def start_job(job_name: str) -> None:
    # Scraping and posting take minutes (the sender pauses between messages),
    # so run it off the request thread and respond straight away.
    threading.Thread(target=_run_job, args=(job_name,), name=f"job-{job_name}", daemon=True).start()


@require_POST
def run_job(request, job_name):
    if job_name not in JOBS:
        raise Http404("Unknown job")
    if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
        messages.error(request, "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID before running jobs.")
        return redirect("home")

    start_job(job_name)
    messages.success(request, f"{JOB_LABELS[job_name]}: checking Amazon and sending results to Telegram.")
    return redirect("home")
