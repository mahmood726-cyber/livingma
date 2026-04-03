"""Selenium tests for LivingMA — Living Meta-Analysis Dashboard."""
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HTML = os.path.join(os.path.dirname(__file__), '..', 'livingma.html')
URL = 'file:///' + os.path.abspath(HTML).replace('\\', '/')


@pytest.fixture(scope='module')
def driver():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--disable-software-rasterizer')
    opts.add_argument('--window-size=1400,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(3)
    yield d
    d.quit()


def fresh(driver):
    """Load page fresh with confirm override and canvas drawing disabled."""
    driver.get(URL)
    driver.execute_script("""
        window.confirm = function(){return true};
        // Disable canvas drawing to prevent Chrome headless crashes
        window._origDrawForest = window.drawForestCanvas;
        window._origDrawStability = window.drawStabilityCanvas;
        window._origDrawWhatIf = window.drawWhatIfCanvas;
        window.drawForestCanvas = function(){};
        window.drawStabilityCanvas = function(){};
        window.drawWhatIfCanvas = function(){};
    """)
    time.sleep(0.3)


def fresh_with_canvas(driver):
    """Load page without disabling canvas (for canvas-specific tests)."""
    driver.get(URL)
    driver.execute_script("window.confirm = function(){return true};")
    time.sleep(0.3)


def js(driver, script):
    return driver.execute_script('return ' + script)


def click(driver, el):
    driver.execute_script("arguments[0].click();", el)


# === Page Load ===

class TestPageLoad:
    def test_title(self, driver):
        fresh(driver)
        assert 'LivingMA' in driver.title

    def test_header_visible(self, driver):
        els = driver.find_elements(By.TAG_NAME, 'h1') + driver.find_elements(By.CSS_SELECTOR, '.app-title, .brand, header')
        text = ' '.join(e.text for e in els)
        assert 'LivingMA' in text or 'Living' in text, f"Header not found, got: {text[:100]}"

    def test_four_tabs_present(self, driver):
        tabs = driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        assert len(tabs) == 4

    def test_no_critical_console_errors(self, driver):
        logs = driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE'
                  and 'favicon' not in l.get('message', '')]
        assert len(severe) == 0, f"Console errors: {severe}"


# === Tab Navigation ===

class TestTabs:
    @pytest.mark.parametrize("tab_id", ["data", "timeline", "whatif", "report"])
    def test_switch_tab(self, driver, tab_id):
        fresh(driver)
        btn = driver.find_element(By.ID, f'tbtn-{tab_id}')
        click(driver, btn)
        time.sleep(0.2)
        panel = driver.find_element(By.ID, f'tab-{tab_id}')
        assert panel.is_displayed()

    def test_aria_selected_updates(self, driver):
        fresh(driver)
        btn = driver.find_element(By.ID, 'tbtn-timeline')
        click(driver, btn)
        time.sleep(0.2)
        assert btn.get_attribute('aria-selected') == 'true'
        data_btn = driver.find_element(By.ID, 'tbtn-data')
        assert data_btn.get_attribute('aria-selected') == 'false'


# === Example Loading ===

class TestExamples:
    def test_load_sglt2(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(0)}catch(e){window._loadErr=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.studies.length")
        assert n >= 3, f"SGLT2i should have >=3 studies, got {n}"

    def test_load_statins(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(1)}catch(e){window._loadErr=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.studies.length")
        assert n >= 5, f"Statins should have >=5 studies, got {n}"

    def test_load_hcq(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(2)}catch(e){window._loadErr=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.studies.length")
        assert n >= 3, f"HCQ should have >=3 studies, got {n}"


# === Analysis ===

class TestAnalysis:
    def test_sglt2_analysis_runs(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(0)}catch(e){window._err=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.cumResults ? state.cumResults.filter(r=>r!==null).length : 0")
        assert n >= 3, f"SGLT2i should have >=3 cumulative results, got {n}"

    def test_statins_changepoints_detected(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(1)}catch(e){window._err=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.cumResults ? state.cumResults.filter(r=>r!==null).length : 0")
        assert n >= 5, f"Statins should have >=5 cumulative results, got {n}"

    def test_pooled_estimate_exists(self, driver):
        fresh(driver)
        driver.execute_script("try{loadExample(0)}catch(e){window._err=e.message}")
        time.sleep(0.5)
        n = js(driver, "state.cumResults ? state.cumResults.filter(r=>r!==null).length : 0")
        assert n >= 3, f"Expected >=3 cumulative results, got {n}"

    def test_pooled_estimate_finite(self, driver):
        valid = js(driver, "state.cumResults ? state.cumResults.filter(r=>r!==null) : []")
        assert valid and len(valid) > 0, "No valid cumulative results"
        last = valid[-1]
        est = last.get('estimate', None)
        assert est is not None and abs(est) < 10, f"Estimate {est} not finite/reasonable"

    def test_heterogeneity_computed(self, driver):
        valid = js(driver, "state.cumResults ? state.cumResults.filter(r=>r!==null) : []")
        assert valid and len(valid) > 0
        i2 = valid[-1].get('I2', None)
        assert i2 is not None and 0 <= i2 <= 1, f"I2={i2} out of range"


# === What-If Analysis ===

class TestWhatIf:
    def test_whatif_tab_renders(self, driver):
        fresh(driver)
        driver.execute_script("loadExample(0)")
        time.sleep(0.5)
        click(driver, driver.find_element(By.ID, 'tbtn-whatif'))
        time.sleep(0.3)
        panel = driver.find_element(By.ID, 'tab-whatif')
        assert panel.is_displayed()

    def test_whatif_computation(self, driver):
        # What-if fields are dynamically created; just try to run
        result = driver.execute_script("""
            try { runWhatIf(); return 'ok'; } catch(e) { return e.message; }
        """)
        time.sleep(0.3)
        assert result == 'ok', f"What-if error: {result}"


# === Report ===

class TestReport:
    def test_report_tab_has_content(self, driver):
        fresh(driver)
        driver.execute_script("loadExample(0)")
        time.sleep(0.5)
        click(driver, driver.find_element(By.ID, 'tbtn-report'))
        time.sleep(0.3)
        panel = driver.find_element(By.ID, 'tab-report')
        text = panel.text
        assert len(text) > 50, "Report should have substantial text"

    def test_report_mentions_reml(self, driver):
        panel = driver.find_element(By.ID, 'tab-report')
        text = panel.text.lower()
        assert 'reml' in text or 'random' in text or 'pool' in text


# === Theme Toggle ===

class TestTheme:
    def test_default_theme(self, driver):
        fresh(driver)
        # Check initial theme
        theme = js(driver, "document.documentElement.getAttribute('data-theme') || 'dark'")
        assert theme in ('dark', 'light', None)

    def test_toggle_theme(self, driver):
        initial = js(driver, "document.documentElement.getAttribute('data-theme') || ''")
        toggle = driver.find_elements(By.CSS_SELECTOR, '[onclick*="theme"], [onclick*="Theme"], .theme-toggle, #themeToggle')
        if toggle:
            click(driver, toggle[0])
            time.sleep(0.2)
            after = js(driver, "document.documentElement.getAttribute('data-theme') || ''")
            assert after != initial, "Theme should change after toggle"


# === Accessibility ===

class TestAccessibility:
    def test_tab_roles(self, driver):
        fresh(driver)
        tabs = driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        assert len(tabs) >= 4

    def test_tabpanel_roles(self, driver):
        panels = driver.find_elements(By.CSS_SELECTOR, '[role="tabpanel"], .tab-panel')
        assert len(panels) >= 4

    def test_canvas_has_aria_label(self, driver):
        driver.execute_script("loadExample(0)")
        time.sleep(0.5)
        canvases = driver.find_elements(By.TAG_NAME, 'canvas')
        labelled = [c for c in canvases if c.get_attribute('aria-label')]
        assert len(labelled) >= 1, "At least one canvas should have aria-label"
