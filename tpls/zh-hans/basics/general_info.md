# General API Information

## Endpoints

The base mainnet endpoint is: https://api3.loopring.io

The base testnet endpoint is: https://uat2.loopring.io

All endpoints return either a JSON object or array.

## HTTP Return Codes
HTTP 400(BAD_REQUEST) return codes are used for malformed requests; the issue is on the sender's side.

HTTP 429 return code is used when breaking a request rate limit.

HTTP 5XX return codes are used for internal errors; the issue is on Loopring's side.

## Error Codes
If there is an error, the API will return an error with a message of the reason.

```json
{
  "code": 100206,
  "msg": "Invalid signature."
}
```

Specific error codes and messages are defined in Error Codes.

## General Information on Endpoints
For GET endpoints, parameters must be sent as a query string.

For POST, PUT, and DELETE endpoints, the parameters must be in the request body with content type `application/json`.

## LIMITS
Each API has its own limit control, refer to specific API page for the configuation.

A 429 will be returned when rate limit is violated.