from enum import Enum

import mysql.connector


class Table(Enum):
    HVAC = "hvac"
    HVAC_EVENTS = "hvac_events"


class Crud:
    _instance = None
    connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Crud, cls).__new__(cls)
            cls._instance.init_singleton()
        return cls._instance

    def init_singleton(self):
        # Define database connection parameters
        self.db_params = {
            "database": "ocs",
            "user": "ocs",
            "password": "ocs",
            "host": "localhost",
            "port": "3306",
        }

    def connect(self):
        self.connection = mysql.connector.connect(**self.db_params)

    def insert_metric(self, table: Table, metric_name: str, metric_value: str):
        try:
            cursor = self.connection.cursor()

            match table:
                case Table.KANBAN:
                    insert_query = "INSERT INTO kanban (name, value) VALUES (%s, %s)"

                case Table.VISUALIZATION:
                    insert_query = (
                        "INSERT INTO visualisation (name, value) VALUES (%s, %s)"
                    )

                case Table.PULL_REQUESTS:
                    insert_query = (
                        "INSERT INTO pull_requests (name, value) VALUES (%s, %s)"
                    )

            cursor.execute(insert_query, (metric_name, metric_value))

            # Insert a new metric
            self.connection.commit()
            print("metric inserted successfully!")

        except Exception as e:
            print(f"Error creating metric: {e}")

        finally:
            cursor.close()

    def read_metrics(self, table: Table):
        try:
            cursor = self.connection.cursor()

            match table:
                case Table.KANBAN:
                    select_query = "SELECT * FROM kanban"

                case Table.VISUALIZATION:
                    select_query = "SELECT * FROM visualisation"

                case Table.PULL_REQUESTS:
                    select_query = "SELECT * FROM pull_requests"

            # Select all metrics
            cursor.execute(select_query)

            metrics = cursor.fetchall()
            for metric in metrics:
                print(metric)

        except Exception as e:
            print(f"Error reading metrics: {e}")

        finally:
            cursor.close()

    def update_metric(self, table: Table, metric_id, new_value):
        try:
            cursor = self.connection.cursor()

            match table:
                case Table.KANBAN:
                    update_query = "UPDATE kanban SET value = %s WHERE id = %s"

                case Table.VISUALIZATION:
                    update_query = "UPDATE visualisation SET value = %s WHERE id = %s"

                case Table.PULL_REQUESTS:
                    update_query = "UPDATE pull_requests SET value = %s WHERE id = %s"

            # Update a metric by metric_id
            cursor.execute(update_query, (new_value, metric_id))
            self.connection.commit()

            print("Metric updated successfully!")

        except Exception as e:
            print(f"Error updating metric: {e}")

        finally:
            cursor.close()

    def delete_metric(self, table: Table, metric_id):
        try:
            cursor = self.connection.cursor()

            match table:
                case Table.KANBAN:
                    delete_query = "DELETE FROM kanban WHERE id = %s"

                case Table.VISUALIZATION:
                    delete_query = "DELETE FROM visualisation WHERE id = %s"

                case Table.PULL_REQUESTS:
                    delete_query = "DELETE FROM pull_requests WHERE id = %s"

            cursor.execute(delete_query, (metric_id,))
            self.connection.commit()

            print("Metric deleted successfully!")

        except Exception as e:
            print(f"Error deleting metric: {e}")

        finally:
            cursor.close()

    def close_connection(self):
        self.connection.close()
