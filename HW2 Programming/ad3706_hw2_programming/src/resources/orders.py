import pymysql
import json

from src.resources.base_resource import Base_Resource

class Orders(Base_Resource):

    def __init__(self):
        super().__init__()
        self.db_schema = 'classicmodels'
        self.db_table = 'orders'
        self.db_table_full_name = self.db_schema + "." + self.db_table
        self.primary_key_field = 'orderNumber'

    def _get_connection(self):
        """
        # DFF TODO There are so many anti-patterns here I do not know where to begin.
        :return:
        """

        # DFF TODO OMG. Did this idiot really put password information in source code?
        # Sure. Let's just commit this to GitHub and expose security vulnerabilities
        #
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="dbuserdbuser",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    def get_resource_by_id(self, id):
        """
        # DFF TODO Will the anti-patterns never end?
        :return:
        """

        sql = "select * from " + self.db_table_full_name + " where orderNumber=%s"
        conn = self._get_connection()
        cursor = conn.cursor()

        the_sql = cursor.mogrify(sql, (id))
        print("The sql = ", the_sql)

        res = cursor.execute(sql, (id))

        if res == 1:
            result = cursor.fetchone()
        else:
            result = None

        return result


    def get_by_template(self,
                        path=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None):
        """
        This is a logical abstraction of an SQL SELECT statement.

        Ignore path for now.

        Assume that
            - template is {'customerNumber': 101, 'status': 'Shipped'}
            - field_list is ['customerNumber', 'orderNumber', 'status', 'orderDate']
            - self.get_full_table_name() returns 'classicmodels.orders'
            - Ignore limit for now
            - Ignore offset for now

        This method would logically execute

        select customerNumber, orderNumber, status, orderDate
            from classicmodels.orders
            where
                customerNumber=101 and status='Shipped'

        :param path: The relative path to the resource. Ignore for now.
        :param template: A dictionary of the form {key: value} to be converted to a where clause
        :param field_list: The subset of the fields to return.
        :param limit: Limit on number of rows to return.
        :param offset: Offset in the list of matching rows.
        :return: The rows matching the query.
        """
        field_str = ""
        for x in field_list:
            field_str += (x + ",")

        template_str = ""
        for (key,val) in template.items():
            template_str += (key + "='" + str(val) + "' and ")

        sql = "select " + field_str[0:len(field_str)-1] + " from " + self.db_table_full_name + " where " + template_str[0:len(template_str)-5]
        conn = self._get_connection()
        cursor = conn.cursor()

        the_sql = cursor.mogrify(sql)
        print("The sql = ", the_sql)

        res = cursor.execute(sql)

        if res > 0:
            result = cursor.fetchall()
        else:
            result = None

        return result

    def create(self, new_resource):
        """

        Assume that
            - new_resource is {'orderNumber': 101, 'status': 'Shipped'} #need a primary key
            - self.get_full_table_name() returns 'classicmodels.orders'

        This function would logically perform

        insert into classicmodels.orders(customerNumber, status)
            values(101, 'Shipped')

        :param new_resource: A dictionary containing the data to insert.
        :return: Returns the values of the primary key columns in the order defined.
            In this example, the result would be [101]
        """
        columns = ', '.join(new_resource.keys())

        values_str = ""
        for val in new_resource.values():
            values_str += ("'" + str(val) + "', ")

        sql = "insert into " + self.db_table_full_name + "(" + columns + ") values(" + values_str[0:len(values_str)-2] + ")"
        conn = self._get_connection()
        cursor = conn.cursor()

        the_sql = cursor.mogrify(sql)
        print("The sql = ", the_sql)

        res = cursor.execute(sql)

        if res:
            result = new_resource["orderNumber"]
            print(result)
        else:
            result = None

        return result

    def update_resource_by_id(self, id, new_values):
        """
        This is a logical abstraction of an SQL UPDATE statement.

        Assume that
            - id is 30100
            - new_values is {'customerNumber': 101, 'status': 'Shipped'}
            - self.get_full_table_name() returns 'classicmodels.orders'

        This method would logically execute.

        update classicmodels.orders
            set customerNumber=101, status=shipped
            where
                orderNumber=30100


        :param id: The 'primary key' of the resource to update
        :new_values: A dictionary defining the columns to update and the new values.
        :return: 1 if a resource was updated. 0 otherwise.
        """

        new_val_str = ""
        for (key,val) in new_values.items():
            new_val_str += (key + "='" + str(val) + "', ")

        sql = "update " + self.db_table_full_name + " set " + new_val_str[0:len(new_val_str)-2] + " where orderNumber=%s"
        print(sql)
        conn = self._get_connection()
        cursor = conn.cursor()

        the_sql = cursor.mogrify(sql, (id))
        print("The sql = ", the_sql)

        res = cursor.execute(sql, (id))

        if res == 1:
            result = 1
        else:
            result = 0

        return result

    def delete_resource_by_id(self, id):
        """
        This is a logical abstraction of an SQL DELETE statement.

        Assume that
            - id is 30100
            - new_values is {'customerNumber': 101, 'status': 'Shipped'}

        This method would logically execute.

        delete from classicmodels.orders
            where
                orderNumber=30100


        :param id: The 'primary key' of the resource to delete
        :return: 1 if a resource was deleted. 0 otherwise.
        """

        sql = "delete from " + self.db_table_full_name + " where orderNumber=%s"
        conn = self._get_connection()
        cursor = conn.cursor()

        the_sql = cursor.mogrify(sql, (id))
        print("The sql = ", the_sql)

        res = cursor.execute(sql, (id))

        if res == 1:
            result = 1
        else:
            result = 0

        return result


if __name__ == "__main__":

    o = Orders() # made order
    res = o.get_resource_by_id('10101')
    print("Result = \n",
          json.dumps(res, indent=2, default=str))