# test_email.py

from send_email_to_substack import send_email_to_substack

send_email_to_substack(
    "WADE TEST: Email Delivery Check",
    "## If you're reading this, WADE can send emails.\n\nThis is a test from GitHub Actions."
)
