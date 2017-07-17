"""
-----------------
POM UI components
-----------------
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

from .base import Block, Container, register_ui, UI, wait_for_presence  # noqa
from .button import Button  # noqa
from .checkbox import CheckBox  # noqa
from .combobox import ComboBox  # noqa
from .form import Form  # noqa
from .link import Link  # noqa
from .table import List, Row, Table  # noqa
from .fields import FileField, IntegerField, TextField  # noqa

__all__ = [
    'Block',
    'Container',
    'register_ui',
    'UI',
    'wait_for_presence',
    'Button',
    'CheckBox',
    'ComboBox',
    'Form',
    'Link',
    'List',
    'Row',
    'Table',
    'FileField',
    'IntegerField',
    'TextField',
]
