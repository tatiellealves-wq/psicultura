from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1350
F="fonts/"
def font(f,s): return ImageFont.truetype(F+f,s)
FRA=lambda s: font("Fraunces-900.ttf",s)
FRAI=lambda s: font("Fraunces-400i.ttf",s)
HK7=lambda s: font("Hanken-700.ttf",s)
MONO=lambda s: font("SpaceMono-700.ttf",s)

CREAM=(251,247,238); GOLD=(232,217,174); GOLD2=(190,154,69); INK=(20,42,32)

def cover(img):
    r=max(W/img.width,H/img.height)
    im=img.resize((int(img.width*r),int(img.height*r)),Image.LANCZOS)
    x=(im.width-W)//2; y=(im.height-H)//2
    return im.crop((x,y,x+W,y+H))

def vgrad(top_rgba,bot_rgba,h):
    g=Image.new('RGBA',(1,h))
    for i in range(h):
        t=i/(h-1)
        g.putpixel((0,i),tuple(int(top_rgba[k]+(bot_rgba[k]-top_rgba[k])*t) for k in range(4)))
    return g.resize((W,h))

def tracked(d,xy,text,fnt,fill,track):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=fnt,fill=fill)
        x+=d.textlength(ch,font=fnt)+track
    return x

def seg_width(d,segs,fh,fe):
    return sum(d.textlength(t,font=(fe if s=='e' else fh)) for t,s in segs)

def build(bg_path,eyebrow,lines,cta,out):
    base=cover(Image.open(bg_path).convert('RGB')).convert('RGBA')
    # top scrim para o texto
    top=vgrad((15,42,32,235),(15,42,32,0),760)
    base.alpha_composite(top,(0,0))
    # bottom scrim para o CTA/marca
    both=vgrad((15,42,32,0),(9,26,20,240),430)
    base.alpha_composite(both,(0,H-430))
    d=ImageDraw.Draw(base)
    mx=74
    # eyebrow
    tracked(d,(mx,92),eyebrow,MONO(24),GOLD,6)
    d.line([(mx,140),(mx+64,140)],fill=GOLD2,width=3)
    # hook
    fh=FRA(66); fe=FRAI(66); lh=80; y=176
    for segs in lines:
        x=mx
        for t,s in segs:
            f=fe if s=='e' else fh
            col=GOLD if s=='e' else CREAM
            d.text((x,y),t,font=f,fill=col)
            x+=d.textlength(t,font=f)
        y+=lh
    # CTA pill
    ctaf=HK7(38); tw=d.textlength(cta,font=ctaf)
    pw=tw+72; ph=76; px=mx; py=H-250
    d.rounded_rectangle([px,py,px+pw,py+ph],radius=ph//2,fill=GOLD2)
    d.text((px+36,py+ph/2-26),cta,font=ctaf,fill=(58,44,7))
    # seta
    ax=px+pw-30; ay=py+ph/2
    d.line([(ax-8,ay),(ax+8,ay)],fill=(58,44,7),width=4)
    d.line([(ax+2,ay-8),(ax+8,ay),(ax+2,ay+8)],fill=(58,44,7),width=4,joint='curve')
    # marca + bonos
    tracked(d,(mx,py+ph+26),"SALUDEDUCATIVA.SHOP",MONO(22),GOLD,5)
    # tag guía+4 bonos (canto sup direito)
    tg="GUÍA + 4 BONOS"; tf=MONO(21); tgw=d.textlength(tg,font=tf)
    d.rounded_rectangle([W-tgw-72,92,W-40,132],radius=20,outline=GOLD,width=2)
    d.text((W-tgw-56,100),tg,font=tf,fill=GOLD)
    base.convert('RGB').save(out,'JPEG',quality=90,optimize=True)
    print('ok',out)

build("bg/bg1.png","MÉTODO VIENTRE LIGERO",
      [[("No es tu fuerza",'h')],[("de voluntad.",'h')],[("Es tu barriga",'h')],[("inflamada",'e'),(".",'h')]],
      "Descubre el plan","creativo-1-culpa.jpg")

build("bg/bg2.png","¿POR QUÉ SIEMPRE HINCHADA?",
      [[("Esa pancita no",'h')],[("siempre es grasa.",'h')],[("Muchas veces",'h')],[("es ",'h'),("hinchazón",'e'),(".",'h')]],
      "Quiero desinflamarme","creativo-2-sintoma.jpg")

build("bg/bg3.png","EL ERROR MÁS COMÚN",
      [[("5 alimentos",'h')],[("“",'h'),("saludables",'e'),("”",'h')],[("que te mantienen",'h')],[("hinchado.",'h')]],
      "Ver los 5 alimentos","creativo-3-error.jpg")

build("bg/bg4.png","SIN PASTILLAS · 21 DÍAS",
      [[("De hinchada",'h')],[("y pesada…",'h')],[("a ",'h'),("ligera",'e'),(" en",'h')],[("21 días.",'h')]],
      "Empezar ahora","creativo-4-deseo.jpg")
