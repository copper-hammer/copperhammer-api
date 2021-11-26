# CopperHammer API

[![DeepSource](https://deepsource.io/gh/copper-hammer/copperhammer-api.svg/?label=active+issues&show_trend=true&token=4R7tABa0hLEft0oP1VCV4xmj)](https://deepsource.io/gh/copper-hammer/copperhammer-api/?ref=repository-badge)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6411cdbfd17b49bb8d25355a07ce30ca)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=copper-hammer/copperhammer-api&amp;utm_campaign=Badge_Grade)

*An extensive API for communicating with CoppenHammer workers and scanners*

## Communication & Models

### Authorization and Registration

Node sends HTTP request to `/{type}/node_register` with its key in the `X-API-Key` header. If the authorization was successful, the server will send an answer containing `nodeID` (conforming to *UUID4*) and a token (128 bits). Since now, the node is expected to connect to `/{type}/node/{nodeID}` via WebSocket with a `token` URL-parameter containing the token.

### Scanner Node

#### **POST** - /scanner/node_register

##### Description

Registeres a Scanner node in DB to receive authentication token.

##### CURL

```sh
curl -X POST "http://localhost:8000/scanner/node_register" \
    -H "X-API-Key: APITOKENKEY" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data-raw "$body"
```

##### Header Parameters

- **X-API-Key** should respect the following schema:

```json
{
  "type": "string"
}
```
- **Content-Type** should respect the following schema:

```json
{
  "type": "string",
  "enum": [
    "application/json; charset=utf-8"
  ]
}
```

##### Body Parameters

- **body** should respect the following schema:

```json
{
  "type": "string",
  "default": "{\"action\":\"AUTHENTICATE_REQUEST\"}"
}
```

#### **WEBSOCKET** - /scanner/node/*nodeID*

##### Description
Connects to Scanner Node websocket with a give nodeID and token.

##### JavaScript Example

```javascript
const WebSocket = require('ws')
var ws = new WebSocket("ws://localhost:8000/scanner/node/nodeID?token=token");

ws.onopen = function() {
   ws.send('{"action": "YAGOOD_NODE"}');
};

ws.onmessage = function (evt) {
   console.log(evt.data);
};
```

##### Query Parameters

- **token** should respect the following schema:

```json
{
  "type": "string"
}
```

##### **Available Actions in Socket**

```
AUTHENTICATE_REQUEST
AUTHENTICATE_ACCEPT
AUTHENTICATE_REJECT
TOKEN_REJECT
YAGOOD_NODE
REQUEST_BATCH
SEND_BATCH
SEND_BATCH_REJECT
BATCH_ACCEPT_CONFIRM
SUBMIT_RESULTS
RESULTS_ACCEPT_CONFIRM
RESULTS_REJECT
OVERALL_ERROR
MALFORMED_MESSAGE
NOTENOUGHARGS_ERROR
UNKNOWN_ACTION_RECEIVED
UNSUPPORTED_ACTION_RECEIVED
```

##### Message Structure

```json
{
  "action": "actionType",
  "result": {},
  "error": {
    "fr": false,
    "msg": null
  }
}
```

## Environment Variables

```ini
MASTER_KEY = # Currently not used, maybe deprecated
WEBSERVER_PORT = 8000 # Webserver port
MONGODB_HOST = # Host of MongoDB
MONGODB_PORT = # Port of MongoDB
MONGODB_USERNAME = # Username for MongoDB
MONGODB_PASSWORD = # Password for given username for MongoDB 
MONGODB_DB_NAME = cprhmr # Database name in MongoDB
MONGODB_AUTH_DB = admin # Authentication DB in MongoDB
```

## Running the App

###### *THIS WILL BE CHANGED TO **RUNNING THE APP IN DOCKER** AFTER THE SEVERAL MORE COMMITS*

Firstly, you need to install Python's requirements:
```
pip3 install -r requirements.tx
```

Secodnly, complete the `.env` file.

Finally, run the app:
```
uvicorn app:app
```
