# Tilapia Rentable — Producto digital

Producto de entrada (info-producto) para pequeños inversionistas de acuicultura en
Latinoamérica (México, Colombia, Perú, Ecuador, Argentina y Chile).

## Entregables

| Archivo | Qué es |
|---|---|
| `entregables/Tilapia-Rentable-Guia.pdf` | E-book principal (12 páginas, español) |
| `entregables/Calculadora-ROI-Tilapia.xlsx` | Bono: calculadora de retorno editable (Excel / Google Sheets) |

## Cómo regenerar los entregables

```bash
pip install reportlab openpyxl
python3 build_ebook.py         # genera el PDF
python3 build_calculadora.py   # genera la planilla XLSX
```

- `build_ebook.py` — genera el e-book con ReportLab (portada, tablas de costos,
  cajas de aviso, checklists, plan de acción 30-60-90).
- `build_calculadora.py` — genera la calculadora de ROI. El usuario final edita
  solo las celdas amarillas; el resto son fórmulas. Se activa `fullCalcOnLoad`
  para que Excel/Google Sheets recalculen al abrir.

## Notas

- Todas las cifras del e-book están en USD como referencia y son ilustrativas.
- Próximo paso pendiente: página de ventas (landing) — a la espera del dominio.
- Idea futura: micro-SaaS a partir de la calculadora (solo si el PDF vende).
