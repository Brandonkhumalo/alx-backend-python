#!/usr/bin/env python3
"""Unit tests for the access_nested_map function in utils module.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence[str], expected: Any) -> None:
        """Test that access_nested_map returns expected result for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

#!/usr/bin/env python3
"""Unit tests for the access_nested_map function in utils module.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence[str], expected: Any) -> None:
        """Test that access_nested_map returns expected result for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence[str]) -> None:
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))

#!/usr/bin/env python3
"""Unit tests for the utils module functions.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Test case for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """Test that get_json returns the expected payload and calls requests.get correctly."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

#!/usr/bin/env python3
"""Unit tests for the utils module functions.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test case for memoize decorator."""

    def test_memoize(self) -> None:
        """Test that a memoized method is called only once despite multiple accesses."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()

        with patch.object(test_obj, 'a_method', return_value=42) as mocked_method:
            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert the return value is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once
            mocked_method.assert_called_once()
