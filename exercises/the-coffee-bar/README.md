# The Coffee Bar

Italian Bar with delicious coffee and cakes. Built using multiple technologies like NodeJS, Ruby, Python and .Net Core. 
It's a simple application where you can order coffee or some cakes (`the-coffee-bar-frontend`). On order request is sent to 
`the-coffee-bar` service. Based on data, order is passed to `the-coffee-machine` which is preparing coffee using 
`machine-svc`, `coffee-svc` and `water-svc`. All money transactions are handled by `the-cashdesk` service which is 
communicating with `calculator-svc` and `postgres` database.

All services are instrumented using [OpenTelemetry](https://opentelemetry.io/) solution.

## Prerequisites

Make sure to finish the [prerequisites](../demo/prerequisites/) first. As a result of that you should have your `SUMOLOGIC_TOKEN` env variable exported:

  ```bash
  export SUMOLOGIC_TOKEN=your-sumologic-token
  ```

Additionally you will need `Docker` and `Docker Compose` installed on your machine:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## The Coffee Bar demo
1. Run `docker-compose up`
1. Navigate to `http://localhost:3000` and make some order
1. Go to Sumo Logic Web App and find your order in [Traces view](https://help.sumologic.com/Traces/02Working_with_Tracing_data/03View_and_investigate_traces)
1. View application logs in [Logs view](https://help.sumologic.com/05Search/Get-Started-with-Search/Search-Basics/About-Search-Basics) or drill down to the specific service log directly from `Trace view` [clicking on the span details](https://help.sumologic.com/Traces/02Working_with_Tracing_data/03View_and_investigate_traces#details-pane) and `Open logs tagged with ...`
