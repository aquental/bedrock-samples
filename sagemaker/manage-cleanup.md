# cleanup usinf CLI

```shell
# Describe an endpoint
aws sagemaker describe-endpoint --endpoint-name california-housing-realtime
```

```json
{
  "EndpointName": "california-housing-realtime",
  "EndpointArn": "arn:aws:sagemaker:us-east-1:635858937972:endpoint/california-housing-realtime",
  "EndpointConfigName": "california-housing-realtime",
  "ProductionVariants": [
    {
      "VariantName": "AllTraffic",
      "DeployedImages": [
        {
          "SpecifiedImage": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3",
          "ResolvedImage": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn@sha256:82bed6e5a382c1132589c5d12f352df53498535c9ced1c4d00148699bf61caa1",
          "ResolutionTime": "2025-11-19T19:45:35.193000+00:00"
        }
      ],
      "CurrentWeight": 1.0,
      "DesiredWeight": 1.0,
      "CurrentInstanceCount": 1,
      "DesiredInstanceCount": 1
    }
  ],
  "EndpointStatus": "InService",
  "CreationTime": "2025-11-19T19:45:34.450000+00:00",
  "LastModifiedTime": "2025-11-19T19:49:00.684000+00:00"
}
```

```shell
# Describe an endpoint config
aws sagemaker describe-endpoint-config --endpoint-config-name california-housing-realtime
```

```json
{
  "EndpointConfigName": "california-housing-realtime",
  "EndpointConfigArn": "arn:aws:sagemaker:us-east-1:635858937972:endpoint-config/california-housing-realtime",
  "ProductionVariants": [
    {
      "VariantName": "AllTraffic",
      "ModelName": "sagemaker-scikit-learn-2025-11-19-19-45-32-551",
      "InitialInstanceCount": 1,
      "InstanceType": "ml.m5.large",
      "InitialVariantWeight": 1.0
    }
  ],
  "CreationTime": "2025-11-19T19:45:33.861000+00:00",
  "EnableNetworkIsolation": false
}
```

```shell
# Delete an endpoint
aws sagemaker delete-endpoint --endpoint-name california-housing-realtime
```

```shell
# Delete an endpoint config
aws sagemaker delete-endpoint-config --endpoint-config-name california-housing-realtime
```
