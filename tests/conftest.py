import os
import pytest
import allure
from dotenv import load_dotenv

from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Load .env automatically
load_dotenv()

def _should_run_local() -> bool:
    return os.getenv("FORCE_LOCAL", "false").lower() == "true" or not os.getenv("SELENOID_HOST", "").strip()

def _build_selenoid_url() -> str:
    protocol = os.getenv("SELENOID_PROTOCOL", "https")
    host = os.getenv("SELENOID_HOST", "selenoid.autotests.cloud")
    port = os.getenv("SELENOID_PORT", "4444")
    login = os.getenv("SELENOID_LOGIN", "").strip()
    password = os.getenv("SELENOID_PASS", "").strip()
    auth = f"{login}:{password}@" if login and password else ""
    return f"{protocol}://{auth}{host}:{port}/wd/hub"

def _video_base() -> str:
    return os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video").rstrip("/")

@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    """Start browser for each test, attach artifacts on failure, then quit."""
    base_url = os.getenv("BASE_URL", "https://demowebshop.tricentis.com")
    timeout = float(os.getenv("SELENE_TIMEOUT", "10"))

    if _should_run_local():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1366,768")

        driver = webdriver.Chrome(options=options)
        browser.config.driver = driver
    else:
        # Selenoid: enable VNC and video
        options = Options()
        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", os.getenv("BROWSER_VERSION", "122.0"))
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True,
            "name": request.node.nodeid,
        })
        # Ask for browser logs where possible
        caps = DesiredCapabilities.CHROME.copy()
        caps["goog:loggingPrefs"] = {"browser": "ALL"}
        for k, v in caps.items():
            options.set_capability(k, v)

        driver = webdriver.Remote(
            command_executor=_build_selenoid_url(),
            options=options
        )
        browser.config.driver = driver

    browser.config.base_url = base_url
    browser.config.timeout = timeout

    yield

    # Attach artifacts on failure
    rep = getattr(request.node, "rep_call", None)
    failed = rep and rep.failed
    try:
        if failed:
            try:
                png = browser.driver.get_screenshot_as_png()
                allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
            try:
                html = browser.driver.page_source
                allure.attach(html, name="page_source", attachment_type=allure.attachment_type.HTML)
            except Exception:
                pass
            try:
                logs = browser.driver.get_log("browser")
                allure.attach(str(logs), name="browser_console_logs", attachment_type=allure.attachment_type.TEXT)
            except Exception:
                pass
            try:
                session_id = browser.driver.session_id
                video_url = f"{_video_base()}/{session_id}.mp4"
                html = f'<html><body><video width="100%" height="100%" controls autoplay><source src="{video_url}" type="video/mp4"></video></body></html>'
                allure.attach(html, name="video", attachment_type=allure.attachment_type.HTML)
            except Exception:
                pass
    finally:
        try:
            browser.quit()
        except Exception:
            pass

# Hook to populate request.node.rep_call / rep_setup / rep_teardown
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# === ALWAYS ATTACH ARTIFACTS (added) ===
import allure as _allure_internal_ref
from selene import browser as _browser_internal_ref
import os, pytest

def _video_base() -> str:
    return os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video").rstrip("/")

@pytest.fixture(autouse=True)
def _always_attach_artifacts():
    yield
    try:
        try:
            png = _browser_internal_ref.driver.get_screenshot_as_png()
            _allure_internal_ref.attach(png, name="screenshot", attachment_type=_allure_internal_ref.attachment_type.PNG)
        except Exception:
            pass
        try:
            src = _browser_internal_ref.driver.page_source
            _allure_internal_ref.attach(src, name="page_source", attachment_type=_allure_internal_ref.attachment_type.HTML)
        except Exception:
            pass
        try:
            logs = _browser_internal_ref.driver.get_log("browser")
            text = "\n".join(f"[{x.get('level')}] {x.get('message')}" for x in logs)
            _allure_internal_ref.attach(text or "(no console logs)", name="browser_logs", attachment_type=_allure_internal_ref.attachment_type.TEXT)
        except Exception:
            pass
        try:
            session_id = _browser_internal_ref.driver.session_id
            video_url = f"{_video_base()}/{session_id}.mp4"
            html = f'<html><body style="margin:0;"><video width="100%" controls><source src="{video_url}" type="video/mp4"></video></body></html>'
            _allure_internal_ref.attach(html, name="video", attachment_type=_allure_internal_ref.attachment_type.HTML)
        except Exception:
            pass
    except Exception:
        pass
