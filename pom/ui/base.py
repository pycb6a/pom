"""
---------------
Base UI element
---------------
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import logging

import waiting
from selenium.common import exceptions
from selenium.webdriver import ActionChains

from pom import utils
from pom.exceptions import PomError

__all__ = [
    'Block',
    'Container',
    'register_ui',
    'wait_for_presence',
    'WebElementProxy',
    'UI',
]

LOGGER = logging.getLogger(__name__)

PRESENCE_ERRORS = (exceptions.StaleElementReferenceException,
                   exceptions.NoSuchElementException)


def wait_for_presence(func):
    """Decorator to wait for ui element will be present at display."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwgs):
        self.wait_for_presence()
        return func(self, *args, **kwgs)

    return wrapper


def register_ui(**ui):
    """Decorator to register ui elements of ui container."""

    def wrapper(cls):
        cls.register_ui(**ui)
        return cls

    return wrapper


class Container(object):
    """Container, base class."""

    @classmethod
    def register_ui(cls, **ui):
        """Register ui elements.

        Sets ui elements as cached properties. Inside property it clones ui
        element to provide safe-thread execution.
        """
        for ui_name, ui_obj in ui.items():
            def ui_getter(self, ui_obj=ui_obj):
                ui_clone = ui_obj.clone()
                ui_clone.set_container(self)
                return ui_clone

            ui_getter.__name__ = ui_name
            ui_getter = property(utils.cache(ui_getter))
            setattr(cls, ui_name, ui_getter)

    def __enter__(self):
        """Use container as context manager for readable code."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from context manager."""
        pass

    def find_element(self, locator):
        """Find DOM element inside container."""
        return self.webelement.find_element(*locator)

    def find_elements(self, locator):
        """Find DOM elements inside container."""
        return self.webelement.find_elements(*locator)


class WebElementProxy(object):
    """Web element proxy is used to catch exceptions with webelement."""

    def __init__(self, webelement_getter, ui_info):
        """Constructor."""
        self._webelement_getter = webelement_getter
        self._cached_webelement = None
        self._ui_info = ui_info

    @utils.cache
    def __dir__(self):
        """Return available methods for code completion."""
        return dir(self._webelement_getter())

    def __getattr__(self, name):
        """Execute web element methods and properties."""

        def webelement_attr(self=self):
            self._cached_webelement = self._cached_webelement or \
                                      self._webelement_getter()
            return getattr(self._cached_webelement, name)

        try:
            result = webelement_attr()

        except PRESENCE_ERRORS:
            LOGGER.debug("{} isn't present in DOM. Cache is flushed.".format(
                self._ui_info))
            self._cached_webelement = None
            result = webelement_attr()

        if not callable(result):  # It's selenium element property.
            return result

        def method(*args, **kwgs):
            try:
                return result(*args, **kwgs)

            except PRESENCE_ERRORS:
                LOGGER.debug(
                    "{} isn't present in DOM. Cache is flushed.".format(
                        self._ui_info))
                self._cached_webelement = None
                return webelement_attr()(*args, **kwgs)

        method.__name__ = name
        return method


class UI(object):
    """Base class of ui element."""

    _container = None
    _timeout = 5  # sec to wait element presence / absence in DOM

    def __init__(self, *locator, **index):
        """Constructor.

        Arguments:
            - locator.
        """
        self.locator = locator
        self.index = index.get('index')

    @utils.cache
    def __repr__(self):
        """Object representation."""
        return self.__class__.__name__ + \
            '(by={!r}'.format(self.locator[0]) + \
            ', value={!r}'.format(self.locator[1]) + \
            (')' if self.index is None else ', index={})'.format(self.index))

    @property
    def container(self):
        """Get container of webelement."""
        return self._container

    def set_container(self, container):
        """Set container of webelement."""
        self._container = container

    @utils.log
    @wait_for_presence
    def click(self):
        """Click ui element."""
        self.webelement.click()

    @utils.log
    @wait_for_presence
    def right_click(self):
        """Right click ui element."""
        self._action_chains.context_click(self.webelement).perform()

    @utils.log
    @wait_for_presence
    def double_click(self):
        """Double click ui element."""
        self._action_chains.double_click(self.webelement).perform()

    @utils.log
    @wait_for_presence
    def get_attribute(self, attr_name):
        """Get attribute of ui element."""
        return self.webelement.get_attribute(attr_name)

    @utils.log
    @wait_for_presence
    def scroll_to(self):
        """Scroll window to ui element."""
        self.webdriver.execute_script("window.scroll({x}, {y});".format(**self.webelement.location))

    @utils.log
    @wait_for_presence
    def move_to(self):
        """Hover to ui element."""
        self._action_chains.move_to_element(self.webelement).perform()

    @property
    @utils.log
    @wait_for_presence
    def value(self):
        """Get value of ui element."""
        return self.webelement.get_attribute('innerHTML').strip()

    @property
    @utils.log
    def is_present(self):
        """Define is ui element present at display."""
        try:
            return self.webelement.is_displayed()
        except PRESENCE_ERRORS:
            return False

    @property
    @utils.log
    def is_enabled(self):
        """Define is ui element enabled."""
        return self.webelement.is_enabled()

    @property
    @utils.cache
    def webdriver(self):
        """Get webdriver."""
        return self.container.webdriver

    @property
    @utils.cache
    def webelement(self):
        """Get webelement."""
        if self.index:
            webelement_getter = lambda self=self: \
                self.container.find_elements(self.locator)[self.index]

        else:
            webelement_getter = lambda self=self: \
                self.container.find_element(self.locator)

        return WebElementProxy(webelement_getter, ui_info=repr(self))

    @property
    @utils.cache
    def _action_chains(self):
        return ActionChains(self.webdriver)

    def clone(self):
        """Clone ui element."""
        return self.__class__(self.locator[0],
                              self.locator[1],
                              index=self.index)

    @utils.log
    def wait_for_presence(self, timeout=None):
        """Wait for ui element presence."""
        timeout = timeout or self._timeout
        try:
            waiting.wait(lambda: self.is_present,
                         timeout_seconds=timeout, sleep_seconds=0.1)
        except waiting.TimeoutExpired:
            raise PomError(
                "{!r} is still absent after {} sec".format(self, timeout))

    @utils.log
    def wait_for_absence(self, timeout=None):
        """Wait for ui element absence."""
        timeout = timeout or self._timeout
        try:
            waiting.wait(lambda: not self.is_present,
                         timeout_seconds=timeout, sleep_seconds=0.1)
        except waiting.TimeoutExpired:
            raise PomError(
                "{!r} is still present after {} sec".format(self, timeout))


class Block(UI, Container):
    """UI block is containerable ui element."""

    @utils.log
    @wait_for_presence
    def find_element(self, locator):
        """Find DOM element inside container."""
        return super(Block, self).find_element(locator)

    @utils.log
    @wait_for_presence
    def find_elements(self, locator):
        """Find DOM elements inside container."""
        return super(Block, self).find_elements(locator)
