import os
import mysql
from mysql.connector.connection_cext import CMySQLCursor, CMySQLConnection


class TaskMissingException(Exception):
    """if task is not fond"""

    pass


class DataStructException(Exception):
    """if the record has no links"""

    pass


class SqlQuery:
    """query for tasks"""

    def __init__(self):
        connect_data = {
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'database': os.environ.get('DB_DATABASE'),
            'raise_on_warnings': True
        }

        self.cnx: CMySQLConnection = mysql.connector.connect(**connect_data)

    def __get_new_task(self):
        """get task or make exception"""

        query = ("SELECT `id`,`entity_id`,`resource_id`,`status_id`, `updated` "
                "FROM `queue` WHERE `type_id` = 10 AND `status_id` = 1 "
                "ORDER BY id LIMIT 1")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query)

        # find company
        data = None
        for i in cursor:
            data = {
                'id': i[0],
                'resource_id': i[2],
                'status_id': i[3],
                'entity_id': i[1]
            }

        if data is None:
            raise TaskMissingException()

        return data

    def __get_keywords_coordinates(self, resource_id):
        """get keywords and coordinates for task"""

        query = ("SELECT `keyword`,`coordinates` FROM `user_imitation_yandex` WHERE `id` = %s")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query, (str(resource_id),))

        data = None
        for i in cursor:
            data = {
                'keyword': i[0],
                'coordinates': i[1]
            }

        if data is None:
            raise DataStructException()

        return data

    def __get_company(self, entity_id):
        """get company for search"""

        query = ("SELECT `yandex_id`,`name`,`latitude`,`longitude` "
                 "FROM `itemcampagin` WHERE `id` = %s")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query, (str(entity_id),))

        data = None
        for i in cursor:
            data = {
                'name': i[1]
            }

        if data is None:
            raise DataStructException()

        return data

    def __get_second_task(self, ):
        """find the child element of the task"""

        query = ("SELECT `status_id`,`result`,`updated` FROM `queue_user_imitation_yandex` "
                "WHERE `queue_id` = id")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query)

    def test(self):
        query = "UPDATE `queue` SET `status_id` = 1 WHERE`type_id` = 10"

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query)

        self.cnx.commit()

    def update_status_task(self, task_id, status, time):
        """inform the database that the task is being completed"""

        query = "UPDATE `queue` SET `status_id` = %s, `updated` = %s WHERE `id` = %s"

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query, (status, time, task_id))

        self.cnx.commit()



    def update_status_task_other(self, queue_id, time):
        """update status of clicker"""

        query = "UPDATE `queue_user_imitation_yandex` SET `status_id` = 2 WHERE `queue_id` = %s"

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(query, (str(queue_id),))

        self.cnx.commit()

    def update_stage_task_other(self, queue_id, time, stage):
        """update stage of clicker"""

        select_query = ("SELECT `result` FROM queue_user_imitation_yandex "
                        "WHERE `queue_id` = %s")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(select_query, (str(queue_id),))

        # add new stage for log
        log_stage = None
        for i in cursor:
            log_stage = i[0]

        if log_stage is None:
            raise DataStructException()

        log_stage += " "
        log_stage += stage

        # query for update stage
        update_query = ("UPDATE `queue_user_imitation_yandex` "
                        "SET `result` = %s , `updated` = %s "
                        "WHERE `queue_id` = %s")

        cursor: CMySQLCursor = self.cnx.cursor()
        cursor.execute(update_query, (log_stage, time, queue_id))

        self.cnx.commit()


    def get_data(self):
        """get all data from requests to db"""

        task = self.__get_new_task()
        keywords_coordinates = self.__get_keywords_coordinates(
            task.get('resource_id')
        )
        name = self.__get_company(
            task.get('entity_id')
        )

        return {
            'keywords': keywords_coordinates.get('keyword'),
            'company': name.get('name'),
            'id_queue': task.get('id')
        }
