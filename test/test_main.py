"""
This module serves to test main.py module.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.main import Main


class TestMain(unittest.TestCase):
    """
    This is the main test class.
    """

    def setUp(self):
        self.main = Main()

    @patch("src.main.HubConnectionBuilder")
    def test_set_sensorhub(self, mock_hub_connection_builder):
        self.main.set_sensorhub()
        mock_hub_connection_builder.assert_called_once()

    @patch("src.main.requests.get")
    def test_send_action_to_hvac(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_get.return_value = mock_response

        action = "TurnOnAc"
        result = self.main.send_action_to_hvac(action)

        expected_url = (
            f"{self.main.host}/api/hvac/{self.main.token}/{action}/{self.main.tickets}"
        )
        mock_get.assert_called_once_with(expected_url)
        self.assertEqual(
            result, None, "The send_action_to_hvac function should return None"
        )

    def test_take_action(self):
        with patch.object(self.main, "send_action_to_hvac") as mock_send_action:
            self.main.take_action(self.main.t_max + 1)
            mock_send_action.assert_called_with("TurnOnAc")

            self.main.take_action(self.main.t_min - 1)
            mock_send_action.assert_called_with("TurnOnHeater")


if __name__ == "__main__":
    unittest.main()
