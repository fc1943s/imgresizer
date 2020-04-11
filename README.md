# imgresizer

## Execution

- `docker-compose -f up --build` to execute the application (unit tests run on build)
- `docker-compose -f docker-compose.e2e.yml up --build` to execute the e2e tests (application needs to be running)

## API Documentation
URL: http://DOCKER_HOST:5000

`POST` **/resize**

Request
- Supported Media Types: `multipart/form-data`
- File name: `img`

Response
- Media Type: `image/png`
- Status code `200`: The resized image is returned.
- Status code `400`: Error while resizing the image.


