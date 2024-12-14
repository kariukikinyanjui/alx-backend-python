#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''
    Test class for GithubOrgClient.
    '''

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        '''
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name(str): The name of the GitHub organization.
            mock_get_json(Mock): The mocked get_json function.
        '''
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"login": org_name})

    @parameterized.expand([
        (
            "google", {"repos_url": "https://api.github.com/orgs/google/repos"}
            ),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    def test_public_repos_url(self, org_name, payload):
        '''
        Test that GithubOrgClient._public_repos_url returns the correct URL

        Args:
            org_name (str): The name of the GitHub organization.
            payload (dict): The mocked payload returned by the org property
        '''
        with patch(
                'client.GithubOrgClient.org', new_callable=PropertyMock
                ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
