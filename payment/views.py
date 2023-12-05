import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from django.template.loader import get_template
import pdfkit
import qrcode
from rest_framework import status
from my_project import settings

from .models import Item


class CashMachineView(APIView):
    def get(self, request, filename, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        return FileResponse(open(file_path, "rb"), content_type="application/pdf")

    def post(self, request, *args, **kwargs):
        id_lis = request.data.get("items", [])
        items = Item.objects.filter(id__in=id_lis)
        total_quantity = len(items)
        total_cost = sum(item.price for item in items)

        # Создаем макет пдф чека
        receipt_data = {
            "items": items,
            "total_quantity": total_quantity,
            "total_cost": total_cost,
            "time": "22.03.2023 13:45",
        }
        html_template = get_template(
            r"C:\Users\vladi\Desktop\cash machine\payment\templates\receipt_template.html"
        )
        html_content = html_template.render(receipt_data)
        pdf_file_path = r"payment\media\receipt.pdf"
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_string(html_content, pdf_file_path, configuration=config)

        # Генерируем qr код
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"http://127.0.0.1:8000/{pdf_file_path}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = r"C:\Users\vladi\Desktop\cash machine\payment\media\qrcode.png"
        img.save(img_path)

        return Response({"qr_code_path": img_path}, status=status.HTTP_201_CREATED)
