# Bucket Manager

upload and manager items in your GCP bucket.

## `app.yaml`

```yaml
runtime: python37
service: bucket-manager
env_variables:
  BUCKET_NAME: <name>
  BASIC_AUTH_USERNAME: <username>
  BASIC_AUTH_PASSWORD: <password>
  SECRET_KEY: <random string>
handlers:
- url: /static
  static_dir: static/
- url: /.*
  script: auto
```

## `requirements.txt`

- `flask`
- `Flask-BasicAuth`
- `google-cloud-storage`
