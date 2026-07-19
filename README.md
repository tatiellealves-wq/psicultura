# Tilapia Rentable — Producto digital (PDF + bono) para LATAM

Infoproducto de entrada sobre **cría de tilapia para pequeños inversionistas**, dirigido a
México, Colombia, Perú, Ecuador, Argentina y Chile.

## Idea y validación de mercado

La demanda del sector es alta y creciente en LATAM (la tilapia es la especie de cultivo más
producida en varios países de la región), pero la oferta de infoproductos se concentra en
**cursos en video completos** (Hotmart) y en **manuales técnicos gratuitos** de gobiernos.

Hueco detectado: no hay un material corto y directo enfocado en la pregunta que realmente frena
al principiante — *"¿esto me da ganancia y en cuánto tiempo?"*. Este producto ataca la **gestión
financiera / ROI**, no la biología (que ya está cubierta y gratis).

## Entregables

Carpeta [`producto/entregables/`](producto/entregables):

| Archivo | Qué es |
|---|---|
| `Tilapia-Rentable-Guia.pdf` | E-book principal (12 págs, español), con costos, flujo de caja, errores comunes, plan de acción. |
| `Calculadora-ROI-Tilapia.xlsx` | Bono: planilla editable (Excel / Google Sheets). El cliente edita solo las celdas amarillas y obtiene su ROI. |

## Cómo regenerar los entregables

```bash
cd producto
pip install reportlab openpyxl
python3 build_ebook.py         # genera el PDF
python3 build_calculadora.py   # genera la planilla XLSX
```

## Notas

- Todas las cifras del e-book están en **USD como referencia** y son **ilustrativas**: el valor
  está en el método de cálculo, no en copiar los números.
- La planilla usa `fullCalcOnLoad`, por lo que Excel y Google Sheets recalculan al abrir.
