# -*- coding: utf-8 -*-

import logging

import mysql.connector

from odoo import models, fields, _

_logger = logging.getLogger(__name__)


class CatalogueConfiguration(models.TransientModel):
    _name = "catalogue.configuration"
    _description = "Catalogue Configuration"
    _rec_name = "catalogue_db_name"

    enable_catalogue_synch = fields.Boolean(string="Enable Catalogue Synch")
    catalogue_server_address = fields.Char(string="Catalogue Server Address")
    catalogue_db_name = fields.Char(
        string="Catalogue DB Name",
    )
    catalogue_mysql_port = fields.Integer(string="Catalogue MySQL Port", default=3306)
    catalogue_db_username = fields.Char(
        string="Catalogue DB Username",
    )
    catalogue_db_password = fields.Char(
        string="Catalogue DB Password",
    )

    catalogue_server_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("connected", "Connected"),
            ("error", "Error"),
        ],
        string="Catalogue Server Status",
        default="draft",
        readonly=True,
    )

    def test_connection_search(self):
        catalogue_server = self.search([], limit=1)
        return catalogue_server.search_read([], ["catalogue_server_status"])

    def test_connection(self):
        """
        Test the connection to the Catalogue server and update the catalogue_server_status accordingly.
        If the connection is successful, the catalogue_server_status is set to 'connected'.
        If the connection fails, the catalogue_server_status is set to 'error' and a ValidationError is raised.
        """
        if self.enable_catalogue_synch:
            if (
                self.catalogue_server_address
                and self.catalogue_db_name
                and self.catalogue_db_username
                and self.catalogue_db_password
            ):
                # MySQL server connection details
                host = self.catalogue_server_address
                port = self.catalogue_mysql_port
                user = self.catalogue_db_username
                password = self.catalogue_db_password
                database = self.catalogue_db_name

                try:
                    # Create a connection
                    connection = mysql.connector.connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        database=database,
                    )

                    if connection.is_connected():
                        _logger.info("Connection to MySQL server successful")
                        self.catalogue_server_status = "connected"

                    # Close the connection
                    connection.close()

                except mysql.connector.Error as e:
                    _logger.error("An error occurred: %s", e)
                    self.catalogue_server_status = "error"

            else:
                self.catalogue_server_status = "error"

    def run_catalogue_sync(self):
        self_ob = self.search([("catalogue_server_status", "=", "connected")], limit=1)
        self_ob = 1
        if self_ob:
            try:
                # connection_config = {
                #     "host": self_ob.catalogue_server_address,
                #     "port": self_ob.catalogue_mysql_port,
                #     "user": self_ob.catalogue_db_username,
                #     "password": self_ob.catalogue_db_password,
                #     "database": self_ob.catalogue_db_name,
                # }

                connection_config = {
                    "host": "localhost",
                    "port": 3306,
                    "user": "admin",
                    "password": "admin",
                    "database": "catalogue_odoo",
                }

                conn = mysql.connector.connect(**connection_config)
                cursor = conn.cursor()
                self.sync_attributes_and_values(cursor, conn)

            except mysql.connector.Error as err:
                logging.error("\n\n\nConnection error occurred: %s", err)
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

    def all_attribute(self):
        value_list = [
            "iCatalogueID",
            "vPPCPartNo",
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
            "vOilSealPlate",
            "vHeatShield",
            "vNozzleRingAssy",
            "vRepairKitMinor",
            "vRepairKitMajor",
            "vActuator",
            "iInventoryId",
            "vImageFileName",
            "vPartNo",
            "vServicePartNo",
            "vAMTCHRAPartNo",
            "iUserId",
            "dCreatedDate",
            "iEditedUserId",
            "dEditedDate",
            "vEditedComputerName",
            "vLinkedComputerName",
            "vNotes",
            "vEngineSize",
            "vFuelType",
            "vAMTRemanPartNo",
            "vBearingHousing",
            "vSWA",
            "vRotorAssy",
            "vCW",
            "vFitmentKit",
            "vOilSupply",
            "vOilDrainPipe",
            "vAirSupplyHose",
            "vInducer",
            "vExducer",
            "vBlade",
            "vTipHeight",
            "vBore",
            "vLength",
            "vThreadSize",
            "vType",
            "vAMTPartNumber",
            "vPPCPartNo_Prev",
            "vOriginalSKU",
            "vOriginalReman",
        ]

        return value_list

    def table_header(self, table, cursor):
        columns = self.all_attribute()

        # Execute a query to retrieve table information
        query = f"SHOW COLUMNS FROM {table}"
        cursor.execute(query)

        # Fetch all the rows returned by the query
        table_info = cursor.fetchall()

        header_names_with_v = [item[0] for item in table_info]

        matching_values_v = list(filter(lambda x: x in columns, header_names_with_v))

        return matching_values_v

    def sync_attributes_and_values(self, cursor, conn):
        tables = [
            "catalog_turbocharger",
            # "catalog_diesel_injection",
            # "catalog_turbocharger_spares",
            # "catalog_compressor_wheel_size",
        ]

        try:
            for table in tables:
                columns = self.table_header(table, cursor)

                selected_column = ", ".join(columns)

                query_values = f"SELECT {selected_column} FROM {table} WHERE NOT readAttributeValue=1"
                cursor.execute(query_values)

                rows = cursor.fetchall()
                for row in rows[0:3]:
                    row_data = dict(zip(columns, row))
                    iCatalogueID = row_data.pop("iCatalogueID")

                    vPPCPartNo = row_data.pop("vPPCPartNo")

                    with self.env.cr.savepoint():
                        try:
                            for name, value in row_data.items():
                                name = name.lstrip("vid")
                                attribute = self._create_or_get_attribute(name)

                                if value:
                                    if name in [
                                        "Engines",
                                        "OENumber",
                                        "OeTurboPartno",
                                    ]:
                                        value_list = list(set(value.split()))
                                        for data in value_list:
                                            value_obj = self._create_attribute_value(
                                                attribute, data
                                            )

                                            # Create Product:
                                            if vPPCPartNo:
                                                self._create_product(
                                                    vPPCPartNo, attribute, value_obj
                                                )

                                    else:
                                        value_obj = self._create_attribute_value(
                                            attribute, value
                                        )
                                        # Create Product:
                                        if vPPCPartNo:
                                            self._create_product(
                                                vPPCPartNo, attribute, value_obj
                                            )

                            self.update_row_status(iCatalogueID, cursor, conn, table)
                            conn.commit()  # Commit changes for each row

                        except Exception as e:
                            conn.rollback()
                            print("Error:", e)

        except Exception as e:
            print("Outer Error:", e)

    def update_row_status(self, iCatalogueID, cursor, conn, table):
        update_row = (
            f"UPDATE {table} SET readAttributeValue=1 WHERE iCatalogueID={iCatalogueID}"
        )
        cursor.execute(update_row)

    def _create_or_get_attribute(self, column):
        attribute_obj = self.env["product.attribute"]

        return attribute_obj.search(
            [("name", "=", column)], limit=1
        ) or attribute_obj.create(
            {
                "name": column,
                "display_type": "select",
                "create_variant": "no_variant",
            }
        )

    def _create_attribute_value(self, attribute, value):
        attribute_value_obj = self.env["product.attribute.value"]

        value_name = value.strip() if isinstance(value, str) else value

        existing_value = attribute_value_obj.search(
            [
                ("attribute_id", "=", attribute.id),
                ("name", "=", value_name),
            ],
            limit=1,
        )

        if not existing_value:
            existing_value = attribute_value_obj.create(
                {
                    "attribute_id": attribute.id,
                    "name": value_name,
                }
            )
        return existing_value

    def _create_product(self, vPPCPartNo, attribute, value_obj):
        product_obj = self.env["product.template"].search(
            [("name", "=", vPPCPartNo)], limit=1
        )

        if product_obj:
            attribute_line = product_obj.attribute_line_ids.filtered(
                lambda line: line.attribute_id.id == attribute.id
            )

            if not attribute_line:
                attribute_line.create(
                    {
                        "product_tmpl_id": product_obj.id,
                        "attribute_id": attribute.id,
                        "value_ids": [(6, 0, [value_obj.id])],
                    }
                )
            elif value_obj.id not in attribute_line.value_ids.ids:
                attribute_line.write({"value_ids": [(4, value_obj.id)]})

        else:
            self.env["product.template"].create(
                {
                    "name": vPPCPartNo,
                    "attribute_line_ids": [
                        (
                            0,
                            0,
                            {
                                "attribute_id": attribute.id,
                                "value_ids": [(6, 0, [value_obj.id])],
                            },
                        )
                    ],
                }
            )

    # def sync_turbocharger(self, cursor):
    #     tables = [
    #         "catalog_turbocharger",
    #         # "catalog_diesel_injection",
    #         # "catalog_turbocharger_spares",
    #         # "catalog_compressor_wheel_size",
    #     ]

    #     columns = self.all_attribute

    #     Product = self.env["product.template"]

    #     for table in tables:
    #         logging.info(f"Create Product For Table: {table}")

    #         try:
    #             query = f"SELECT vPPCPartNo FROM {table}"
    #             cursor.execute(query)
    #             records = cursor.fetchall()

    #             for record in records[0:10]:
    #                 print("#################", record)
    #                 vPPCPartNo = record[0]
    #                 input()
    #                 if vPPCPartNo:
    #                     try:
    #                         for column in columns:
    #                             new_query = f"SELECT DISTINCT v{column} FROM {table} WHERE vPPCPartNo='{vPPCPartNo}' AND v{column} IS NOT NULL"
    #                             cursor.execute(new_query)
    #                             records = cursor.fetchall()

    #                             values_list = [item[0].strip() for item in records]

    #                             if not values_list:
    #                                 continue

    #                             attribute = self.env["product.attribute"].search(
    #                                 [("name", "=", column)]
    #                             )

    #                             value_ids = self.env["product.attribute.value"].search(
    #                                 [
    #                                     (
    #                                         "attribute_id",
    #                                         "=",
    #                                         attribute.id,
    #                                     ),
    #                                     ("name", "in", values_list),
    #                                 ]
    #                             )

    #                             if not value_ids:
    #                                 continue

    #                             product = Product.search(
    #                                 [("name", "=", vPPCPartNo)], limit=1
    #                             )

    #                             if product:
    #                                 # Search for products with the specified attribute
    #                                 if attribute:
    #                                     old_value_ids = (
    #                                         product.attribute_line_ids.filtered(
    #                                             lambda line: line.attribute_id.id
    #                                             == attribute.id
    #                                         ).value_ids.ids
    #                                     )

    #                                     sorted_value_ids = sorted(old_value_ids)
    #                                     sorted_new_value_ids = sorted(value_ids.ids)

    #                                     if sorted_value_ids == sorted_new_value_ids:
    #                                         continue

    #                                     new_value_ids = list(
    #                                         set(sorted_value_ids)
    #                                         ^ set(sorted_new_value_ids)
    #                                     )

    #                                     if new_value_ids:
    #                                         attribute_line = (
    #                                             product.attribute_line_ids.filtered(
    #                                                 lambda line: line.attribute_id.id
    #                                                 == attribute.id
    #                                             )
    #                                         )
    #                                         if attribute_line:
    #                                             attribute_line.write(
    #                                                 {
    #                                                     "value_ids": [
    #                                                         (
    #                                                             6,
    #                                                             0,
    #                                                             new_value_ids,
    #                                                         )
    #                                                     ]
    #                                                 }
    #                                             )
    #                                         else:
    #                                             attribute_line.create(
    #                                                 {
    #                                                     "product_tmpl_id": product.id,
    #                                                     "attribute_id": attribute.id,
    #                                                     "value_ids": [
    #                                                         (
    #                                                             6,
    #                                                             0,
    #                                                             value_ids.ids,
    #                                                         )
    #                                                     ],
    #                                                 }
    #                                             )

    #                             else:
    #                                 # Create a new product in Odoo
    #                                 Product.create(
    #                                     {
    #                                         "name": vPPCPartNo,
    #                                         "attribute_line_ids": [
    #                                             (
    #                                                 0,
    #                                                 0,
    #                                                 {
    #                                                     "attribute_id": attribute.id,
    #                                                     "value_ids": [
    #                                                         (
    #                                                             6,
    #                                                             0,
    #                                                             value_ids.ids,
    #                                                         )
    #                                                     ],
    #                                                 },
    #                                             )
    #                                         ],
    #                                     }
    #                                 )

    #                     except Exception as e:
    #                         logging.error(f"Error in columns=============> : {e}")
    #                         continue

    #         except Exception as e:
    #             logging.error(f"Error processing================> {table}: {e}")
    #             continue
