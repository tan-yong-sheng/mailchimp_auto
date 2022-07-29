from mailchimp_auto import __version__
import pytest
from mailchimp_auto.scripts.gspread_data import connect_google
import os

def test_version():
    assert __version__ == '0.1.0'

def test_connect_google():
    connect_google()
