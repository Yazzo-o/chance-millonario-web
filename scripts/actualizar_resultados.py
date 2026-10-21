#!/usr/bin/env python3
"""Consulta fuentes oficiales y solo guarda valores que pasan validaciones básicas."""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"resultados.json"
SUPER_URL="https://supergirossucre.com.co/"
CHANCE_URL="https://www.chancemillonario.com/index.php"
HEADERS={"User-Agent":"Mozilla/5.0 (compatible; ChanceMillonarioUpdater/1.0)"}

class PageText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ("script","style","noscript"): self.skip+=1
        alt=a.get("alt") or a.get("title")
        if alt and any(k in alt.lower() for k in ("cifra","acumulado","chance millonario")):
            self.parts.append(alt)
    def handle_endtag(self,tag):
        if tag in ("script","style","noscript") and self.skip: self.skip-=1
    def handle_data(self,data):
        if not self.skip and data.strip(): self.parts.append(re.sub(r"\s+"," ",data).strip())

def get_text(url):
    req=Request(url,headers=HEADERS)
    with urlopen(req,timeout=35) as res:
        if res.status!=200: raise RuntimeError(f"HTTP {res.status}: {url}")
        html=res.read().decode("utf-8","replace")
    p=PageText(); p.feed(html); return " ".join(p.parts)

def numbers(region):
    return [int(x.replace(".","")) for x in re.findall(r"(?<!\d)(?:\$\s*)?(\d{1,3}(?:\.\d{3})+)(?!\d)",region)]

def extract_accumulations(text):
    low=text.lower(); a=low.find("modalidad 3 cifras"); b=low.find("modalidad 4 cifras")
    end=low.find("resultados",b if b>=0 else 0)
    if a<0 or b<0: raise RuntimeError("No se hallaron las dos modalidades en SuperGIROS.")
    n3=numbers(text[a:b]); n4=numbers(text[b:end if end>b else len(text)])
    if len(n3)<8 or len(n4)<8: raise RuntimeError(f"Formato no reconocido (3 cifras={len(n3)}, 4 cifras={len(n4)} valores).")
    bets={1000,2000,3000,5000}
    def rows(nums,cifras):
        out=[]
        for i in range(0,8,2):
            stake,value=nums[i],nums[i+1]
            if stake not in bets or value<=0: raise RuntimeError("Pareja apuesta/acumulado no válida.")
            out.append({"cifras":cifras,"apuesta":"$"+format(stake,",").replace(",","."),"valor":value})
        if {x["apuesta"] for x in out}!={"$1.000","$2.000","$3.000","$5.000"}:
            raise RuntimeError("Las cuatro apuestas no están completas.")
        return out
    def grand(cifras):
        m=re.search(rf"{cifras}\s*cifras\s+Gran\s+Acumulado\s*\$?\s*([\d.]+)",text,re.I)
        if not m:return None
        value=int(m.group(1).replace(".",""))
        return value if value>0 else None
    return rows(n3,3)+rows(n4,4),grand(3),grand(4)

def extract_chance(text):
    m=re.search(r"Acumulado\s+(\d{2}-\d{2}-\d{4}|20\d{2}-\d{2}-\d{2})\s*[#$ ]*\s*([\d.]{7,})",text,re.I)
    if not m: raise RuntimeError("No se encontró acumulado acompañado por fecha.")
    value=int(m.group(2).replace(".",""))
    if not 100_000_000<=value<=100_000_000_000: raise RuntimeError("El acumulado está fuera del rango esperado.")
    return m.group(1),value

def extract_results(text):
    pat=re.compile(r"([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9 .'-]{2,38}?)\s+(20\d{2}-\d{2}-\d{2})\s+(\d)\s+(\d)\s+(\d)\s+(\d)(?=\s|$)")
    allowed=("ANTIOQUEÑITA","CAFETERITO","CHONTICO","DORADO","CARIBEÑA","CULONA","FANTASTICA","MOTILON","PAISITA","PIJAO","SAMAN","SINUANO")
    out=[];seen=set()
    for m in pat.finditer(text):
        name=re.sub(r"\s+"," ",m.group(1)).strip()
        if not any(name.startswith(k) for k in allowed):continue
        row={"nombre":name,"fecha":m.group(2),"numero":"".join(m.group(i) for i in range(3,7))}
        key=(row["nombre"],row["fecha"])
        if key not in seen:seen.add(key);out.append(row)
    if not out:raise RuntimeError("No se validaron resultados de cuatro cifras.")
    return out[:60]

def main():
    old=json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    updates=[];errors=[]
    try:
        rows,g3,g4=extract_accumulations(get_text(SUPER_URL))
        old["acumulados"]=rows
        if g3 is not None:old["gran_acumulado_3"]=g3
        if g4 is not None:old["gran_acumulado_4"]=g4
        updates.append("acumulados SuperGIROS")
    except Exception as e:errors.append("SuperGIROS: "+str(e))
    try:
        text=get_text(CHANCE_URL)
        date,value=extract_chance(text);results=extract_results(text)
        old["principal"]={"apuesta":"$6.000","valor":value,"fecha":date}
        old["resultados"]=results
        updates.append("acumulado y resultados Chance Millonario")
    except Exception as e:errors.append("Chance Millonario: "+str(e))
    if not updates:
        print("No se guardaron cambios: ninguna fuente pasó validación.\n"+"\n".join(errors),file=sys.stderr)
        sys.exit(1)
    old["fuentes"]={"supergiros_sucre":SUPER_URL,"chance_millonario":CHANCE_URL}
    old["actualizado_en"]=datetime.now(ZoneInfo("America/Bogota")).isoformat(timespec="seconds")
    old["estado"]="actualizado" if not errors else "actualizado-parcial"
    old["errores"]=errors
    OUT.write_text(json.dumps(old,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Estado={old['estado']}; acumulados={len(old.get('acumulados',[]))}; resultados={len(old.get('resultados',[]))}")
    if errors:print("\n".join(errors))
if __name__=="__main__":main()
