"""Taurus AI v4 - Entry point for Hugging Face Spaces + Streamlit Cloud.

Run locally: streamlit run app.py
This imports the real Streamlit UI in app/streamlit_app_v4.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importing this file runs the Streamlit UI (it has top-level Streamlit code)
import app.streamlit_app_v4  # noqa: F401
