# Prompts de imagem COM texto embutido — Onda 1

Formato: **1080×1350 (4:5 vertical)**
Uso: colar direto no ChatGPT / gerador de imagem. A peça sai pronta.

---

## Como esses prompts foram construídos

**1. Textos sem acento.** Cada frase foi reescrita para não ter `á é í ó ú ñ`.
É onde o modelo mais erra. Em espanhol, maiúscula sem acento é tipograficamente
aceita — nada fica gramaticalmente errado.

**2. Poucas palavras.** Quanto menor o bloco, maior a chance de sair soletrado
certo. Cada peça tem no máximo 3 blocos de texto.

**3. Layout declarado.** O prompt diz exatamente onde cada bloco vai, para o
modelo não empilhar tudo no meio.

**4. Gere 3 ou 4 variações de cada.** Mesmo com tudo isso, o modelo erra às
vezes. Escolha a que soletrou certo.

**Confira antes de subir:** cada letra, o `$6,90` (vírgula, não ponto), e se
não apareceu nenhuma palavra inventada no fundo.

---

## 🐟 IMAGEM 1 — El orden

```
Photorealistic vertical advertisement, 4:5 aspect ratio, 1080x1350.

SCENE (lower 45% of the frame): a rural backyard in Latin America at early
morning, soft golden light. A partially assembled circular geomembrane fish
tank, still empty, black liner folded over a simple metal frame, a green
garden hose coiled on packed earth. Behind it, a simple wooden fence and
banana plants, softly out of focus. Natural documentary photography, 35mm,
shallow depth of field, muted earthy colours with a teal accent.

TREATMENT: a dark teal gradient overlay rises from the middle of the image
to the top, so white text reads clearly over it.

TEXT — render these three blocks, spelled EXACTLY as written, in a bold
heavy sans-serif font, pure white, perfectly legible:

Top block, large, centered, two lines:
"PRIMERO EL TANQUE
O PRIMERO EL AGUA?"

Middle block, smaller, left-aligned, four separate lines:
"1 EL AGUA
2 EL TANQUE
3 CICLAR
4 EL PEZ"
The line "1 EL AGUA" is in warm yellow; the other three in white.

Bottom block, small, centered, on a solid yellow rounded badge with dark
text: "DESDE $6,90"

No other text anywhere in the image. No logos. No watermarks. No people.
```

---

## 💧 IMAGEM 2 — La semana 2

```
Photorealistic vertical advertisement, 4:5 aspect ratio, 1080x1350.

SCENE (lower 50% of the frame): extreme close-up of the weathered hands of
a Latin American fish farmer holding a clear plastic bag half-submerged in
tank water. Inside the bag, about a dozen small live tilapia fingerlings,
healthy and active, silver-grey with faint dark stripes. Soft ripples and
reflections. Warm late-morning light, shallow depth of field.
All fish alive and healthy — no dead fish.

TREATMENT: the upper half is calm dark green water, darkened further with a
gradient so white text reads clearly over it.

TEXT — render these three blocks, spelled EXACTLY as written, in a bold
heavy sans-serif font, pure white, perfectly legible:

Top block, large, centered, three lines:
"LA SEMANA 2
MATA MAS PECES
QUE CUALQUIER ENFERMEDAD"

Below it, smaller, centered, one line in warm yellow:
"AGUA SIN CICLAR"

Bottom block, small, centered, on a solid yellow rounded badge with dark
text: "DESDE $6,90"

No other text anywhere. No logos. No watermarks. No faces.
```

---

## 💸 IMAGEM 3 — Los numeros

```
Photorealistic vertical advertisement, 4:5 aspect ratio, 1080x1350.

SCENE (lower 55% of the frame): a weathered wooden table outdoors beside a
small fish farm. On the table, an open laptop showing a spreadsheet with
yellow highlighted cells and columns of figures, a pocket calculator, a
pencil and a small notebook. Behind, out of focus, a circular blue-lined
tilapia tank with banana plants. Warm natural light, shallow depth of field.

IMPORTANT: on the laptop screen show ONLY numeric figures, coloured cells
and simple bar charts — absolutely no words, no letters, no readable labels.

TREATMENT: a dark teal gradient overlay covers the upper part of the image
so white text reads clearly.

TEXT — render these three blocks, spelled EXACTLY as written, in a bold
heavy sans-serif font, pure white, perfectly legible:

Top block, large, centered, three lines:
"6 MESES GASTANDO
ANTES DE LA
PRIMERA VENTA"

Below it, smaller, centered, one line in warm yellow:
"HASTA 70% ES SOLO ALIMENTO"

Bottom block, small, centered, on a solid yellow rounded badge with dark
text: "DESDE $6,90"

No other text anywhere in the image, and no words on the laptop screen.
No logos. No watermarks. No people.
```

---

## 🔁 IMAGEM 4 — Ya lo intentaste

```
Photorealistic vertical advertisement, 4:5 aspect ratio, 1080x1350.

SCENE (lower 55% of the frame, subject on the right side): a Latin American
man in his late 40s, weathered face, worn work shirt and a cap, standing at
the edge of a small tilapia tank, looking down at the water with a
thoughtful, reflective expression — not sad, not smiling. Late afternoon
golden light from behind him, long soft shadows. Documentary photojournalism
style, 50mm, natural skin texture, no beauty retouching.

TREATMENT: the upper portion is warm sky and calm water, darkened with a
gradient so white text reads clearly over it.

TEXT — render these three blocks, spelled EXACTLY as written, in a bold
heavy sans-serif font, pure white, perfectly legible:

Top block, large, centered, two lines:
"YA LO INTENTASTE
Y PERDISTE EL LOTE?"

Below it, smaller, centered, one line in warm yellow:
"NO FUE FALTA DE TALENTO"

Bottom block, small, centered, on a solid yellow rounded badge with dark
text: "DESDE $6,90"

No other text anywhere. No logos. No watermarks.
```

---

## Se o modelo errar a grafia

Regenere pedindo:

```
Keep the exact same image, but fix the text. It must read EXACTLY:
"TEXTO CORRETO AQUI"
Check every letter. Bold heavy sans-serif, pure white, perfectly legible.
```

Se errar 3 vezes seguidas na mesma peça, use os prompts sem texto
(`prompts-imagens-onda1.md`) e monte no Canva. Sai mais rápido que insistir.

---

## Checklist antes de subir no Meta

- [ ] Cada letra conferida, sem palavra inventada no fundo
- [ ] `$6,90` com **vírgula**, não ponto
- [ ] Texto principal no terço central (fora dos 150px do topo e 250px da base)
- [ ] Texto ocupa no máximo ~20% da área da imagem
- [ ] Nenhum peixe morto na imagem 2
- [ ] Nenhuma palavra legível na tela do notebook na imagem 3
