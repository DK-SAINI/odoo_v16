# -*- coding: utf-8 -*-

from odoo import models, fields, api

import mysql.connector
import traceback


class ProductMysql(models.Model):
    _name = "product.mysql"
    _description = "product.mysql"

    def connect_to_mysql(self):
        # Establish MySQL connection
        mysql_config = {
            "user": "admin",
            "password": "admin",
            "host": "localhost",
            "port": "3306",
            "database": "catalogue_odoo",
        }

        try:
            conn = mysql.connector.connect(**mysql_config)
            # Create a cursor
            cursor = conn.cursor()
            self.create_attribute_and_value(cursor, conn)

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            if conn.is_connected():
                # Now you can execute SQL queries using the `conn` connection object
                conn.close()  # Close the connection when done

    def all_columns(self):
        values_list = [
            "iCatalogueID",
            "vPPCPartNo",
            # "vPartNo",
            "vMarket",
            "vMake",
            "vModel",
            "vYear",
            "vHP",
            "vEngines",
            "vOENumber",
            "vPPCTurboMake",
            "vOeTurboMake",
            "vOeTurboPartno",
            "vTurboModel",
            "vKit",
            "vCompW",
            "vWS",
            "vBHousing",
            "vBackPlate",
            "iInventoryId",
            "vImageFileName",
            "vAMTCHRAPartNo",
            "iUserId",
            "dCreatedDate",
            "iEditedUserId",
            "dEditedDate",
            "vEditedComputerName",
            "vLinkedComputerName",
            "vNotes",
            "vPPCPartNo_Prev",
            "vEngineSize",
            "vFuelType",
            "vAMTRemanPartNo",
            "vServicePartNo",
        ]

        return values_list

    def create_attribute_and_value(self, cursor, conn):
        columns = self.all_columns()

        values = " ,".join(columns)

        # Execute a SELECT query
        query = (
            f"SELECT {values} FROM catalog_turbocharger WHERE NOT readAttributeValue=1"
        )
        cursor.execute(query)

        columns.pop(0)
        columns.pop(0)

        # Fetch all rows
        rows = cursor.fetchall()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", len(rows))

        for row in rows[:100]:
            try:
                data = list(row)

                iCatalogueID = data.pop(0)
                vPPCPartNo = data.pop(0)

                for i, value in enumerate(data):
                    if not value:
                        value = "-"

                    column_name = columns[i]

                    attribute_obj = self.env["product.attribute"].search(
                        [("name", "=", column_name)], limit=1
                    )

                    if not attribute_obj:
                        attribute_obj = self.env["product.attribute"].create(
                            {
                                "name": column_name,
                                "create_variant": "no_variant",
                                "display_type": "select",
                            }
                        )

                    if attribute_obj:
                        domain = [
                            ("name", "=", value),
                            ("attribute_id", "=", attribute_obj.id),
                        ]
                        attribute_value_obj = self.env[
                            "product.attribute.value"
                        ].search(domain, limit=1)

                        if column_name in ["vEngines", "vOENumber", "vOeTurboPartno"]:
                            continue

                        if not attribute_value_obj:
                            attribute_value_obj = self.env[
                                "product.attribute.value"
                            ].create({"name": value, "attribute_id": attribute_obj.id})

                self.update_row_status(iCatalogueID, cursor, conn)
                conn.commit()  # Commit changes for each row

            except Exception as e:
                print("Error processing row:", e)
                traceback.print_exc()

    def update_row_status(self, iCatalogueID, cursor, conn):
        update_row = f"UPDATE catalog_turbocharger SET readAttributeValue=1 WHERE iCatalogueID={iCatalogueID}"
        cursor.execute(update_row)
