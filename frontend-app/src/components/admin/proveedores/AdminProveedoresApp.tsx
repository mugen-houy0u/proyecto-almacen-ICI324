import { useMemo, useRef } from 'preact/hooks';
import ProviderForm from './ProviderForm';
import ItemsTable from './ItemsTable';
import InvoicePreview from './InvoicePreview';
import PdfInvoice from './PdfInvoice';        // 👈 usamos PdfInvoice
import { useInvoice } from './useInvoice';
import { generatePdf } from './pdf';

export default function AdminProveedoresApp() {
  const { proveedor, setProveedor, items, totales, addRow, removeRow, updateRow } = useInvoice();

  const canExport = useMemo(() => (items?.length ?? 0) > 0, [items]);

  const previewRef = useRef<HTMLElement>(null); // vista visible (opcional)
  const pdfRef = useRef<HTMLElement>(null);     // DOM limpio para PDF

  return (
    <div class="space-y-6">
      <ProviderForm value={proveedor} onChange={setProveedor} />

      <ItemsTable
        items={items}
        totales={totales}
        onAdd={addRow}
        onClear={() => location.reload()}
        onRemove={removeRow}
        onChange={updateRow}
      />

      <div class="flex gap-3">
        <button
          class="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          disabled={!canExport}
          onClick={async () => {
            const el = pdfRef.current;
            const rut = proveedor?.rut || 'proveedor';
            if (el) {
              // Espera a que fuentes/estilos estén listas, luego exporta
              setTimeout(() => {
                generatePdf(el as HTMLElement, `factura-${rut}.pdf`);
                }, 200);

            } else {
              alert('No se encontró el contenido de PDF.');
            }
          }}
        >
          🧾 Generar factura (PDF)
        </button>

        <button
          class="inline-flex items-center rounded-md border border-gray-700 bg-gray-800 px-4 py-2 text-white hover:bg-gray-700"
          onClick={() => console.log({ proveedor, items, totales })}
        >
          Guardar borrador (API)
        </button>
      </div>

      {/* Vista previa visible (oscura) */}
      <InvoicePreview elRef={previewRef} proveedor={proveedor} items={items} totales={totales} />

      {/* PdfInvoice: dentro del viewport pero invisible */}
      {/* PdfInvoice: fuera del viewport, pero visible para html2canvas */}
    <div
    id="pdfContainer"
    style={{
        position: 'absolute',
        top: '0',
        left: '0',
        width: '100%',
        background: '#fff',
        visibility: 'hidden', // 👈 en lugar de opacity 0 o display none
        pointerEvents: 'none',
    }}
    >
    <PdfInvoice elRef={pdfRef} proveedor={proveedor} items={items} totales={totales} />
    </div>

    </div>
  );
}
