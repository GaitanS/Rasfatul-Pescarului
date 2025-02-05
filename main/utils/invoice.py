from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os
from datetime import datetime

class InvoiceGenerator:
    def __init__(self, order):
        self.order = order
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4

    def _header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(2*cm, self.height - 2*cm, settings.COMPANY_NAME)
        
        # Company details (top right)
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(self.width - 2*cm, self.height - 2*cm, f"CUI: {settings.COMPANY_VAT}")
        canvas.drawRightString(self.width - 2*cm, self.height - 2.5*cm, f"Reg. Com.: {settings.COMPANY_REG}")
        canvas.drawRightString(self.width - 2*cm, self.height - 3*cm, settings.COMPANY_ADDRESS)
        canvas.drawRightString(self.width - 2*cm, self.height - 3.5*cm, settings.COMPANY_PHONE)
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2*cm, 2*cm, f"Document generat la: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        canvas.drawCentredString(self.width/2, 2*cm, f"Pagina {doc.page}")
        canvas.drawRightString(self.width - 2*cm, 2*cm, settings.COMPANY_EMAIL)
        
        canvas.restoreState()

    def generate(self, output_path):
        """Generate invoice PDF"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm
        )

        # Prepare story (content)
        story = []

        # Invoice title and number
        story.append(Paragraph(
            f"FACTURĂ FISCALĂ Seria {settings.INVOICE_PREFIX} Nr. {self.order.id}",
            self.styles['Heading1']
        ))
        story.append(Spacer(1, 20))

        # Date and payment info
        date_payment = [
            ['Data facturii:', self.order.created_at.strftime('%d.%m.%Y')],
            ['Data scadentă:', self.order.created_at.strftime('%d.%m.%Y')],
            ['Metodă de plată:', self.order.get_payment_method_display()],
        ]
        t = Table(date_payment, colWidths=[4*cm, 4*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # Client and company details
        client_company = [
            ['FURNIZOR:', 'CLIENT:'],
            [settings.COMPANY_NAME, self.order.user.get_full_name()],
            [settings.COMPANY_ADDRESS, self.order.shipping_address],
            [f"CUI: {settings.COMPANY_VAT}", ''],
            [f"Reg. Com.: {settings.COMPANY_REG}", ''],
            [f"Cont: {settings.COMPANY_BANK}", ''],
            [f"Banca: {settings.COMPANY_BANK_NAME}", ''],
        ]
        t = Table(client_company, colWidths=[8*cm, 8*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # Products table
        products_data = [['Nr.', 'Produs', 'Cantitate', 'Preț unitar', 'TVA', 'Total']]
        for idx, item in enumerate(self.order.items.all(), 1):
            vat = item.total_price * 0.19  # 19% TVA
            products_data.append([
                str(idx),
                item.product.name,
                str(item.quantity),
                f"{item.unit_price:.2f} Lei",
                f"{vat:.2f} Lei",
                f"{item.total_price:.2f} Lei"
            ])
        
        # Add shipping if applicable
        if self.order.total_amount < 200:
            vat = 20 * 0.19  # 19% TVA pe transport
            products_data.append([
                str(len(products_data)),
                'Transport',
                '1',
                '20.00 Lei',
                f"{vat:.2f} Lei",
                '20.00 Lei'
            ])

        t = Table(products_data, colWidths=[1*cm, 8*cm, 2*cm, 2.5*cm, 2.5*cm, 2.5*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # Totals
        subtotal = self.order.total_amount
        vat = subtotal * 0.19
        total = subtotal + vat

        totals_data = [
            ['Subtotal:', f"{subtotal:.2f} Lei"],
            ['TVA (19%):', f"{vat:.2f} Lei"],
            ['Total:', f"{total:.2f} Lei"],
        ]
        t = Table(totals_data, colWidths=[8*cm, 2.5*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black),
        ]))
        story.append(t)

        # Build PDF
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

def generate_invoice(order):
    """Generate invoice for an order"""
    # Create invoices directory if it doesn't exist
    invoice_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
    os.makedirs(invoice_dir, exist_ok=True)

    # Generate invoice filename
    filename = f"factura_{settings.INVOICE_PREFIX}_{order.id}.pdf"
    filepath = os.path.join(invoice_dir, filename)

    # Generate invoice
    generator = InvoiceGenerator(order)
    generator.generate(filepath)

    return filepath