#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

from .. import test_utils
from google.datacatalog_connectors.commons_test import utils
import mock


class MetadataScraperTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    def test_scrape_metadata_with_csv_should_return_objects(
            self, to_metadata_dict):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')
        to_metadata_dict.return_value = metadata

        scraper = test_utils.FakeScraper()

        schemas_metadata = scraper.get_metadata(
            {},
            csv_path=utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH, 'rdbms_full_dump.csv'))

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    def test_scrape_metadata_with_credentials_should_return_objects(
            self, to_metadata_dict):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        to_metadata_dict.return_value = metadata

        scraper = test_utils.FakeScraper()

        schemas_metadata = scraper.get_metadata({},
                                                connection_args={
                                                    'host': 'localhost',
                                                    'port': 1234
                                                })

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    def test_scrape_metadata_on_exception_should_re_raise(
            self, to_metadata_dict):  # noqa
        scraper = test_utils.FakeScraper()

        self.assertRaises(Exception, scraper.get_metadata, {})

        self.assertEqual(to_metadata_dict.call_count, 0)

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    def test_scrape_metadata_on_connection_exception_should_re_raise(
            self, to_metadata_dict):  # noqa
        scraper = test_utils.FakeScraperWithConError()

        self.assertRaises(Exception,
                          scraper.get_metadata, {},
                          connection_args={
                              'host': 'localhost',
                              'port': 1234
                          })

        self.assertEqual(to_metadata_dict.call_count, 0)
