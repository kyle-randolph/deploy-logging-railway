#!/usr/local/bin/python3

try:
    import sys
    from gql import gql, Client
    from gql.transport.websockets import WebsocketsTransport
except ImportError as e:
    print("Error importing modules:", e)
    sys.exit(1)

# The file name for logs to be written to
file_name = "railwayDeploymentLogging.log"

# The authorization token to complete api requests.
authorization_token = "AUTH_TOKEN"

# The UUID tied for a deployment to a given environment and project to be logged
deployment_id = "DEPLOYMENT_ID"

def build_graph_query(authorization_token, deployment_id):
    # graphql_ws generates an instance of the WebsocketsTransport class containing the target 
    # websocket URL and any required headers.
    graphql_ws = WebsocketsTransport(
        url = "wss://backboard.railway.app/graphql/v2", 
        headers = {
            "Authorization": "Bearer %s"%(authorization_token),
            "Content-Type": "application/json",
            }
    )
    # Construct Client class using the preceding transport. This is the main entrypoint for
    # executing GraphQL requests.
    try:
        gql_client = Client(
            transport = graphql_ws,
            fetch_schema_from_transport = True,
        )
    except Exception as e:
        print("Error creating the GraphQL client:", e)
        sys.exit(1)

    # The query string listed here is using a subscription. This allows for the continous reading of
    # changes to the deployment logs for running applications.
    try:
        gql_query = gql("""
        subscription DeploymentLogs {
            deploymentLogs(deploymentId: "%s") {
                timestamp
                message
                severity
            }
        }
        """%(deployment_id))
    except Exception as e:
        print("Error creating the GraphQL query string: ", e)
        sys.exit(1)
    except GraphQLError as e:
        print("Syntax error in GraphQL string: ", e)
        sys.exit(1)
    return gql_client, gql_query

def open_subscription_stream(gql_client, gql_query, file_name):
    # As we're getting results back from the query to deployment logs, we're writing them to 
    # the set logging file. This way, the file can be tailed or watched to assist in debugging efforts. 
    try:
        for result in gql_client.subscribe(gql_query):
            try:
                with open(file_name, "a") as file:
                    file.write(str(result) + '\n')
            except IOError as e:
                print("Error opening or writing to the log file:", e)
    except Exception as e:
        print("Error in the GraphQL subscription:", e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
        sys.exit(0)
    finally:
        file.close()

if __name__ == '__main__':
    gql_client, gql_query = build_graph_query(authorization_token, deployment_id)
    open_subscription_stream(gql_client, gql_query, file_name)