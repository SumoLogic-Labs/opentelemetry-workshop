#!/bin/bash

readonly EPOCH_DATE="$(date +%s)"

read -r -d "" SPAN <<END_SPAN
{"resourceSpans":[{
	"resource":{
		"attributes":[
			{"key":"service.name","value":{"stringValue":"Some Service"}}
		]
	},
	"scopeSpans":[{
		"scope":{},
			"spans":[
				{
					"traceId":"0000000000000000ffffff${EPOCH_DATE}",
					"spanId":"ffffff${EPOCH_DATE}",
					"parentSpanId":"",
					"name":"some-service-span",
					"kind":"SPAN_KIND_SERVER",
					"startTimeUnixNano":"${EPOCH_DATE}000000000",
					"endTimeUnixNano":"${EPOCH_DATE}010000000",
					"attributes":[
						{"key":"net.peer.port","value":{"intValue":"4444"}}
					],
					"status":{
						"code":"STATUS_CODE_OK"
					}
				},
				{
					"traceId":"0000000000000000ffffff${EPOCH_DATE}",
					"spanId":"fffffa${EPOCH_DATE}",
					"parentSpanId":"",
					"name":"some-service-span",
					"kind":"SPAN_KIND_SERVER",
					"startTimeUnixNano":"${EPOCH_DATE}020000000",
					"endTimeUnixNano":"${EPOCH_DATE}030000000",
					"attributes":[
						{"key":"net.peer.port","value":{"intValue":"4444"}}
					],
					"status":{
						"code":"STATUS_CODE_OK"
					}
				}
			]
		}]
	}]
}
END_SPAN

set -x
curl -v "http://localhost:4318/v1/traces"  -H "Content-type: application/json" --data-raw "$SPAN"
