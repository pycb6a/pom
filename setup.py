"""
--------------------------------------------------------------------------
POM microframework to develop web UI tests easy, quickly and with pleasure
--------------------------------------------------------------------------
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

from setuptools import setup, find_packages

setup(
    name='python-pom2',
    version='2.0.1',
    description=('POM is Page-Object-Model microframework to develop web UI '
                 'tests easy, quickly and with pleasure.'),
    long_description=open('readme.rst').read(),
    author='Sergei Chipiga',
    author_email='chipiga86@gmail.com',
    license='ALv2',
    packages=find_packages(),
    url='https://github.com/sergeychipiga/pom',
    install_requires=[
        'six',
        'selenium',
        'waiting',
    ]
)
