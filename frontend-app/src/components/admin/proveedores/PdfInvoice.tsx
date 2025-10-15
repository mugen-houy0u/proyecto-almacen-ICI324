import type { Item, Proveedor, Totales } from './types';
import { money } from './money';
import type { Ref } from 'preact';

type Props = {
  proveedor: Proveedor;
  items: Item[];
  totales: Totales;
  elRef?: Ref<HTMLElement>;
};

export default function PdfInvoice({ proveedor, items, totales, elRef }: Props) {
  // tolera variantes de nombres por si tu ItemsTable usa otras keys
  const norm = (it: any) => ({
    id: it.id,
    descripcion: it.descripcion ?? it.desc ?? '',
    cantidad: Number(it.cantidad ?? it.qty ?? 0),
    um: it.um ?? it.unidad ?? 'UN',
    precio: Number(it.precio ?? it.price ?? 0),
    porcImpuesto: Number(it.porcImpuesto ?? it.impuesto ?? it.tax ?? 0),
    porcDescuento: Number(it.porcDescuento ?? it.descuento ?? it.disc ?? 0),
    total: Number(it.total ?? 0),
  });

  const N = items?.map(norm) ?? [];

  return (
    <section
      ref={elRef}
      id="pdf-invoice"
      style={{
        // A4 con margen de 10mm → 210 - 20 = 190mm útiles
        width: '190mm',
        fontFamily: 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif',
        lineHeight: 1.4 as any,
        color: '#1f2937',
        background: '#ffffff',
        border: '1px solid #e5e7eb',
        borderRadius: '12px',
        padding: '10mm',
        boxSizing: 'border-box',
      }}
    >
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16}}>
        <div>
          <div style={{fontSize: 12, color: '#6b7280'}}>PRUEBA</div>
          <h2 style={{margin: 0, fontSize: 22}}>Factura</h2>
          <div style={{fontSize: 12, color: '#6b7280'}}>Emisor demo — www.demo.cl — +56 55 5555</div>
        </div>
        <div style={{border: '2px solid #ef4444', color: '#ef4444', padding: '6px 12px', borderRadius: 10, fontWeight: 700}}>
          FACTURA&nbsp;ELECTRÓNICA
        </div>
      </header>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, fontSize: 14, marginBottom: 16}}>
        <div>
          <div><strong>Señor(es):</strong>{' '}{proveedor?.nombre || '—'}</div>
          <div><strong>R.U.T.:</strong>{' '}{proveedor?.rut || '—'}</div>
          <div><strong>Giro:</strong>{' '}{proveedor?.giro || '—'}</div>
          <div><strong>Correo:</strong>{' '}{proveedor?.correo || '—'}</div>
        </div>
        <div>
          <div><strong>Fecha emisión:</strong>{' '}{proveedor?.fechaEmision || '—'}</div>
          <div><strong>Forma de pago:</strong>{' '}{proveedor?.formaPago || '—'}</div>
        </div>
      </div>

      <div style={{overflow: 'hidden', border: '1px solid #e5e7eb', borderRadius: 10}}>
        <table style={{width: '100%', borderCollapse: 'collapse', fontSize: 14}}>
          <thead style={{background: '#f3f4f6'}}>
            <tr>
              {['N°','Descripción','Cantidad','U.M','Precio','% Imp.','% Desc.','Total'].map((h, i) => (
                <th key={i} style={{textAlign: 'left', padding: 10, borderBottom: '1px solid #e5e7eb', color: '#374151'}}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {N && N.length > 0 ? (
              N.map((r) => (
                <tr key={r.id}>
                  <td style={tdMono}>{r.id}</td>
                  <td style={td}>{r.descripcion || '—'}</td>
                  <td style={tdMono}>{r.cantidad}</td>
                  <td style={td}>{r.um}</td>
                  <td style={tdMono}>{money(r.precio)}</td>
                  <td style={tdMono}>{r.porcImpuesto}%</td>
                  <td style={tdMono}>{r.porcDescuento}%</td>
                  <td style={{...tdMono, textAlign: 'right'}}>{money(r.total)}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={8} style={{textAlign: 'center', padding: 20, color: '#6b7280'}}>Sin productos agregados</td>
              </tr>
            )}
          </tbody>
          <tfoot>
            {[
              ['Subtotal', money(totales?.subtotal ?? 0)],
              ['Impuestos', money(totales?.impuestos ?? 0)],
              ['Descuentos', `-${money(totales?.descuentos ?? 0).replace('$','')}`],
              ['Total factura', money(totales?.total ?? 0)],
            ].map(([k, v], i) => (
              <tr key={i}>
                <td colSpan={7} style={{padding: 10, textAlign: 'right', fontWeight: 600, borderTop: '1px solid #e5e7eb'}}>{k}</td>
                <td style={{padding: 10, textAlign: 'right', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace', fontWeight: 700, borderTop: '1px solid #e5e7eb'}}>{v}</td>
              </tr>
            ))}
          </tfoot>
        </table>
      </div>

      <p style={{marginTop: 10, fontSize: 12, color: '#6b7280'}}>Documento de demostración (frontend). “Sello rojo” decorativo.</p>
    </section>
  );
}

const td = { padding: '10px', borderBottom: '1px solid #e5e7eb' };
const tdMono = { ...td, fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace' };
