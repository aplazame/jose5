# jose5

JSON Composer

The fifth José in Aplazame

## Example

The following file, `dev.json` ...

```json
{
    "__extends": "./base.json",
    "__variables": {
        "ENVIRONMENT": "dev"
    },
    "environment": [
        {
            "name": "LOG_LEVEL",
            "value": "DEBUG"
        },
        {
            "name": "EXTRA_DEVELOPMENT_PARAM",
            "value": 20
        }
    ],
    "secrets": [
        {
            "name": "SECRET_KEY",
            "valueFrom": "${PARAM_BASE_PATH}/SECRET_KEY"
        }
    ],
    "mergemap": {
        "b": "dev",
        "c": "dev"
    }
}
```

... with `base.json`

```json
{
    "__variables": {
        "PARAM_BASE_PATH": "/app/${ENVIRONMENT}"
    },
    "environment": [
        {
            "name": "ENVIRONMENT",
            "value": "${ENVIRONMENT}"
        },
        {
            "name": "LOG_LEVEL",
            "value": "INFO"
        }
    ],
    "mergemap": {
        "a": "base",
        "b": "base"
    }
}
```

... produces this result

```json
{
  "environment": [
    {
      "name": "ENVIRONMENT",
      "value": "dev"
    },
    {
      "name": "LOG_LEVEL",
      "value": "DEBUG"
    },
    {
      "name": "EXTRA_DEVELOPMENT_PARAM",
      "value": 20
    }
  ],
  "mergemap": {
    "a": "base",
    "b": "dev",
    "c": "dev"
  },
  "secrets": [
    {
      "name": "SECRET_KEY",
      "valueFrom": "/app/${ENVIRONMENT}/SECRET_KEY"
    }
  ]
}
```
