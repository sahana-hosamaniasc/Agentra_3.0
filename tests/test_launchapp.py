import allure
import pytest
from pages.web import login_page
from core.logger import get_logger
from pywinauto.application import Application

logger = get_logger(__name__)

@pytest.mark.flaky(reruns=2, reruns_delay=5)

def test_launchapp(hpApp):

    """
    <Short Test Title>
    <1–2 line summary of what this test validates.>

    Description:
        <High-level description of the business flow under test.>
        <Explain why this test exists and what user scenario it simulates.>

    Test Type:
        <Functional / Regression / Integration / E2E / Smoke / Sanity>

    Preconditions:
        - <List all required pre-state conditions>
        - <User account, device state, environment, network, etc.>
        - <If none, write: None>

    Platforms:
        - Supported: Web / Mobile / Desktop
        - Driven by CLI flag: --platform

    Steps:
        1. <Step 1 description>
        2. <Step 2 description>
        3. <Step 3 description>
        ...
        N. <Final step>

    Expected Result:
        <The exact outcome that must occur for the test to pass>
        <May include UI behavior, API response, state updates, etc.>

    Parameters:
        driver (BaseDriver):
            Platform-agnostic driver instance injected by pytest.
        test_data (dict or tuple):
            Data-driven inputs supplied by JSON/Excel or @pytest.mark.parametrize.

    Tags:
        pytest.mark.<suite>
        pytest.mark.<business_module>
        pytest.mark.<platform>
        pytest.mark.dependency()

    Notes:
        - This test uses the Agentra abstraction layer, so page objects
          automatically adjust based on selected platform.
        - Avoid platform-specific conditions inside the test; those belong
          in Page Objects.

    """    
    
    logger.info(f"Launching the HP Smart Desktop App")

    
    hpApp.launch_app()
    hpApp.create_account()
    # hpApp.start_enrollment()
    # hpApp.enter_shipping_details()
    # hpApp.confirm_enrollment()
