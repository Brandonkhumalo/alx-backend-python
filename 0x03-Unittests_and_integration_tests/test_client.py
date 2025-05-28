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
