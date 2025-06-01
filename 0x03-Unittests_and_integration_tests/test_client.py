#!/usr/bin/env python3
"""Unit and Integration tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct output."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL."""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "http://test.com/orgs/google/repos"
            }

            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "http://test.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct list."""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://test.com/orgs/google/repos"

            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(
                "http://test.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": {"repos_url": "http://test.com/orgs/google/repos"},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ],
        "expected_repos": ["repo1", "repo2", "repo3"],
        "apache2_repos": ["repo1", "repo3"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get and fixtures."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def json_side_effect(url, *args, **kwargs):
            mock_resp = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock_get.side_effect = json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering."""
        client = GithubOrgClient("google")
        result = client.public_repos(license_key="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
