import base64
import io
import pandas as pd
from datetime import datetime

from odoo import models, fields
from odoo.exceptions import UserError


class TailorOrderImportWizard(models.TransientModel):
    _name = "tailor.order.import.wizard"
    _description = "Ultimate Import (CSV/XLS/XLSX)"

    file = fields.Binary("Upload File", required=True)
    filename = fields.Char("File Name")

    # -------------------------------------------------
    # DATE PARSER
    # -------------------------------------------------
    def _parse_date(self, value):
        if not value:
            return False

        if isinstance(value, pd.Timestamp):
            return value.date()

        if isinstance(value, datetime):
            return value.date()

        try:
            return pd.to_datetime(value, dayfirst=True).date()
        except Exception:
            raise UserError(f"Invalid Date Format: {value}")

    # -------------------------------------------------
    # GOD MODE SELECTION MAPPER
    # -------------------------------------------------
    def _map_dynamic_selection(self, model_name, field_name, value):

        if not value:
            return False

        value = str(value).strip().lower()

        field = self.env[model_name]._fields[field_name]

        if not field.selection:
            return False

        for key, label in field.selection:

            key_clean = str(key).strip().lower()
            label_clean = str(label).strip().lower()

            # exact key match
            if value == key_clean:
                return key

            # exact label match
            if value == label_clean:
                return key

            # partial safe match
            if value in key_clean:
                return key

            if value in label_clean:
                return key

        return False

    # -------------------------------------------------
    # MAIN IMPORT
    # -------------------------------------------------
    def action_import_file(self):

        if not self.file:
            raise UserError("Please upload file")

        if not self.filename:
            raise UserError("File name missing")

        file_data = base64.b64decode(self.file)

        # ---------- READ FILE ----------
        try:
            ext = (self.filename or '').lower().split(".")[-1]
            df = None

            if ext == "csv":
                encodings = ['utf-8', 'cp1252', 'latin1']

                for enc in encodings:
                    try:
                        df = pd.read_csv(
                            io.BytesIO(file_data),
                            encoding=enc,
                            on_bad_lines='skip'
                        )
                        break
                    except UnicodeDecodeError:
                        continue

                if df is None:
                    raise UserError("Unable to read CSV file. Please upload valid CSV.")

            elif ext == "xlsx":
                df = pd.read_excel(io.BytesIO(file_data), engine="openpyxl")

            elif ext == "xls":
                df = pd.read_excel(io.BytesIO(file_data), engine="xlrd")

            else:
                raise UserError("Allowed file types: CSV, XLS, XLSX")

        except Exception as e:
            raise UserError(f"File Read Error:\n{str(e)}")

        if df.empty:
            raise UserError("File contains no data")

        if df.empty:
            raise UserError("File contains no data")

        df = df.fillna("")

        TailorOrder = self.env["tailor.order"]
        Customer = self.env["tailor.customer"]

        # ---------- LOOP ----------
        for index, row in df.iterrows():
            line_no = index + 1 
            try:
                # CUSTOMER
                customer_name = row.get("Customer Name")
                if not customer_name:
                    continue

                customer = Customer.search(
                    [("name", "=", customer_name)],
                    limit=1
                )

                if not customer:
                    customer = Customer.create({
                        "name": customer_name
                    })

                # DATE
                delivery_date_raw = row.get("Delivery Date")

                if not delivery_date_raw:
                    continue  # skip this row

                try:
                    delivery_date = self._parse_date(delivery_date_raw)
                except Exception:
                    continue

                # LOOKUPS
                pant_type = self.env["tailor.pant.type"].search(
                    [("name", "=", row.get("Pants/Pant Type"))],
                    limit=1,
                )

                pant_style = self.env["tailor.pant.style"].search(
                    [("name", "=", row.get("Pants/Pant Style"))],
                    limit=1,
                )

                silai_type = self.env["tailor.silayi.type"].search(
                    [("name", "=", row.get("Pants/Silai Type"))],
                    limit=1,
                )

                shirt_style = self.env["tailor.shirt.type"].search(
                    [("name", "=", row.get("Shirts/Shirt Style"))],
                    limit=1,
                )

                # ORDER
                order_vals = {
                    "customer_id": customer.id,
                    "phone": row.get("Phone"),
                    "address": row.get("Customer Address"),
                    "delivery_date": delivery_date,
                    "state": "delivered",
                    "note": str(line_no),
                }

                # PANT LINE
                pant_vals = {
                    "pant_type_id": pant_type.id if pant_type else False,
                    "pant_style_id": pant_style.id if pant_style else False,
                    "silai_type_id": silai_type.id if silai_type else False,
                    "pant_qty": row.get("Pants/Pant Quantity") or 1,
                    "pant_lambai": row.get("Pants/Lambai"),
                    "pant_kamar": row.get("Pants/Kamar"),
                    "pant_sit": row.get("Pants/Sit"),
                    "pant_jang": row.get("Pants/Jang"),
                    "pant_bottom": row.get("Pants/Bottom"),
                    "pant_kistak": row.get("Pants/Kistak"),
                    "pant_guthna": row.get("Pants/Guthna"),
                    "pant_front_pocket": self._map_dynamic_selection(
                        "tailor.order.pants",
                        "pant_front_pocket",
                        row.get("Pants/Front Pocket"),
                    ),
                    "pant_back_pocket": self._map_dynamic_selection(
                        "tailor.order.pants",
                        "pant_back_pocket",
                        row.get("Pants/Back Pocket"),
                    ),
                }

                # SHIRT LINE
                shirt_vals = {
                    "shirt_style_id": shirt_style.id if shirt_style else False,
                    "shirt_qty": row.get("Shirts/Shirt Quantity") or 1,
                    "shirt_lambai": row.get("Shirts/Lambai"),
                    "shirt_chati": row.get("Shirts/Chati"),
                    "shirt_shoulder": row.get("Shirts/Shoulder"),
                    "shirt_aastin": row.get("Shirts/Aastin"),
                    "shirt_gala": row.get("Shirts/Gala"),
                    "shirt_peat": row.get("Shirts/Peat"),
                    "shirt_front": row.get("Shirts/Front"),
                    "shirt_patti": self._map_dynamic_selection(
                        "tailor.order.shirts",
                        "shirt_patti",
                        row.get("Shirts/Patti"),
                    ),
                    "others": self._map_dynamic_selection(
                        "tailor.order.shirts",
                        "others",
                        row.get("Shirts/Patti Type"),
                    ),
                    "shirt_collar": row.get("Shirts/Collar"),
                    "shirt_a": row.get("Shirts/A"),
                    # "notes": row.get("Shirts/Notes"),
                }

                order_vals["pant_ids"] = [(0, 0, pant_vals)]
                order_vals["shirt_ids"] = [(0, 0, shirt_vals)]

                TailorOrder.create(order_vals)

            except Exception as e:
                raise UserError(
                    f"Error in Row {index + 2}\n\n{str(e)}"
                )

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
