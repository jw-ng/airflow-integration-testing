import json
import os
import time

import requests
from requests.auth import HTTPBasicAuth


class AirflowAPI:
    def __init__(self):
        self.api_url = f"http://airflow-web:8080/api/v1"

        airflow_admin_username = os.getenv("AIRFLOW_ADMIN_USERNAME")
        airflow_admin_password = os.getenv("AIRFLOW_ADMIN_PASSWORD")
        self.http_basic_auth = HTTPBasicAuth(
            airflow_admin_username,
            airflow_admin_password,
        )

    def trigger_dag(self, dag_id: str, run_id: str, conf: dict = None):
        _conf = conf or {}
        self.unpause_dag(dag_id)

        response = requests.post(
            url=f"{self.api_url}/dags/{dag_id}/dagRuns",
            auth=self.http_basic_auth,
            json={"dag_run_id": run_id, "conf": _conf},
        )
        if not response.ok:
            raise RuntimeError(f"Unable to trigger DAG {dag_id}: {response.reason}")

    def unpause_dag(self, dag_id: str):
        response = requests.patch(
            url=f"{self.api_url}/dags/{dag_id}?update_mask=is_paused",
            auth=self.http_basic_auth,
            json={"is_paused": False},
        )
        if not response.ok:
            raise RuntimeError(f"Unable to unpause {dag_id}: {response.reason}")

    def wait_for_dag_to_complete(
        self,
        dag_id: str,
        run_id: str,
        timeout_in_sec: int = 120,
    ):
        until = time.time() + timeout_in_sec
        while time.time() <= until:
            time.sleep(1)

            if not self._is_dag_running(dag_id=dag_id, run_id=run_id):
                return

        raise Exception(
            f"Dag {dag_id} (with run_id: {run_id}) did not complete in {timeout_in_sec} seconds"
        )

    def _is_dag_running(self, dag_id: str, run_id: str) -> bool:
        response = requests.get(
            url=f"{self.api_url}/dags/{dag_id}/dagRuns/{run_id}",
            auth=self.http_basic_auth,
        )
        json_response = json.loads(response.text)
        return json_response.get("state", None) == "running"

    def create_connection(
        self,
        conn_id: str,
        conn_type: str,
        host: str = None,
        login: str = None,
        password: str = "UNDEFINED",
        schema: str = None,
        port: int = None,
        extra: str = None,
    ):
        self.delete_connection(conn_id=conn_id)

        response = requests.post(
            url=f"{self.api_url}/connections",
            auth=self.http_basic_auth,
            json={
                "connection_id": conn_id,
                "conn_type": conn_type,
                "host": host,
                "login": login,
                "schema": schema,
                "port": port,
                "password": password,
                "extra": extra,
            },
        )
        if not response.ok:
            raise RuntimeError(f"Unable to create connection '{conn_id}': {response.reason}")

    def delete_connection(self, conn_id: str):
        response = requests.delete(
            url=f"{self.api_url}/connections/{conn_id}",
            auth=self.http_basic_auth,
        )
        if response.status_code == 404:
            return
        if not response.ok:
            raise RuntimeError(f"Unable to delete connection '{conn_id}: {response.reason}")

