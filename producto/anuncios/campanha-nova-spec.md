# Campanha nova — especificação completa

Substitui CP 15 e CP 16. Estrutura consolidada, 4 criativos, 6 países.

---

## Estrutura

```
1 CAMPANHA
└── 1 CONJUNTO
    ├── Criativo 1 — El orden
    ├── Criativo 2 — La semana 2
    ├── Criativo 3 — Los números
    └── Criativo 4 — Ya lo intentaste
```

**Um conjunto só.** Não separe por país nem por criativo — fragmentar divide as
conversões e nenhum conjunto sai do aprendizado.

---

## CAMPANHA

| Campo | Valor |
|---|---|
| Nome | `TILAPIA · ONDA1 · 29-07` |
| Objetivo | **Vendas** |
| Orçamento | **Orçamento da campanha (CBO)** — não no conjunto |
| Valor | **R$ 80/dia** |
| Estratégia de lance | Maior volume (sem limite de custo) |
| Teste A/B | Desligado |
| Advantage+ campanha | Ligado |

**Por que R$80/dia:** com 4 criativos dá ~R$20 por criativo/dia. A CPM de ~R$60,
são ~330 impressões diárias cada — em 7 dias, ~2.300 por criativo, o suficiente
para o Meta julgar cada um.

**Não suba o orçamento na primeira semana.** Foi exatamente isso que degradou a
CP15 (custo por IC subiu de R$20 para R$34 conforme o orçamento subiu).

---

## CONJUNTO

| Campo | Valor |
|---|---|
| Nome | `CJT · 6 PAISES · AMPLO` |
| Evento de conversão | **Compra** |
| Pixel | `2630923590655993` |
| Janela de atribuição | 7 dias clique, 1 dia visualização (padrão) |

### Países (só estes 6)

```
México · Colombia · República Dominicana · Perú · Ecuador · Guatemala
```

**NÃO inclua:** EUA, Canadá, Espanha, Chile, Uruguai, Paraguai, Venezuela,
Bolívia, Argentina.

Motivo de cada corte está em `paises-analise.md` — resumo: EUA CPM R$220,
Canadá R$394, Chile e Uruguai água fria (tilápia não cresce), Venezuela
pagamento inviável, Paraguai R$8,45 por visita.

### Público

| Campo | Valor |
|---|---|
| Idade | **25 – 65+** |
| Gênero | Todos |
| Segmentação detalhada | **VAZIA** — nenhum interesse |
| Público Advantage+ | **Ligado** |
| Idioma | deixe vazio |

Interesses viraram sugestão, não filtro. **O criativo é a segmentação agora.**

### Posicionamentos

**Advantage+ (automáticos).** Não force manual.

---

## ANÚNCIOS (os 4, no mesmo conjunto)

| Nome do anúncio | Imagem | Copy |
|---|---|---|
| `A1-ORDEN` | 1080×1350 | Criativo 1 |
| `A2-SEMANA2` | 1080×1350 | Criativo 2 |
| `A3-NUMEROS` | 1080×1350 | Criativo 3 |
| `A4-INTENTO` | 1080×1350 | Criativo 4 |

Textos completos em `criativos-estaticos-onda1.md`.
CTA dos quatro: **Mais informações**

### ⚠️ URL — o passo que já quebrou antes

No campo **"URL do site"**, cole isto **antes de publicar pela primeira vez**:

```
https://cultivorentabledetilapia.online/?utm_source=facebook&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

E deixe **"Parâmetros de URL" VAZIO**.

**Por quê:** o Meta congela o valor das macros na primeira publicação. Se você
publicar sem elas e editar depois, elas chegam literais (`{{campaign.name}}`) e
a UTMify não consegue ler a campanha. Foi o que aconteceu com as campanhas
antigas e o motivo de você ter tido que duplicar tudo.

---

## Checklist antes de publicar

- [ ] Orçamento **na campanha**, não no conjunto
- [ ] **Um** conjunto só
- [ ] Evento de conversão = **Compra**
- [ ] Só os 6 países
- [ ] Segmentação detalhada **vazia**
- [ ] Os 4 anúncios dentro do mesmo conjunto
- [ ] URL completa com UTMs em **"URL do site"**
- [ ] "Parâmetros de URL" **vazio**
- [ ] Idade 25–65+

## Depois de publicar

1. Espere as **primeiras impressões** da campanha nova
2. **Só então** pause CP 15 e CP 16 (e as outras 8)
3. **Não mexa em nada por 5 a 7 dias** — nem orçamento, nem criativo, nem país

---

## O que medir no dia 7

| Métrica | Hoje | Meta |
|---|---|---|
| CPM | R$60–72 | < R$55 |
| Custo por visita | R$2,21–2,58 | < R$2,00 |
| Custo por IC | R$26–34 | < R$20 |
| Visita → IC | ~7% | > 12% |
| IC → compra | ~4% | > 15% |
| Custo por venda | R$182 | < R$72 |

**R$72 é o ponto de equilíbrio** (receita líquida do Plan Completo). Abaixo
disso a campanha se paga.

Se no dia 7 o custo por venda estiver entre R$72 e R$120, vale insistir e
otimizar. Acima de R$150, o problema não é a campanha — é o ticket de $14,90,
e aí a conversa passa a ser sobre preço.
