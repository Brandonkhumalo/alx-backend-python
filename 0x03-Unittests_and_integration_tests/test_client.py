#!/usr/bin/env python3
"""Unit tests for the client.GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org property."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns correct JSON payload and calls get_json once.

        Args:
            org_name (str): The GitHub organization name to test.
            mock_get_json (MagicMock): The mocked get_json function.
        """
        # Setup the mock return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Create client instance
        client = GithubOrgClient(org_name)

        # Access the org property (do not call as method)
        result = client.org

        # Assert get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert the result is as expected
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()

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
