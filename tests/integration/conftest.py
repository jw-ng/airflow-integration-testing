import pytest
import requests
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from dags.constants import DOCUMENT_STORE_CONNECTION_ID
from tests.integration.airflow_api import AirflowAPI


@pytest.fixture
def setup_airflow_connections(wait_for_airflow, airflow_api):
    airflow_api.create_connection(
        conn_id=DOCUMENT_STORE_CONNECTION_ID,
        conn_type="mongodb",
        host="airflow-mongodb",
        port=27017,
        schema="local",
    )


@pytest.fixture
def wait_for_airflow() -> requests.Session:
    api_url = f"http://airflow-web:8080/health"
    return assert_container_is_ready(api_url)


@pytest.fixture
def airflow_api():
    return AirflowAPI()


@pytest.fixture
def document_store_mongo_collection(mongo_database):
    return mongo_database.document_store


@pytest.fixture
def mongo_database():
    mongo_client = MongoClient(f"mongodb://airflow-mongodb:27017")
    database = mongo_client.local
    return database


def assert_container_is_ready(readiness_check_url) -> requests.Session:
    request_session = requests.Session()
    retries = Retry(
        total=20,
        backoff_factor=0.2,
        status_forcelist=[404, 500, 502, 503, 504],
    )
    request_session.mount("http://", HTTPAdapter(max_retries=retries))
    assert request_session.get(readiness_check_url)
    return request_session
