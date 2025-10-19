import unittest
from unittest.mock import patch, MagicMock, call
import sys
import importlib


class TestBedrockClient(unittest.TestCase):
    """Test suite for Bedrock client functionality"""

    def setUp(self):
        """Remove main module from cache before each test"""
        if 'main' in sys.modules:
            del sys.modules['main']
    
    @patch('boto3.client')
    def test_bedrock_client_initialization(self, mock_boto_client):
        """Test that the Bedrock client is initialized correctly"""
        # Setup mock
        mock_boto_client.return_value = MagicMock()
        
        # Import the module to trigger client initialization
        import main
        
        # Verify boto3.client was called with correct parameters
        mock_boto_client.assert_called_with("bedrock-runtime", region_name="us-east-1")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_correct_model_id_used(self, mock_boto_client, mock_print):
        """Test that the correct model ID is used in the converse call"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response
        mock_client.converse.return_value = {
            "output": {
                "message": {
                    "content": [{"text": "Test response"}]
                }
            }
        }
        
        # Import and execute the main module
        import main
        
        # Verify converse was called with the correct model ID
        mock_client.converse.assert_called_once()
        args, kwargs = mock_client.converse.call_args
        self.assertEqual(kwargs['modelId'], "us.anthropic.claude-sonnet-4-20250514-v1:0")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_message_formatting(self, mock_boto_client, mock_print):
        """Test that the input message is correctly formatted for the converse call"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response
        mock_client.converse.return_value = {
            "output": {
                "message": {
                    "content": [{"text": "Test response"}]
                }
            }
        }
        
        # Import and execute the main module
        import main
        
        # Expected message format
        expected_messages = [
            {
                "role": "user",
                "content": [
                    {
                        "text": "Explain to a beginner what is AWS Bedrock."
                    }
                ]
            }
        ]
        
        # Verify converse was called with correctly formatted messages
        mock_client.converse.assert_called_once()
        args, kwargs = mock_client.converse.call_args
        self.assertEqual(kwargs['messages'], expected_messages)
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_response_parsing_single_part(self, mock_boto_client, mock_print):
        """Test that the response from the Bedrock API is parsed and extracted correctly"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response with single content part
        mock_response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "AWS Bedrock is a managed service."}
                    ]
                }
            }
        }
        mock_client.converse.return_value = mock_response
        
        # Import and execute the main module
        import main
        
        # Verify the response was extracted and printed correctly
        mock_print.assert_called_with("AWS Bedrock is a managed service.")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_response_parsing_multiple_parts(self, mock_boto_client, mock_print):
        """Test response parsing with multiple content parts"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response with multiple content parts
        mock_response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "Part 1: AWS Bedrock "},
                        {"text": "Part 2: is a "},
                        {"text": "Part 3: managed service."}
                    ]
                }
            }
        }
        mock_client.converse.return_value = mock_response
        
        # Import and execute the main module
        import main
        
        # Verify all parts were joined correctly
        mock_print.assert_called_with("Part 1: AWS Bedrock Part 2: is a Part 3: managed service.")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_response_parsing_with_non_dict_parts(self, mock_boto_client, mock_print):
        """Test response parsing handles non-dict parts gracefully"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response with mixed content types
        mock_response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "Valid text"},
                        "invalid_string",  # Non-dict element
                        {"text": " continued"},
                        None,  # None element
                        {"other_key": "no text key"},  # Dict without 'text' key
                    ]
                }
            }
        }
        mock_client.converse.return_value = mock_response
        
        # Import and execute the main module
        import main
        
        # Verify only valid text parts were extracted
        mock_print.assert_called_with("Valid text continued")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_response_parsing_empty_content(self, mock_boto_client, mock_print):
        """Test response parsing with empty content"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock response with empty content
        mock_response = {
            "output": {
                "message": {
                    "content": []
                }
            }
        }
        mock_client.converse.return_value = mock_response
        
        # Import and execute the main module
        import main
        
        # Verify empty string is printed
        mock_print.assert_called_with("")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_response_parsing_missing_fields(self, mock_boto_client, mock_print):
        """Test response parsing with missing fields"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Test with missing 'message' field
        mock_response = {"output": {}}
        mock_client.converse.return_value = mock_response
        
        # Import and execute the main module
        import main
        
        # Verify empty string is printed when fields are missing
        mock_print.assert_called_with("")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_error_handling_api_failure(self, mock_boto_client, mock_print):
        """Test error handling when the Bedrock API call fails"""
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock to raise an exception
        mock_client.converse.side_effect = Exception("API connection failed")
        
        # Import and execute the main module
        import main
        
        # Verify error was caught and printed
        mock_print.assert_called_with("Error: API connection failed")
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_error_handling_boto3_client_error(self, mock_boto_client, mock_print):
        """Test error handling for boto3 ClientError"""
        from botocore.exceptions import ClientError
        
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock to raise ClientError
        error_response = {
            'Error': {
                'Code': 'ValidationException',
                'Message': 'Invalid model ID provided'
            }
        }
        mock_client.converse.side_effect = ClientError(error_response, 'converse')
        
        # Import and execute the main module
        import main
        
        # Verify error was caught and printed
        mock_print.assert_called()
        printed_message = mock_print.call_args[0][0]
        self.assertIn("Error:", printed_message)
        self.assertIn("ValidationException", printed_message)
    
    @patch('builtins.print')
    @patch('boto3.client')
    def test_error_handling_timeout(self, mock_boto_client, mock_print):
        """Test error handling for timeout errors"""
        from botocore.exceptions import ConnectTimeoutError
        
        # Setup mock client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Setup mock to raise timeout error
        mock_client.converse.side_effect = ConnectTimeoutError(endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com')
        
        # Import and execute the main module
        import main
        
        # Verify error was caught and printed
        mock_print.assert_called()
        printed_message = mock_print.call_args[0][0]
        self.assertIn("Error:", printed_message)


if __name__ == '__main__':
    unittest.main()