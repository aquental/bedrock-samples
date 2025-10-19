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
