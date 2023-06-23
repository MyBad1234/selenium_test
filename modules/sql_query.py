import os
import json
import time

import mysql
from mysql.connector.connection_cext import CMySQLCursor, CMySQLConnection


class TaskMissingException(Exception):
    """if task is not fond"""

    pass


class DataStructException(Exception):
    """if the record has no links"""

    pass


class SqlOrm:
    """all universal query for db and work with exceptions"""

    def __init__(self):
        self.cnx: CMySQLConnection = SqlOrm.reconnect()
        self.repeat_connect = 0

    @staticmethod
    def reconnect():
        """reconnect if there are problems"""

        connect_data = {
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'database': os.environ.get('DB_DATABASE'),
            'raise_on_warnings': True
        }

        return mysql.connector.connect(**connect_data)

    def _select_query(self, query, arguments=None) -> list:
        """universal select query"""

        try:
            cursor: CMySQLCursor = self.cnx.cursor()
            if arguments is None:
                cursor.execute(query)
            else:
                cursor.execute(query, arguments)

        except mysql.connector.errors.OperationalError:
            time.sleep(1)

            # control repeat connection
            if self.repeat_connect == 10:
                raise mysql.connector.errors.OperationalError()

            # repeat connect to db
            self.cnx = SqlQuery.reconnect()
            self.repeat_connect += 1

            # repeat select query
            return self._select_query(query, arguments)

        # if connection is good
        self.repeat_connect = 0

        # get data from query
        data_list = []
        for i in cursor:
            data_list.append(i)

        return data_list

    def _update_query(self, query, arguments=None):
        """universal update query"""

        try:
            cursor: CMySQLCursor = self.cnx.cursor()
            if arguments is None:
                cursor.execute(query)
            else:
                cursor.execute(query, arguments)

            self.cnx.commit()

        except mysql.connector.errors.OperationalError:
            time.sleep(1)

            # control repeat connection
            if self.repeat_connect == 10:
                raise mysql.connector.errors.OperationalError()

            # repeat connect to db
            self.cnx = SqlQuery.reconnect()
            self.repeat_connect += 1

            # repeat select query
            self._update_query(query, arguments)


class SqlQuery(SqlOrm):
    """requests to db for getting task"""

    def __get_new_task(self):
        """get task or make exception"""

        query = ("SELECT `id`,`entity_id`,`resource_id`,`status_id`, `updated` "
                 "FROM `queue` WHERE `type_id` = 10 AND `status_id` = 1 "
                 "ORDER BY id LIMIT 1")

        data_from_query = super()._select_query(query)

        # find company
        data = None
        for i in data_from_query:
            data = {
                'id': i[0],
                'resource_id': i[2],
                'status_id': i[3],
                'entity_id': i[1]
            }

        if data is None:
            raise TaskMissingException()

        return data

    def __get_task_by_id(self, id_queue):
        """get task without status for test"""

        query = ("SELECT `id`,`entity_id`,`resource_id`,"
                 "`status_id`, `updated` FROM queue WHERE id = %s;")

        data_from_request = super()._select_query(query, (str(id_queue),))

        data = None
        for i in data_from_request:
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

        query = "SELECT `keyword`,`coordinates` FROM `user_imitation_yandex` WHERE `id` = %s"

        # make request to db
        data_from_request = super()._select_query(query, (str(resource_id),))

        # get data from this request
        data = None
        for i in data_from_request:
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

        # make request to db
        data_from_request = super()._select_query(query, (str(entity_id),))

        # get data from request
        data = None
        for i in data_from_request:
            data = {
                'name': i[1],
                'x': i[3],
                'y': i[2]
            }

        if data is None:
            raise DataStructException()

        return data

    def update_status_task(self, task_id, status):
        """inform the database that the task is being completed"""

        query = "UPDATE `queue` SET `status_id` = %s, `updated` = %s WHERE `id` = %s"

        super()._update_query(query, (status, str(int(time.time())), task_id))

    def update_status_task_other(self, queue_id, status):
        """update status of clicker"""

        query = ("UPDATE `queue_user_imitation_yandex` "
                 "SET `status_id` = %s, `updated` = %s"
                 " WHERE `queue_id` = %s")

        super()._update_query(query, (status, str(int(time.time())), queue_id))

    def update_stage_task_other(self, queue_id, stage, status=True):
        """update stage of clicker"""

        select_query = ("SELECT `result` FROM queue_user_imitation_yandex "
                        "WHERE `queue_id` = %s")

        data_from_request = super()._select_query(
            select_query, (str(queue_id),)
        )

        # add new stage for log
        log_stage = None
        for i in data_from_request:
            if i[0] is None:
                log_stage = {}
            else:
                log_stage = json.loads(i[0])

        if log_stage is None:
            raise DataStructException()

        log_stage[stage] = status

        # query for update stage
        update_query = ("UPDATE `queue_user_imitation_yandex` "
                        "SET `result` = %s , `updated` = %s "
                        "WHERE `queue_id` = %s")

        super()._update_query(
            update_query, (json.dumps(log_stage), str(int(time.time())), queue_id)
        )

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
            'entity_id': task.get('entity_id'),
            'company': name.get('name'),
            'id_queue': task.get('id'),
            'x': name.get('x'),
            'y': name.get('y')
        }

    def get_data_by_id(self, id_queue):
        """get task by id without status"""

        task = self.__get_task_by_id(id_queue)
        keywords_coordinates = self.__get_keywords_coordinates(
            task.get('resource_id')
        )
        name = self.__get_company(
            task.get('entity_id')
        )

        return {
            'keywords': keywords_coordinates.get('keyword'),
            'entity_id': task.get('entity_id'),
            'company': name.get('name'),
            'id_queue': task.get('id'),
            'x': name.get('x'),
            'y': name.get('y')
        }
