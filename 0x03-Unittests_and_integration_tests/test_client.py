#!/usr/bin/env python3
"""Parameterize Integration test"""

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """test github org client"""

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, inp, mock):
        """function test org """
        test_cla = GithubOrgClient(inp)
        test_cla.org()
        mock.assert_called_once_with(f'https://api.github.com/orgs/{inp}')

    def test_public_repos_url(self):
        """ test public repos"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payom = {"repos_url": "World"}
            mock.return_value = payom
            test_cla = GithubOrgClient('test')
            resu = test_cla._public_repos_url
            self.assertEqual(resu, payom["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """test public repos"""
        json_payom = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = json_payom

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public:

            mock_public.return_value = "hello/world"
            test_cla = GithubOrgClient('test')
            resu = test_cla.public_repos()

            check = [i["name"] for i in json_payom]
            self.assertEqual(resu, check)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """test_has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(resu, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """TestIntegrationGithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """setUpClass"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """test_public_repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """test_public_repos_with_license"""
        test_cla = GithubOrgClient("google")

        self.assertEqual(test_cla.public_repos(), self.expected_repos)
        self.assertEqual(test_cla.public_repos("XLICENSE"), [])
        self.assertEqual(test_cla.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """tearDownClass"""
        cls.get_patcher.stop()
