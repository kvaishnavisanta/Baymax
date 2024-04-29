import unittest
from unittest.mock import patch
from io import StringIO
from main import main


class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=["1"])  # Simulate user input of "1"
    @patch('hume.HumeVoiceClient')
    @patch('hume.MicrophoneInterface.start')
    def test_choice_1(self, mock_start, mock_client, mock_input):
        main()
        mock_client.assert_called_once_with("k4tzTx8wFZOGgmCKEes1khlzcLK1270ohsbcjKnoptT6FPyp")
        mock_start.assert_called_once()

    @patch('builtins.input', side_effect=["2"])
    @patch('hume.HumeVoiceClient')
    @patch('find_config.list_configs', return_value=("Selected Config Name", "Selected Config ID"))
    def test_choice_2(self, mock_list_configs, mock_client, mock_input):
        main()
        mock_list_configs.assert_called_once()
        mock_client.assert_called_once_with("k4tzTx8wFZOGgmCKEes1khlzcLK1270ohsbcjKnoptT6FPyp")

    @patch('builtins.input', side_effect=["3"])
    @patch('create_personality.create_personality_config')
    @patch('hume.HumeVoiceClient')
    def test_choice_3(self, mock_client, mock_create_personality, mock_input):
        main()
        mock_create_personality.assert_called_once()
        mock_client.assert_called_once_with("k4tzTx8wFZOGgmCKEes1khlzcLK1270ohsbcjKnoptT6FPyp")

    @patch('builtins.input', side_effect=["4"])  # Simulate invalid choice
    @patch('sys.stdout', new_callable=StringIO)
    @patch('hume.HumeVoiceClient')
    def test_invalid_choice(self, mock_client, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Invalid choice. Please choose again.")


if __name__ == '__main__':
    unittest.main()
