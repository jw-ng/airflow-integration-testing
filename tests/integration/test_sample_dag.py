from datetime import datetime
from unittest.mock import ANY

from dags.sample_dag import DAG_ID as sample_dag_id


class TestSampleDag:
    def test_happy_path(
        self,
        setup_airflow_connections,
        airflow_api,
        document_store_mongo_collection,
    ):
        document_store_mongo_collection.delete_many({"source": "some_source"})
        document_store_mongo_collection.insert_one(
            {
                "source": "some_source",
                "date": "2021-12-10",
                "value": 42,
            }
        )

        run_id = f'test_run_id_{datetime.now().strftime("%d%m%Y-%H%M%S")}'
        airflow_api.trigger_dag(
            dag_id=sample_dag_id,
            run_id=run_id,
            conf={"source_name": "some_source"},
        )
        airflow_api.wait_for_dag_to_complete(
            dag_id=sample_dag_id,
            run_id=run_id,
        )

        (document,) = document_store_mongo_collection.find(
            {"source": "some_source"}
        ).limit(1)
        assert document == {
            "_id": ANY,
            "source": "some_source",
            "date": "2021-12-10",
            "value": 42,
            "processed": True,
        }
