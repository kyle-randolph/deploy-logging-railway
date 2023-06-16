#!/usr/local/bin/python3
import unittest
from railway_gql_query import ( 
        build_graph_query, 
        open_subscription_stream
)

auth_token = "777a123b-c4d5-6fg7-8h90-1ij2klmno345"
deployment_id = "777a123b-c4d5-6fg7-8h90-1ij2klmno345"
file_name = "railwayDeploymentLogging.log"

class RailwayGQLTests(unittest.TestCase):
    def test_build_graph_query(self):
        with self.assertRaises(TypeError):
            build_graph_query()

    def test_open_subscription_stream_one(self):
        with self.assertRaises(TypeError):
            open_subscription_stream()

    def test_open_subscription_stream_two(self):
        gql_client, gql_query = build_graph_query(auth_token, deployment_id)
        with self.assertRaises(Exception):
            open_subscription_stream(gql_client, gql_query, file_name)


if __name__ == '__main__':
    unittest.main()