from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from django.conf import settings

client = Client(
    transport=RequestsHTTPTransport(url='http://localhost:8001/graphql'),
    fetch_schema_from_transport=True,
)