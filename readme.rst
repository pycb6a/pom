==========
Annotation
==========
POM is Page-Object-Model microframework to develop web UI tests easy, quickly and with pleasure.

============
Architecture
============
POM provides API to manipulate with web UI elements and pages in browser. Under hood it uses selenium.
Before to act with UI element POM waits for its visibility, because in user cases user can't interact with UI element if it isn't visible at display.
POM provides tree hirarchy to request UI elements with UI caching mechanism at each level.

POM doesn't use **implicit_wait** method to wait UI element, because implicit_wait waits until element is present at DOM even if it isn't visible. And also implicit_wait has conflict with caching mechanism, that leads to long requests in some cases.

So POM has own implementation to wait element before interact. It leads to additinal webdriver request before interact with UI element, but provide reliable and simple architecture, without speed degradation.

============
How to start
============
Let imagine simple testcase:

- ``Go to https://facebook.com``
- ``Fill login / password fields with 'admin' / 'admin' values``
- ``Click button login``
- ``Assert page to log in is opened``
- ``Assert alert message is opened``

Its implementation with POM:

.. code:: python

  import pytest
  from selenium import webdriver
  from selenium.webdriver.common.by import By

  import pom
  from pom import ui


  @ui.register_ui(field_login=ui.TextField(By.ID, 'email'),
  field_password=ui.TextField(By.ID, 'pass'))
  class FormLogin(ui.Form):
  """Form to login."""


  @ui.register_ui(form_login=FormLogin(By.ID, 'login_form'))
  class PageMain(pom.Page):
        """Main page."""
      url = '/'


  @ui.register_ui(
      alert_message=ui.Block(By.CSS_SELECTOR, 'div.uiContextualLayerPositioner'))
  class PageLogin(pom.Page):
      """Login page."""
      url = '/login'

  @pom.register_pages([PageMain, PageLogin])
  class Facebook(pom.App):
      """Facebook web application."""

      def __init__(self):
          super(Facebook, self).__init__(url='https://www.facebook.com',
                                         browser='chrome',
                                         executable_path='path/to/chromedriver')
          self.webdriver.maximize_window()
          self.webdriver.set_page_load_timeout(30)


  @pytest.fixture()
  def fb():
      fb_ = Facebook()

      yield fb_

      fb_.quit()


  def test_facebook_invalid_login(fb):
  """User with invalid credentials can't login to facebook."""
        fb.page_main.open()
        with fb.page_main.form_login as form:
            form.field_login.set_value('admin')
            form.field_password.set_value('admin')
            form.submit()
        assert fb.current_page == fb.page_login
        assert fb.page_login.alert_message.is_present


**To launch example:**

- Save example code in file ``test_pom.py``
- Install POM framework ``pip install hg+ssh://hg@bitbucket.org/pycb6a/pom#egg=python-pom2``
- Launch test example ``py.test test_pom.py``
