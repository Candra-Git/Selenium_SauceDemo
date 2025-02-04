import pytest
import os

REPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../reports"))
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_screenshots"))

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Saves screenshots in case of errors and adds the report to pytest-html."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_name = f"screenshot_failed_{item.name}.png"
            screenshot_path = os.path.join("SCREENSHOT_DIR", screenshot_name)
            driver.save_screenshot(screenshot_path)

            if hasattr(report, "extra"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    report.extra.append(pytest_html.extras.image(screenshot_path))
