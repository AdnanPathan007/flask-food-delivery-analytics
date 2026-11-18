# Food Delivery Web App

A Flask-based food delivery demo with a menu, shopping cart, checkout, and order confirmation pages. The app also records clickstream events and can publish them to Google Cloud Pub/Sub.

## Features

- Browse the food menu
- Add items to a cart and proceed through checkout
- Record click events with a server timestamp
- Enrich events with approximate IP-based location data using ipinfo.io
- Send events to a Google Cloud Pub/Sub topic

> This project is a learning/demo application. Review its privacy, security, and payment handling before using it with real customers.

## Tech stack

- Python and Flask
- HTML templates and JavaScript
- Google Cloud Pub/Sub
- ipinfo.io for approximate IP geolocation

## Requirements

- Python 3.10 or newer
- A Google Cloud project with Pub/Sub enabled, if clickstream publishing is required
- A Pub/Sub topic and credentials with permission to publish to that topic

## Run locally

1. Clone this repository and open its project directory:

   ```bash
   git clone https://github.com/AdnanPathan007/flask-food-delivery-analytics.git
   cd flask-food-delivery-analytics
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure Google Cloud credentials as described below, then start Flask:

   ```bash
   python app.py
   ```

5. Open <http://127.0.0.1:5000> in your browser.

## Google Cloud Pub/Sub configuration

The publisher is configured for a Google Cloud Pub/Sub topic. Do not commit service-account JSON keys or other credentials to GitHub.

For local development, set `GOOGLE_APPLICATION_CREDENTIALS` to the path of a service-account credential file kept outside the repository. The service account should have only the permissions needed to publish to the configured topic. Update the topic setting in `publisher/config.py` to match your own project and topic.

If Pub/Sub is not configured, click-event publishing may fail. The storefront pages can still be explored, but the `/log_click` feature requires valid Pub/Sub access.

## Deploy online

GitHub hosts this source repository. GitHub Pages cannot run a Flask/Python server because it publishes static files only. To make this app available as a live Flask website, deploy the GitHub repository to a Python web host such as Render.

Typical Render settings:

- **Root directory:** the directory containing `app.py` and `requirements.txt`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

Add `gunicorn` to `requirements.txt` before deploying. Confirm `requirements.txt` is saved as UTF-8 text; the supplied ZIP contains a UTF-16 version, which may need conversion before `pip install -r requirements.txt` works. Configure Google Cloud credentials and the Pub/Sub topic as protected host secrets/settings; never upload the service-account JSON key to the repository. The app's current publisher configuration uses a local `jsonkey.json` path, so update it to use the host's secret-file path or an environment-based credential setup before enabling Pub/Sub in production.

## Project structure

```text
app.py                 Flask routes
publisher/             Google Cloud Pub/Sub publisher
static/                Browser-side JavaScript
templates/              HTML pages
 data/                  Sample clickstream data
requirements.txt        Python dependencies
```

## Privacy note

The click logging route stores an IP address and attempts to infer its approximate location through ipinfo.io. Tell users what is collected, why it is collected, and how long it is retained before using this beyond a local demo. Avoid logging personal or payment information.

