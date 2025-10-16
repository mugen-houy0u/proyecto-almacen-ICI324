from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List
import io
from fpdf import FPDF

# --- Modelos de Pydantic (sin cambios) ---
class ItemFactura(BaseModel):
    descripcion: str
    cantidad: int
    um: str
    precio: int
    impuesto: int
    descuento: int
    total: int

class TotalesFactura(BaseModel):
    subtotal: str
    impuestos: str
    descuentos: str
    total: str

class ProveedorFactura(BaseModel):
    rut: str
    nombre: str
    correo: str
    giro: str
    fechaEmision: str = Field(..., alias="fechaEmision")
    formaPago: str = Field(..., alias="formaPago")

class FacturaPayload(BaseModel):
    proveedor: ProveedorFactura
    items: List[ItemFactura]
    totales: TotalesFactura

# --- Router ---
router = APIRouter(prefix="/facturas", tags=["Facturas"])

# --- Clase Helper para generar el PDF con fpdf2 ---
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 18)
        self.cell(0, 10, 'Factura', 0, 1, 'C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 5, 'Emisor: El Vecino - www.elvecino.cl', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, data):
        self.set_font('Helvetica', '', 10)
        for key, value in data.items():
            self.multi_cell(0, 5, f'{key}: {value}')
        self.ln()
    
    def items_table(self, items):
        self.set_font('Helvetica', 'B', 9)
        col_width = [90, 25, 35, 40] # Descripción, Cant., Precio, Total
        headers = ['Descripción', 'Cantidad', 'Precio Unit.', 'Total']
        for i, header in enumerate(headers):
            self.cell(col_width[i], 7, header, 1, 0, 'C')
        self.ln()

        self.set_font('Helvetica', '', 9)
        for item in items:
            start_y = self.get_y()
            self.multi_cell(col_width[0], 6, item.descripcion, 1)
            current_y = self.get_y()
            
            self.set_xy(self.get_x() + col_width[0], start_y)
            self.cell(col_width[1], current_y - start_y, f'{item.cantidad} {item.um}', 1, 0, 'C')
            self.cell(col_width[2], current_y - start_y, f'${item.precio:,}'.replace(',', '.'), 1, 0, 'R')
            self.cell(col_width[3], current_y - start_y, f'${item.total:,}'.replace(',', '.'), 1, 0, 'R')
            self.ln()
    
    def totals_section(self, totales):
        self.ln(5)
        table_width = 90 + 25 + 35 + 40
        total_label_width = table_width - 40

        self.set_font('Helvetica', '', 10)
        self.cell(total_label_width, 6, 'Subtotal:', 0, 0, 'R')
        self.cell(40, 6, totales.subtotal, 0, 1, 'R')
        self.cell(total_label_width, 6, 'Impuestos:', 0, 0, 'R')
        self.cell(40, 6, totales.impuestos, 0, 1, 'R')
        self.cell(total_label_width, 6, 'Descuentos:', 0, 0, 'R')
        self.cell(40, 6, totales.descuentos, 0, 1, 'R')
        self.set_font('Helvetica', 'B', 12)
        self.cell(total_label_width, 8, 'Total Factura:', 0, 0, 'R')
        self.cell(40, 8, totales.total, 0, 1, 'R')


# --- Endpoint para generar el PDF ---
@router.post("/generar-pdf", summary="Generar factura en PDF")
def generar_factura_pdf(payload: FacturaPayload):
    try:
        pdf = PDF()
        pdf.add_page()
        
        pdf.chapter_title('Datos del Proveedor')
        proveedor_data = {
            "Señor(es)": payload.proveedor.nombre,
            "R.U.T.": payload.proveedor.rut,
            "Giro": payload.proveedor.giro,
            "Correo": payload.proveedor.correo,
            "Fecha Emisión": payload.proveedor.fechaEmision,
            "Forma de Pago": payload.proveedor.formaPago,
        }
        pdf.chapter_body(proveedor_data)

        pdf.chapter_title('Detalle de Productos')
        pdf.items_table(payload.items)

        pdf.totals_section(payload.totales)
        
        # 👇 CORREGIDO: Genera el PDF directamente a bytes, que es más seguro y moderno.
        pdf_bytes = pdf.output()
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=factura-{payload.proveedor.rut}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")
