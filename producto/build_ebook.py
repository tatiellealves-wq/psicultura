# -*- coding: utf-8 -*-
"""
Genera el e-book "Tilapia Rentable" en PDF.
Producto de entrada (LATAM: MX, CO, PE, EC, AR, CL) para pequeños inversionistas.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    NextPageTemplate, PageBreak, Flowable, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ----------------------------------------------------------------------------
# Paleta de marca
# ----------------------------------------------------------------------------
TEAL      = colors.HexColor("#0E7C86")   # primario (agua)
TEAL_DARK = colors.HexColor("#0A5A62")
AQUA_BG   = colors.HexColor("#EAF4F5")   # fondo suave
ORANGE    = colors.HexColor("#E8833A")   # acento / CTA
INK       = colors.HexColor("#1A2B32")   # texto
GREY      = colors.HexColor("#5B6B72")
GREEN_BG  = colors.HexColor("#E7F3EC")
GREEN_LN  = colors.HexColor("#2E9E5B")
RED_BG    = colors.HexColor("#FBEBE8")
RED_LN    = colors.HexColor("#D0472A")
GOLD_BG   = colors.HexColor("#FBF3E2")
GOLD_LN   = colors.HexColor("#D99A22")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ----------------------------------------------------------------------------
# Estilos
# ----------------------------------------------------------------------------
styles = getSampleStyleSheet()

def S(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

st_body = S("body", fontName="Helvetica", fontSize=10.5, leading=15.5,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
st_body_l = S("body_l", parent=st_body, alignment=TA_LEFT)
st_lead = S("lead", fontName="Helvetica", fontSize=12.5, leading=18,
            textColor=TEAL_DARK, alignment=TA_LEFT, spaceAfter=10)
st_h1 = S("h1", fontName="Helvetica-Bold", fontSize=21, leading=25,
          textColor=TEAL_DARK, spaceBefore=4, spaceAfter=4)
st_h1num = S("h1num", fontName="Helvetica-Bold", fontSize=12, leading=14,
             textColor=ORANGE, spaceAfter=2)
st_h2 = S("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=17,
          textColor=INK, spaceBefore=12, spaceAfter=5)
st_h3 = S("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
          textColor=TEAL_DARK, spaceBefore=8, spaceAfter=3)
st_callout_t = S("callo_t", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=INK)
st_callout = S("callo", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, alignment=TA_LEFT)
st_bullet = S("bul", parent=st_body, alignment=TA_LEFT, spaceAfter=4, leftIndent=2)
st_tbl_h = S("tblh", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.white)
st_tbl = S("tbl", fontName="Helvetica", fontSize=9.5, leading=12, textColor=INK)
st_tbl_r = S("tblr", parent=st_tbl, alignment=TA_CENTER)
st_tbl_b = S("tblb", parent=st_tbl, fontName="Helvetica-Bold")
st_cap = S("cap", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=GREY, spaceBefore=3)
st_toc = S("toc", fontName="Helvetica", fontSize=11, leading=20, textColor=INK)
st_toc_n = S("tocn", fontName="Helvetica-Bold", fontSize=11, leading=20, textColor=ORANGE)

# ----------------------------------------------------------------------------
# Flowables auxiliares
# ----------------------------------------------------------------------------
class HRule(Flowable):
    def __init__(self, w, color=TEAL, thick=2, space=0):
        super().__init__(); self.w=w; self.color=color; self.thick=thick; self.space=space
    def wrap(self, aw, ah): return (self.w, self.thick + self.space)
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.thick)
        self.canv.line(0, self.space, self.w, self.space)

def callout(title, body_html, bg, line, icon=""):
    """Caja de color con barra lateral."""
    inner = []
    if title:
        inner.append(Paragraph((icon + " " if icon else "") + title, st_callout_t))
        inner.append(Spacer(1, 3))
    if isinstance(body_html, list):
        for b in body_html:
            inner.append(Paragraph(b, st_callout)); inner.append(Spacer(1,2))
    else:
        inner.append(Paragraph(body_html, st_callout))
    t = Table([[inner]], colWidths=[PAGE_W - 2*MARGIN - 8*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LINEBEFORE", (0,0), (0,-1), 3, line),
        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return KeepTogether([Spacer(1,4), t, Spacer(1,6)])

def data_table(header, rows, col_widths, totals_row=None, align_cols=None):
    align_cols = align_cols or {}
    data = [[Paragraph(h, st_tbl_h) for h in header]]
    for r in rows:
        cells=[]
        for i, c in enumerate(r):
            stl = st_tbl_r if align_cols.get(i)=="c" else (st_tbl_b if align_cols.get(i)=="b" else st_tbl)
            cells.append(Paragraph(str(c), stl))
        data.append(cells)
    if totals_row:
        data.append([Paragraph(str(c), st_tbl_b) for c in totals_row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    ts = [
        ("BACKGROUND", (0,0), (-1,0), TEAL),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, AQUA_BG]),
        ("LINEBELOW", (0,0), (-1,0), 0.5, TEAL_DARK),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CFE0E2")),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]
    if totals_row:
        ts.append(("BACKGROUND", (0,-1), (-1,-1), TEAL_DARK))
        ts.append(("TEXTCOLOR", (0,-1), (-1,-1), colors.white))
    t.setStyle(TableStyle(ts))
    return t

def checklist(items):
    rows = [[Paragraph("☐", S("cbx",fontName="Helvetica",fontSize=13,textColor=TEAL)),
             Paragraph(it, st_bullet)] for it in items]
    t = Table(rows, colWidths=[7*mm, PAGE_W-2*MARGIN-7*mm])
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return t

def bullets(items, style=st_bullet):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=10, value="•") for i in items],
        bulletType="bullet", start="•", bulletColor=TEAL, leftIndent=12, bulletFontSize=9,
    )

# ----------------------------------------------------------------------------
# Cabecera / pie
# ----------------------------------------------------------------------------
def header_footer(canvas, doc):
    canvas.saveState()
    # pie
    canvas.setFillColor(GREY); canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 12*mm, "Tilapia Rentable  ·  Guía práctica para tu primer tanque")
    canvas.drawRightString(PAGE_W - MARGIN, 12*mm, "%d" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#D9E6E7")); canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 15*mm, PAGE_W-MARGIN, 15*mm)
    # marca superior
    canvas.setFillColor(TEAL); canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H-13*mm, "TILAPIA RENTABLE")
    canvas.setStrokeColor(colors.HexColor("#D9E6E7"))
    canvas.line(MARGIN, PAGE_H-15*mm, PAGE_W-MARGIN, PAGE_H-15*mm)
    canvas.restoreState()

def cover_page(canvas, doc):
    canvas.saveState()
    # fondo
    canvas.setFillColor(TEAL_DARK); canvas.rect(0,0,PAGE_W,PAGE_H, fill=1, stroke=0)
    # banda superior mas clara
    canvas.setFillColor(TEAL); canvas.rect(0, PAGE_H-95*mm, PAGE_W, 95*mm, fill=1, stroke=0)
    # ondas decorativas
    canvas.setStrokeColor(colors.HexColor("#3A99A1")); canvas.setLineWidth(1.2)
    import math
    for k in range(6):
        y0 = PAGE_H-95*mm + k*4*mm
        canvas.setStrokeColor(colors.Color(0.23,0.6,0.63, alpha=0.35))
        p = canvas.beginPath(); p.moveTo(0, y0)
        x=0
        while x <= PAGE_W:
            p.lineTo(x, y0 + 2.2*mm*math.sin(x/18.0)); x+=4
        canvas.drawPath(p)
    # etiqueta
    canvas.setFillColor(ORANGE); canvas.roundRect(MARGIN, PAGE_H-52*mm, 68*mm, 9*mm, 2*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold", 9.5)
    canvas.drawString(MARGIN+5*mm, PAGE_H-49.2*mm, "GUÍA PRÁCTICA PARA LATINOAMÉRICA")
    # titulo
    canvas.setFillColor(colors.white); canvas.setFont("Helvetica-Bold", 40)
    canvas.drawString(MARGIN, PAGE_H-72*mm, "Tilapia")
    canvas.drawString(MARGIN, PAGE_H-86*mm, "Rentable")
    # subtitulo
    canvas.setFillColor(colors.HexColor("#CDE6E8")); canvas.setFont("Helvetica", 14)
    canvas.drawString(MARGIN, PAGE_H-100*mm, "Cómo empezar tu primer tanque")
    canvas.drawString(MARGIN, PAGE_H-108*mm, "con poca inversión — y saber cuándo")
    canvas.drawString(MARGIN, PAGE_H-116*mm, "vas a recuperar tu dinero.")
    # bullets de portada
    canvas.setFont("Helvetica", 10.5); canvas.setFillColor(colors.white)
    by = PAGE_H-136*mm
    for line in ["Inversión inicial real, sin adornos",
                 "Flujo de caja de tu primer ciclo (6 meses)",
                 "El error financiero que quiebra a la mayoría",
                 "Bono: calculadora de retorno editable"]:
        canvas.setFillColor(ORANGE); canvas.circle(MARGIN+2*mm, by+1.2*mm, 1.4*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white); canvas.drawString(MARGIN+7*mm, by, line); by-=8*mm
    # pie de portada
    canvas.setFillColor(colors.HexColor("#9FC9CC")); canvas.setFont("Helvetica", 9)
    canvas.drawString(MARGIN, 18*mm, "México  ·  Colombia  ·  Perú  ·  Ecuador  ·  Argentina  ·  Chile")
    canvas.setFont("Helvetica-Oblique", 8.5)
    canvas.drawString(MARGIN, 12*mm, "Edición LATAM · Valores en USD de referencia")
    canvas.restoreState()

# ----------------------------------------------------------------------------
# Documento
# ----------------------------------------------------------------------------
def build():
    doc = BaseDocTemplate(
        "/home/user/psicultura/producto/entregables/Tilapia-Rentable-Guia.pdf",
        pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=20*mm, bottomMargin=20*mm,
        title="Tilapia Rentable - Guía práctica para empezar tu primer tanque",
        author="Tilapia Rentable", subject="Acuicultura para pequeños inversionistas en LATAM",
    )
    frame = Frame(MARGIN, 18*mm, PAGE_W-2*MARGIN, PAGE_H-36*mm, id="main")
    cover_frame = Frame(0,0,PAGE_W,PAGE_H, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
        PageTemplate(id="content", frames=[frame], onPage=header_footer),
    ])

    E = []
    A = E.append

    # -- Portada (dibujada en onPage); solo salto --
    A(NextPageTemplate("content"))
    A(PageBreak())

    # ========================= ÍNDICE =========================
    A(Paragraph("Contenido", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,10))
    toc = [
        ("", "Antes de empezar: lee esto"),
        ("1", "Por qué tilapia (y por qué ahora)"),
        ("2", "Cuánto cuesta empezar de verdad"),
        ("3", "El error #1 que quiebra al pequeño productor"),
        ("4", "Flujo de caja de tu primer ciclo"),
        ("5", "Lo técnico esencial (sin relleno)"),
        ("6", "Cómo vender tu producción"),
        ("7", "Plan de acción de 30-60-90 días"),
        ("", "Tu bono: calculadora de retorno (ROI)"),
        ("", "Próximos pasos"),
    ]
    trows=[]
    for n, t in toc:
        trows.append([Paragraph(n or "•", st_toc_n), Paragraph(t, st_toc)])
    tt = Table(trows, colWidths=[12*mm, PAGE_W-2*MARGIN-12*mm])
    tt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LINEBELOW",(0,0),(-1,-1),0.4,colors.HexColor("#E1ECED")),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    A(tt)
    A(Spacer(1, 14))
    A(callout("Un aviso honesto sobre las cifras",
        "Los precios de alevines, alimento y energía cambian entre México, Colombia, Perú, "
        "Ecuador, Argentina y Chile — y cambian cada año. Por eso todos los números de esta guía "
        "están en <b>dólares (USD) como referencia</b> y son <b>ilustrativos</b>. La idea no es que "
        "copies estas cifras, sino que aprendas <b>el método</b> para calcular las tuyas con precios "
        "locales. Para eso incluimos la calculadora editable al final.",
        GOLD_BG, GOLD_LN, "⚠"))

    A(PageBreak())

    # ========================= INTRO =========================
    A(Paragraph("Antes de empezar", st_h1num))
    A(Paragraph("Lee esto primero", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph(
        "Si estás leyendo esto, probablemente ya buscaste “cómo criar tilapia” en internet "
        "y encontraste decenas de videos y manuales técnicos gratuitos. Manuales que te explican la "
        "biología del pez, el pH del agua y la temperatura ideal… pero que <b>nunca responden la "
        "única pregunta que de verdad te quita el sueño</b>:", st_lead))
    A(Paragraph("“¿Esto me va a dar ganancia, y en cuánto tiempo?”",
        S("q", fontName="Helvetica-BoldOblique", fontSize=15, leading=20, textColor=ORANGE,
          alignment=TA_CENTER, spaceBefore=6, spaceAfter=10)))
    A(Paragraph(
        "Esta guía existe para responder exactamente eso. No es un tratado de biología acuícola. "
        "No son 200 páginas que nunca vas a terminar. Es una guía directa, pensada para que en una "
        "tarde de lectura sepas <b>si este negocio es para ti</b> — y si lo es, sepas <b>exactamente "
        "por dónde empezar</b>, con qué dinero y con qué expectativas realistas.", st_body))
    A(Paragraph(
        "La tilapia es hoy uno de los peces más cultivados de Latinoamérica. En Colombia representa "
        "cerca del 58&nbsp;% de toda la producción acuícola; en México se cultiva en 31 estados y la "
        "acuicultura ya aporta más del 90&nbsp;% de la tilapia que se consume. Hay una razón para eso: "
        "ciclo corto (cosechas en ~6 meses), demanda constante y una inversión de arranque mucho más "
        "accesible que la de casi cualquier otra actividad ganadera.", st_body))
    A(callout("Lo que este material SÍ es y NO es",
        ["<b>SÍ es:</b> un plan de negocio conciso, con costos, flujo de caja y un plan de acción.",
         "<b>NO es:</b> un curso académico, ni una promesa de “hágase rico rápido”. "
         "La tilapia es rentable, pero es <b>trabajo</b>, no un botón mágico."],
        AQUA_BG, TEAL, "ℹ"))

    A(PageBreak())

    # ========================= 1. POR QUÉ TILAPIA =========================
    A(Paragraph("Capítulo 1", st_h1num))
    A(Paragraph("Por qué tilapia (y por qué ahora)", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("La tilapia gana frente a otras especies por cuatro razones muy concretas para "
                "quien empieza con poco capital:", st_body))
    A(Paragraph("1. Ciclo corto de producción", st_h3))
    A(Paragraph("En condiciones adecuadas, la tilapia llega a talla comercial (400–600&nbsp;g) en "
        "aproximadamente <b>6 meses</b>. Eso significa que puedes ver el resultado de tu inversión en el "
        "mismo año — no en 3 o 4 años como en otras actividades.", st_body))
    A(Paragraph("2. Rusticidad", st_h3))
    A(Paragraph("Tolera variaciones de temperatura y densidades altas mejor que la mayoría de los peces "
        "de cultivo. Perdona errores de principiante que otras especies no perdonan.", st_body))
    A(Paragraph("3. Demanda y precio estable", st_h3))
    A(Paragraph("Carne blanca, sabor suave, sin espinas intramusculares molestas y de precio accesible: "
        "es un pescado que <b>el mercado ya conoce y pide</b>. No tienes que “educar” al comprador.", st_body))
    A(Paragraph("4. Inversión de arranque flexible", st_h3))
    A(Paragraph("Puedes empezar con un tanque de geomembrana de pocos metros cuadrados en el patio, o con "
        "un estanque de tierra de 500&nbsp;m². La actividad <b>escala contigo</b>.", st_body))

    A(Paragraph("Las cuatro tipologías de productor", st_h2))
    A(Paragraph("Los estudios de rentabilidad en la región suelen clasificar al productor en cuatro "
        "niveles. Ubícate: esta guía te lleva del nivel <b>Inicial</b> al <b>Artesanal</b> con paso firme.", st_body))
    A(data_table(
        ["Tipología", "Escala típica", "Objetivo"],
        [["Inicial", "1 tanque, autoconsumo + venta vecinal", "Aprender el ciclo sin perder dinero"],
         ["Artesanal", "1–3 estanques, venta local regular", "Primera fuente de ingreso real"],
         ["Intermedio", "Varios estanques, venta a intermediarios", "Negocio de tiempo completo"],
         ["Empresarial", "Producción a escala, marca propia", "Rentabilidad máxima por kg"]],
        [32*mm, 62*mm, PAGE_W-2*MARGIN-94*mm]))
    A(Spacer(1,4))
    A(callout("Dato de mercado",
        "En un estudio del Estado de México, un proyecto de tilapia mostró una Tasa Interna de Retorno "
        "(TIR) del <b>24&nbsp;%</b> con capital propio y hasta <b>64&nbsp;%</b> con financiamiento, con recuperación "
        "de la inversión entre <b>1,3 y 3,3 años</b> según el manejo. La rentabilidad existe — pero depende "
        "casi por completo de la <b>planificación</b>, no de la suerte.",
        GREEN_BG, GREEN_LN, "✓"))

    A(PageBreak())

    # ========================= 2. CUÁNTO CUESTA =========================
    A(Paragraph("Capítulo 2", st_h1num))
    A(Paragraph("Cuánto cuesta empezar de verdad", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Aquí está el corazón de la guía. La mayoría de las personas abandonan no por la "
        "técnica, sino porque <b>subestimaron lo que costaba</b> y se quedaron sin capital a mitad del "
        "primer ciclo. Vamos a evitar eso desde hoy.", st_body))
    A(Paragraph("La inversión se divide en dos bloques que jamás debes mezclar en tu cabeza:", st_body))
    A(bullets([
        "<b>Inversión fija (una sola vez):</b> lo que compras al inicio y te dura varios ciclos "
        "— tanque, aireador, red, tubería, báscula.",
        "<b>Capital de operación (cada ciclo):</b> lo que se consume — alevines, alimento, energía, "
        "mano de obra. <b>Este es el que la gente olvida presupuestar.</b>"]))

    A(Paragraph("Escenario A — Principiante (tanque de patio)", st_h2))
    A(Paragraph("Tanque de geomembrana de ~15&nbsp;m², ~500 alevines. Ideal para aprender el ciclo "
        "completo con riesgo bajo.", st_body_l))
    A(data_table(
        ["Concepto", "Tipo", "USD aprox."],
        [["Tanque geomembrana + estructura", "Fija", "350"],
         ["Aireador / bomba pequeña", "Fija", "180"],
         ["Red, baldes, báscula, kit de agua", "Fija", "120"],
         ["500 alevines reversados", "Operación", "60"],
         ["Alimento balanceado (~450 kg / ciclo)", "Operación", "340"],
         ["Energía (6 meses)", "Operación", "90"],
         ["Imprevistos (10&nbsp;%)", "Operación", "115"]],
        [PAGE_W-2*MARGIN-60*mm, 28*mm, 32*mm],
        totals_row=["Inversión total para arrancar", "", "USD ≈ 1.255"],
        align_cols={1:"c",2:"c"}))
    A(Paragraph("Cosecha estimada: ~450 alevines llegan a mercado (10&nbsp;% de mortalidad) × ~0,5 kg = "
        "<b>~225 kg</b>. A un precio de venta de USD 3,0/kg = <b>USD 675 por ciclo</b>.", st_cap))
    A(callout("Ojo con el Escenario A",
        "A esta escala pequeña, casi todo el primer ciclo paga la <b>inversión fija</b>. No esperes "
        "ganancia el primer ciclo: su valor es <b>aprender sin arriesgar mucho</b>. La ganancia real "
        "aparece del segundo ciclo en adelante, cuando la estructura ya está pagada.",
        GOLD_BG, GOLD_LN, "⚠"))

    A(Paragraph("Escenario B — Pequeño comercial (estanque 500 m²)", st_h2))
    A(Paragraph("Estanque de tierra o geomembrana de 500&nbsp;m², ~3.000 alevines. El primer paso hacia un "
        "ingreso real y recurrente.", st_body_l))
    A(data_table(
        ["Concepto", "Tipo", "USD aprox."],
        [["Adecuación de estanque + geomembrana", "Fija", "1.600"],
         ["Sistema de aireación", "Fija", "650"],
         ["Equipo de manejo y cosecha", "Fija", "400"],
         ["3.000 alevines reversados", "Operación", "330"],
         ["Alimento (~4.200 kg / ciclo)", "Operación", "3.150"],
         ["Energía + mano de obra (6 meses)", "Operación", "900"],
         ["Imprevistos (10&nbsp;%)", "Operación", "740"]],
        [PAGE_W-2*MARGIN-60*mm, 28*mm, 32*mm],
        totals_row=["Inversión total para arrancar", "", "USD ≈ 7.770"],
        align_cols={1:"c",2:"c"}))
    A(Paragraph("Cosecha estimada: 2.700 peces (10&nbsp;% mortalidad) × ~0,55 kg = <b>~1.485 kg</b>. "
        "A USD 3,0/kg = <b>USD 4.455</b> el primer ciclo (≈ USD 10.000 si logras 2.500&nbsp;kg con mejor manejo).", st_cap))

    A(Spacer(1,4))
    A(callout("La regla de oro del alimento",
        "En ambos escenarios notarás lo mismo: el <b>alimento balanceado es el 40&nbsp;% a 70&nbsp;% de todo tu "
        "costo</b>. No es un detalle — es EL número del negocio. Si no controlas la conversión alimenticia "
        "(cuántos kg de alimento para producir 1 kg de pez), no controlas tu ganancia. Volveremos a esto.",
        RED_BG, RED_LN, "❗"))

    A(PageBreak())

    # ========================= 3. EL ERROR =========================
    A(Paragraph("Capítulo 3", st_h1num))
    A(Paragraph("El error #1 que quiebra al pequeño productor", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Aquí va la verdad que casi nadie te dice, y que vale por sí sola el precio de esta guía:", st_lead))
    A(Paragraph("El pequeño productor de tilapia rara vez fracasa por no saber criar peces. "
        "Fracasa por <b>mala gestión financiera</b>: se queda sin dinero para comprar alimento "
        "antes de poder cosechar y vender.",
        S("big", fontName="Helvetica-Bold", fontSize=13, leading=18, textColor=INK,
          alignment=TA_LEFT, spaceAfter=10)))
    A(Paragraph("Piensa en el ciclo: compras alevines pequeños y durante <b>6 meses solo gastas</b> "
        "(alimento, energía) sin ingresar un solo peso. El dinero únicamente entra <b>al final</b>, "
        "cuando cosechas. Ese “valle” de 6 meses es donde mueren la mayoría de los proyectos.", st_body))

    A(Paragraph("Los 5 errores que vacían tu bolsillo", st_h2))
    A(Paragraph("1. No presupuestar el capital de operación completo", st_h3))
    A(Paragraph("Compran el tanque y los alevines con casi todo su dinero… y no les queda para el alimento "
        "de los meses 4, 5 y 6 — justo cuando el pez más come. <b>Regla:</b> ten guardado el costo de "
        "alimento de <b>todo el ciclo</b> ANTES de comprar el primer alevin.", st_body))
    A(Paragraph("2. Sobreestimar la densidad y subestimar la mortalidad", st_h3))
    A(Paragraph("“Si meto el doble de peces, gano el doble.” Falso: sin oxígeno suficiente, mueren o "
        "no crecen. Para principiante, planea con <b>10&nbsp;% de mortalidad</b> y densidad conservadora.", st_body))
    A(Paragraph("3. No medir la conversión alimenticia (FCA)", st_h3))
    A(Paragraph("Si gastas más de ~1,6&nbsp;kg de alimento por cada kg de pez, tu margen se evapora. "
        "Pesa, anota, ajusta. Lo que no se mide, no se gestiona.", st_body))
    A(Paragraph("4. Producir sin comprador definido", st_h3))
    A(Paragraph("Llegan a la cosecha con 1.500&nbsp;kg de pez vivo… y ahí empiezan a buscar a quién "
        "vender. El pez no espera. <b>El comprador se consigue ANTES de sembrar</b>, no después (Capítulo 6).", st_body))
    A(Paragraph("5. Mezclar el dinero del proyecto con el dinero de la casa", st_h3))
    A(Paragraph("El proyecto necesita su propia “caja”. Si sacas de ahí para el gasto diario, "
        "descapitalizas el ciclo sin darte cuenta.", st_body))

    A(callout("La prueba de fuego antes de invertir",
        "Si no puedes responder con números a estas tres preguntas, <b>aún no estás listo para "
        "sembrar</b>: (1) ¿Cuánto alimento consumirá todo el ciclo y cuánto cuesta? "
        "(2) ¿A quién y a qué precio por kg le vas a vender? "
        "(3) ¿De dónde saldrá el dinero para los meses 4–6? La calculadora del bono responde la (1).",
        AQUA_BG, TEAL, "ℹ"))

    A(PageBreak())

    # ========================= 4. FLUJO DE CAJA =========================
    A(Paragraph("Capítulo 4", st_h1num))
    A(Paragraph("Flujo de caja de tu primer ciclo", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Este es el mapa que te salva del “valle de la muerte” de los 6 meses. Usamos el "
        "<b>Escenario B</b> (500&nbsp;m², 3.000 peces). Fíjate cómo el dinero solo <b>sale</b> hasta el mes 6:", st_body))
    A(data_table(
        ["Mes", "Actividad", "Sale (USD)", "Entra (USD)", "Caja acum."],
        [["0", "Inversión fija + alevines", "2.980", "–", "–2.980"],
         ["1", "Alimento inicio + energía", "430", "–", "–3.410"],
         ["2", "Alimento + energía", "560", "–", "–3.970"],
         ["3", "Alimento + energía", "720", "–", "–4.690"],
         ["4", "Alimento (pico de consumo)", "900", "–", "–5.590"],
         ["5", "Alimento + energía", "950", "–", "–6.540"],
         ["6", "Cosecha y VENTA", "600", "4.455", "–2.685"]],
        [12*mm, PAGE_W-2*MARGIN-12*mm-90*mm, 26*mm, 28*mm, 28*mm],
        totals_row=["", "Resultado del 1er ciclo", "7.140", "4.455", "–2.685"],
        align_cols={0:"c",2:"c",3:"c",4:"c"}))
    A(Spacer(1,4))
    A(callout("Cómo leer este cuadro (clave)",
        ["El “–2.685” final <b>no es una pérdida</b>: es que aún no recuperaste la <b>inversión "
         "fija</b> (tanque, aireador…), que dura muchos ciclos.",
         "Del <b>2° ciclo en adelante</b> ya no compras estructura: solo pones ~USD 5.100 de operación "
         "y recibes ~USD 4.455+. Ahí es donde el negocio se vuelve <b>rentable de verdad</b>.",
         "El número más importante de toda la tabla es la <b>caja acumulada más baja</b> (–USD 6.540 en "
         "el mes 5): ese es el capital que <b>necesitas tener asegurado</b> antes de sembrar."],
        GREEN_BG, GREEN_LN, "✓"))
    A(Paragraph("Regla práctica: nunca siembres un ciclo si no tienes cubierto el punto más bajo de tu "
        "caja acumulada. La calculadora del bono te da ese número automáticamente al meter tus precios locales.", st_body))

    A(PageBreak())

    # ========================= 5. TÉCNICO ESENCIAL =========================
    A(Paragraph("Capítulo 5", st_h1num))
    A(Paragraph("Lo técnico esencial (sin relleno)", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Lo técnico profundo ya existe gratis en manuales oficiales. Aquí va solo el mínimo "
        "indispensable para que tus números del negocio se cumplan.", st_body))
    A(Paragraph("Elegir el sistema de cultivo", st_h2))
    A(data_table(
        ["Sistema", "Inversión", "Bueno para…"],
        [["Estanque de tierra", "Baja", "Terreno propio, clima cálido, más área"],
         ["Tanque de geomembrana", "Media", "Patio, control del agua, principiantes"],
         ["Tanque-red (jaula)", "Media", "Tienes acceso a represa / lago"],
         ["Biofloc / recirculación", "Alta", "Poco espacio, alta densidad, más técnica"]],
        [42*mm, 26*mm, PAGE_W-2*MARGIN-68*mm]))
    A(callout("Recomendación para empezar",
        "Si es tu primer proyecto, empieza con <b>geomembrana</b>: controlas el agua, es fácil de "
        "cosechar y de limpiar, y el error se corrige rápido. Deja el biofloc para cuando ya domines "
        "el ciclo básico.", AQUA_BG, TEAL, "ℹ"))

    A(Paragraph("Los 4 parámetros que no puedes descuidar", st_h2))
    A(bullets([
        "<b>Oxígeno disuelto:</b> manténlo por encima de 4&nbsp;mg/L. Es la causa #1 de muerte masiva. "
        "Un aireador no es un lujo, es un seguro de vida.",
        "<b>Temperatura:</b> la tilapia crece mejor entre 26&nbsp;°C y 30&nbsp;°C. Por debajo de 18&nbsp;°C "
        "deja de comer (clave en zonas altas de Perú, Ecuador o el sur de Argentina/Chile).",
        "<b>Densidad de siembra:</b> para principiante en geomembrana, empieza conservador "
        "(~10–15 peces/m³ con aireación). Prefiere pocos peces sanos a muchos estresados.",
        "<b>Recambio y calidad del agua:</b> agua verde clara = fitoplancton sano; agua muy turbia o con "
        "olor = alerta. Observa a diario."]))
    A(callout("Sobre el clima de tu región",
        "La tilapia es de agua cálida. En zonas frías (altiplano andino, Patagonia) es viable pero "
        "necesita invernadero o agua templada, lo que sube el costo. Si vives en zona fría, calcula "
        "ese sobrecosto ANTES — o considera que en esas zonas la <b>trucha</b> suele rendir mejor.",
        GOLD_BG, GOLD_LN, "⚠"))

    A(PageBreak())

    # ========================= 6. VENDER =========================
    A(Paragraph("Capítulo 6", st_h1num))
    A(Paragraph("Cómo vender tu producción", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Esta es la parte que casi ningún curso técnico te enseña — y es la que decide si "
        "ganas dinero. Producir es la mitad; <b>vender bien es la otra mitad</b>.", st_body))
    A(Paragraph("Tus canales de venta, de menor a mayor margen", st_h2))
    A(data_table(
        ["Canal", "Precio/kg", "Ventaja / desventaja"],
        [["Intermediario (mayorista)", "El más bajo", "Te compra todo de una vez, pero paga poco"],
         ["Pescaderías / tiendas locales", "Medio", "Volumen estable si cumples calidad"],
         ["Restaurantes de la zona", "Medio-alto", "Pagan mejor por tamaño y frescura constante"],
         ["Venta directa (vecinos, feria)", "El más alto", "Máximo margen, pero vendes de a poco"]],
        [46*mm, 26*mm, PAGE_W-2*MARGIN-72*mm]))
    A(Paragraph("La estrategia ganadora del principiante suele ser <b>mixta</b>: vende una parte directa "
        "(mejor precio) y coloca el resto con un intermediario para no quedarte con pez sin vender.", st_body))

    A(Paragraph("Cómo fijar tu precio (sin perder)", st_h2))
    A(Paragraph("Primero calcula tu <b>costo real por kg</b>: divide TODO lo que gastaste en el ciclo "
        "(operación) entre los kilos que cosechaste. Si gastaste USD 5.100 y cosechaste 1.485&nbsp;kg, tu "
        "costo es <b>USD 3,43/kg</b> — y ahí descubres que vender a 3,0 te hace <b>perder</b>. Tu precio "
        "de venta debe cubrir ese costo y dejar margen. La calculadora del bono hace esta cuenta por ti.", st_body))
    A(callout("El secreto: consigue al comprador ANTES de sembrar",
        "Antes de comprar tu primer alevin, habla con 2 o 3 compradores potenciales (una pescadería, "
        "un restaurante, un intermediario). Pregúntales qué tamaño quieren, cuántos kilos por semana "
        "y a qué precio. Eso <b>define tu proyecto</b> — no al revés. Producir para un comprador que ya "
        "dijo “sí” es la diferencia entre negocio y hobby caro.",
        GREEN_BG, GREEN_LN, "✓"))

    A(PageBreak())

    # ========================= 7. PLAN DE ACCIÓN =========================
    A(Paragraph("Capítulo 7", st_h1num))
    A(Paragraph("Plan de acción de 30-60-90 días", st_h1))
    A(HRule(PAGE_W-2*MARGIN, TEAL, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Imprime esta página. Es tu hoja de ruta antes de invertir tu primer peso. "
        "Marca cada casilla — no siembres hasta tener todas.", st_body))

    A(Paragraph("Días 1–30 · Validar (sin gastar en peces)", st_h3))
    A(checklist([
        "Definir mi escenario (A principiante o B comercial) y mi meta de kilos.",
        "Llenar la <b>calculadora de ROI</b> del bono con precios de MI ciudad.",
        "Hablar con 3 compradores potenciales y anotar tamaño, volumen y precio/kg.",
        "Cotizar alevines reversados con al menos 2 proveedores locales.",
        "Confirmar que tengo cubierto el <b>punto más bajo de caja</b> del ciclo.",
    ]))
    A(Paragraph("Días 31–60 · Montar", st_h3))
    A(checklist([
        "Adecuar el terreno / instalar el tanque de geomembrana.",
        "Instalar y probar la aireación (¡antes de meter peces!).",
        "Llenar y estabilizar el agua; medir oxígeno, pH y temperatura.",
        "Comprar el alimento del <b>primer mes</b> y planificar el resto.",
        "Abrir una “caja” separada solo para el proyecto.",
    ]))
    A(Paragraph("Días 61–90 · Sembrar y operar", st_h3))
    A(checklist([
        "Sembrar los alevines (temprano en la mañana, con agua estable).",
        "Empezar la <b>bitácora</b>: fecha, alimento diario, mortalidad, observaciones.",
        "Pesar una muestra cada 15 días y ajustar la ración.",
        "Revisar oxígeno a diario, sobre todo de madrugada.",
        "Confirmar con el comprador la fecha estimada de cosecha (mes ~6).",
    ]))
    A(callout("Tu única tarea de esta semana",
        "No compres nada todavía. Abre la <b>calculadora de ROI</b> y llénala con los precios reales de "
        "tu ciudad. En 20 minutos vas a saber, con TUS números, si este proyecto te conviene — y de "
        "cuánto capital necesitas partir. Ese es el paso #1.",
        AQUA_BG, TEAL, "→"))

    A(PageBreak())

    # ========================= BONO =========================
    A(Paragraph("Tu bono incluido", st_h1num))
    A(Paragraph("Calculadora de retorno (ROI)", st_h1))
    A(HRule(PAGE_W-2*MARGIN, ORANGE, 2, 4)); A(Spacer(1,8))
    A(Paragraph("Junto a esta guía recibes una <b>planilla editable</b> (Excel / Google Sheets) donde "
        "solo llenas las celdas amarillas con TUS precios locales y la planilla calcula sola:", st_body))
    A(bullets([
        "Tu <b>inversión total</b> para arrancar (fija + operación).",
        "Tu <b>costo real por kilo</b> de pez producido.",
        "Tu <b>ganancia estimada</b> por ciclo y tu margen.",
        "El <b>punto más bajo de caja</b> que debes tener asegurado.",
        "Tu <b>retorno (ROI)</b> y en cuántos ciclos recuperas la inversión fija.",
    ]))
    A(callout("Cómo usar tu planilla",
        ["<b>1.</b> Ábrela (Excel, o en Google Sheets: Archivo → Hacer una copia).",
         "<b>2.</b> Cambia solo las <b>celdas amarillas</b> por los precios de tu ciudad y moneda.",
         "<b>3.</b> Lee los resultados en la sección verde. ¡No toques las fórmulas!"],
        GOLD_BG, GOLD_LN, "⭐"))
    A(Spacer(1, 6))

    # ========================= CIERRE =========================
    A(Paragraph("Próximos pasos", st_h2))
    A(Paragraph("Ya tienes más claridad que el 90&nbsp;% de las personas que empiezan en la tilapia: "
        "sabes cuánto cuesta, dónde está el riesgo, cómo se vende y qué hacer primero. El único paso "
        "que falta es el más importante: <b>llenar tu calculadora y decidir con números</b>.", st_body))
    A(Paragraph("La tilapia recompensa a quien planifica. No a quien improvisa. Ya elegiste ser del "
        "primer grupo. Ahora ejecuta.", st_lead))
    A(Spacer(1, 10))
    A(HRule(PAGE_W-2*MARGIN, colors.HexColor("#D9E6E7"), 1, 3))
    A(Paragraph("© Tilapia Rentable · Guía práctica para Latinoamérica. Uso personal. "
        "Cifras ilustrativas en USD; verifica precios y normativa acuícola de tu país.",
        S("legal", fontName="Helvetica", fontSize=8, leading=11, textColor=GREY)))

    doc.build(E)
    print("PDF generado OK")

if __name__ == "__main__":
    build()
