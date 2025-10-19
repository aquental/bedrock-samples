# basic sample

Connect and ask `Explain to a beginner what is AWS Bedrock.` to Claude Sonnet 4

## setup

### if you do not have AWS cli installed

```shell
brew install awscli
```

Run `aws configure`:

1. Set environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
2. Use an IAM role if running on AWS infrastructure

### add boto library

```shell
uv add boto3
```

## run

```shell
uv run python main.py
```

# Bedrock Client Unit Tests

## Overview

This test suite provides comprehensive unit testing for the AWS Bedrock client implementation in `main.py`.

## Test Coverage

The test suite covers the following scenarios:

1. **Client Initialization** - Verifies that the Bedrock client is initialized with correct parameters (service name and region)

2. **Model ID Usage** - Ensures the correct Claude Sonnet model ID is used in API calls

3. **Message Formatting** - Validates that user messages are properly formatted according to the Bedrock API requirements

4. **Response Parsing**:

   - Single content part responses
   - Multiple content parts (concatenation)
   - Empty content handling
   - Missing fields in response
   - Non-dictionary elements in content array

5. **Error Handling**:
   - Generic API failures
   - boto3 ClientError exceptions
   - Connection timeout errors

## Running the Tests

### Prerequisites

- Python 3.12.6+
- boto3 library installed (included in project dependencies)

### With Virtual Environment (Recommended)

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run all tests with verbose output
python -m unittest test_main -v

# Run a specific test
python -m unittest test_main.TestBedrockClient.test_bedrock_client_initialization -v
```

### Without Virtual Environment

```bash
# Install dependencies first
pip install boto3

# Run tests
python -m unittest test_main -v
```

## Test Implementation Details

The tests use Python's built-in `unittest` framework with `unittest.mock` for mocking AWS services. Key features:

- **Mocking Strategy**: All tests mock the `boto3.client` to prevent actual AWS API calls
- **Module Isolation**: Each test removes the `main` module from Python's module cache to ensure clean imports
- **Comprehensive Assertions**: Tests verify both successful operations and error conditions

## Adding New Tests

To add new tests, follow this pattern:

```python
@patch('builtins.print')
@patch('boto3.client')
def test_new_feature(self, mock_boto_client, mock_print):
    """Test description"""
    # Setup mock client
    mock_client = MagicMock()
    mock_boto_client.return_value = mock_client

    # Configure mock behavior
    mock_client.converse.return_value = {...}

    # Import and execute
    import main

    # Assert expected behavior
    self.assertEqual(...)
```

## CI/CD Integration

These tests can be easily integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    python -m pip install boto3
    python -m unittest test_main
```
