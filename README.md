# CopperHammer API

[![DeepSource](https://deepsource.io/gh/copper-hammer/copperhammer-api.svg/?label=active+issues&show_trend=true&token=4R7tABa0hLEft0oP1VCV4xmj)](https://deepsource.io/gh/copper-hammer/copperhammer-api/?ref=repository-badge)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6411cdbfd17b49bb8d25355a07ce30ca)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=copper-hammer/copperhammer-api&amp;utm_campaign=Badge_Grade)

*An extensive API for communicating with CoppenHammer workers and scanners*

## Communication & Models

### Authorization and Registration

Node sends HTTP request to `/{type}/node_register` with its key in the `X-API-Key` header. If the authorization was successful, the server will send an answer containing `nodeID` (conforming to *UUID4*) and a token (128 bits). Since now, the node is expected to connect to `/{type}/node/{nodeID}` via WebSocket with a `token` URL-parameter containing the token.
