from airflow.models import BaseOperator
from airflow.models.taskinstance import Context
from airflow.providers.mongo.hooks.mongo import MongoHook

from dags.constants import DOCUMENT_STORE_COLLECTION_NAME


class ProcessDocumentOperator(BaseOperator):
    def __init__(self, document_store_connection_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_store_connection_id = document_store_connection_id

    def execute(self, context: Context):
        mongo_hook = MongoHook(conn_id=self.document_store_connection_id)
        source_name = context["dag_run"].conf["source_name"]

        mongo_hook.update_one(
            mongo_collection=DOCUMENT_STORE_COLLECTION_NAME,
            filter_doc={"source": source_name},
            update_doc={"$set": {"processed": True}},
        )
