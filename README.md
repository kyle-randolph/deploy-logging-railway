# deploy-logging-railway
deploy-logging-railway is an open source Python tool designed to stream logs from a Railway deployment to a text file.

## Overview
This script facilitates the extraction of logs from a running application deployment, enabling efficient debugging.  
Currently this script is set to the scope of a single deployment. Once properly set up and authorized, the script creates a new file named `railwayDeploymentLogging.log`, which contains the output of the gathered deployment logs as they become available.

## Prerequisites
Before using this tool, ensure the following has been completed:
1. Enrolled in the [Priority Boarding Beta](https://docs.railway.app/reference/priority-boarding)
to collect deployment logging.
2. Generate an API token to programmatically interact with your Railway instance. 
Follow the instructions [here](https://docs.railway.app/reference/public-api) to generate the token.
3. Obtain your Deployment ID, which is required to retrieve a running stream of logs. You can find it in the Railway 
Dashboard by navigating to YOUR_PROJECT -> YOUR_ENVIRONMENT -> TARGET_SERVICE -> Deployments -> View Logs, and selecting 
the UUID adjacent to the project. ([Here's](https://github.com/kyle-randolph/deploy-logging-railway/assets/20173512/1849086a-dcd1-4840-8d51-730c54c7239f) a short video showing exactly where to get the Deployment ID)
5. Ensure that the system running this script has Python@3.7 installed
6. This script leverages the gql library to establish a websocket connection 
to log streaming. Refer to the installation instructions [here](https://github.com/graphql-python/gql#installation) 

## Implementation Notes
This script leverages the [gql library](https://gql.readthedocs.io/en/stable/index.html)
to execute queries against the GraphQL API. Specifically, it establishes a websocket connection using gpl to create a 
subscription in GraphQL, allowing for continuous log streaming. 
After creating the websocket, the script creates instance of the Client 
class and leverages the subscribe method to receive a stream of deployment logs from the service. The script then 
iterates through the results and writes them to a file.

## Next Steps
If you wish to extend on the capabilities of the script, you can review the 
[API](https://backboard.railway.app/graphql/v2) using introspection in Postman or 
Insomnia to explore the rest of the querying schema. You can also experiment with queries using our browser-based playground [here](https://railway.app/graphiql)

Currently, the Deployment ID and API Key (authorization token) are saved in clear-text within the script. It is 
recommended to pass the Deployment ID as a parameter to the script to make it easier to store logs from different 
deployments. Furthermore, for enhanced security, consider storing the API key encrypted on the system and decrypt it when 
used by this script.
