#!/usr/bin/env python3
"""Tests for client.GithubOrgClient.org method"""

import unittest
from unittest.mock import patch

from client import GithubOrgClient
from fixtures import org_payload


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient"""

    def test_org(self):
        """Test that GithubOrgClient.org returns the correct value and calls get_json once"""

        for org_name in ("google", "abc"):
            with self.subTest(org=org_name):
                with patch("client.get_json") as mock_get_json:
                    mock_get_json.return_value = org_payload

                    client = GithubOrgClient(org_name)
                    result = client.org()

                    mock_get_json.assert_called_once_with(
                        f"https://api.github.com/orgs/{org_name}"
                    )
                    self.assertEqual(result, org_payload)

#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url property returns the repos_url from the
        mocked org payload.
        """
        fake_payload: Dict[str, str] = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=fake_payload
        ):
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from typing import List, Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that public_repos returns the expected list of repo names.

        Uses patch to mock get_json and _public_repos_url.
        """
        repos_payload: List[Dict[str, str]] = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test_org/repos"
        ) as mock_public_repos_url:
            result = client.public_repos()

            expected = [repo["name"] for repo in repos_payload]
            self.assertEqual(result, expected)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.has_license method."""

import unittest
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Test that has_license returns True if repo has the given license key,
        else False.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)

#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos method."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
import requests
from client import GithubOrgClient
import fixtures  # assumes fixtures.py is in the same folder or accessible


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using real logic except external calls."""

    @classmethod
    def setUpClass(cls) -> None:
        """Setup patcher for requests.get and configure side_effect for json() to return fixtures."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Helper side_effect function for requests.get().json()
        def json_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock_get.side_effect = json_side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher for requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public_repos with license filtering (apache-2.0)."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license_key="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
