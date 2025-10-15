// Usa la versión global por CDN (simple y estable)
export async function generatePdf(el: HTMLElement, filename: string) {
  if (!el) {
    alert('No se encontró el contenido a exportar.');
    return;
  }
  const w = typeof window !== 'undefined' ? (window as any) : undefined;
  const html2pdf = w?.html2pdf;
  if (!html2pdf) {
    alert('No se pudo generar el PDF: html2pdf no está disponible.');
    return;
  }

  // Esperar fuentes si el navegador lo permite (evita saltos de texto)
  if ((document as any).fonts?.ready) {
    try { await (document as any).fonts.ready; } catch {}
  }

  // Clonar para aislar estilos de invisibilidad (opacity/z-index) del original
  const clone = el.cloneNode(true) as HTMLElement;
  clone.style.position = 'absolute';
  clone.style.left = '-9999px';
  clone.style.top = '0';
  document.body.appendChild(clone);

  const opt = {
    filename,
    margin: 10, // mm
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
      // usar tamaño real del nodo para evitar recortes
      width: clone.scrollWidth,
      height: clone.scrollHeight,
      windowWidth: Math.max(clone.scrollWidth, document.documentElement.clientWidth),
      windowHeight: Math.max(clone.scrollHeight, document.documentElement.clientHeight),
      logging: false,
    },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] },
  } as const;

  await new Promise(r => setTimeout(r, 50));

  try {
    await html2pdf().from(clone).set(opt).save();
  } catch (err) {
    console.error('Error al generar PDF:', err);
    alert('Ocurrió un problema al generar el PDF.');
  } finally {
    document.body.removeChild(clone);
  }
}
