#!/usr/bin/env python3
"""Actualizador prudente: extrae acumulados/resultados de las dos fuentes.
No modifica resultados.json si no puede validar cifras reales en el HTML obtenido.
"""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "resultados.json"
URL_SUPER = "https://supergirossucre.com.co/"
URL_CHANCE = "https://www.chancemillonario.com/index.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ChanceMillonarioUpdater/1.0; +https://github.com/Yazzo-o/chance-millonario-web)"}

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style","noscript"): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("script","style","noscript") and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(re.sub(r"\s+"," ",data).strip())

def get_text(url):
    req=Request(url,headers=HEADERS)
    with urlopen(req,timeout=30) as response:
        html=response.read().decode("utf-8","replace")
    parser=TextExtractor(); parser.feed(html)
    return "\n".join(parser.parts)

def money(s):
    return int(re.sub(r"\D","",s))

def extract_supergiros(text):
    # El sitio suele presentar los valores como etiquetas de apuesta seguidas
    # por su acumulado. Exigimos valores claros para evitar guardar datos parciales.
    rows=[]
    lines=[re.sub(r"\s+"," ",x).strip() for x in text.splitlines() if x.strip()]
    for i,line in enumerate(lines):
        if "Modalidad 3 cifras" in line or "Modalidad 4 cifras" in line:
            cifras=3 if "3 cifras" in line else 4
            window=" ".join(lines[i:i+30])
            pairs=re.findall(r"\$\s*([1-5]\.000)\s+\$\s*([\d.]{5,})",window)
            for apuesta,valor in pairs[:4]:
                rows.append({"cifras":cifras,"apuesta":"$"+apuesta,"valor":money(valor),"fuente":"SuperGIROS Sucre"})
    # Filtra duplicados manteniendo el orden.
    unique={}
    for row in rows: unique[(row["cifras"],row["apuesta"])]=row
    return list(unique.values())

def extract_chance(text):
    # El acumulado destacado se identifica por el rótulo y fecha que le anteceden.
    patterns=[
        r"Acumulado\s+\d{2}[-/]\d{2}[-/]\d{4}\s+\$?\s*([\d.]{8,})",
        r"Acumulado\s+\d{4}-\d{2}-\d{2}\s+\$?\s*([\d.]{8,})",
    ]
    for pattern in patterns:
        match=re.search(pattern,text,re.I)
        if match:
            return money(match.group(1))
    return None

def extract_results(text):
    # La fuente presenta nombres de sorteos, fecha ISO y cuatro dígitos.
    rows=[]
    pattern=re.compile(r"([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9 .'-]{2,40})\s+(20\d{2}-\d{2}-\d{2})\s+(\d)\s+(\d)\s+(\d)\s+(\d)(?=\s|$)")
    for m in pattern.finditer(text):
        name=re.sub(r"\s+"," ",m.group(1)).strip()
        if any(word in name for word in ("ACUMULADO","RESULTADOS","CHANCE MILLONARIO")): continue
        rows.append({"nombre":name,"fecha":m.group(2),"numero":"".join(m.group(i) for i in range(3,7))})
    seen=set(); out=[]
    for r in rows:
        key=(r["nombre"],r["fecha"])
        if key not in seen: seen.add(key); out.append(r)
    return out[:60]

def main():
    try:
        sg_text=get_text(URL_SUPER)
        ch_text=get_text(URL_CHANCE)
        sg=extract_supergiros(sg_text)
        jackpot=extract_chance(ch_text)
        results=extract_results(ch_text)
        # Se requiere al menos una extracción válida antes de guardar. No inventa cifras.
        if not sg and jackpot is None and not results:
            raise RuntimeError("Las fuentes respondieron, pero la estructura de datos no coincide con los patrones validados.")
        existing=json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        data={
            "fuentes":{"supergiros_sucre":URL_SUPER,"chance_millonario":URL_CHANCE},
            "actualizado_en":datetime.now().astimezone().isoformat(timespec="seconds"),
            "estado":"actualizado-parcial" if not sg or jackpot is None or not results else "actualizado",
            "acumulados":sg or existing.get("acumulados",[]),
            "principal":{"apuesta":"$6.000","valor":jackpot if jackpot is not None else (existing.get("principal") or {}).get("valor")},
            "resultados":results or existing.get("resultados",[]),
            "notas":"Los datos que no se pudieron validar conservan el último valor guardado."
        }
        OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("Actualización guardada:",data["estado"],"acumulados:",len(data["acumulados"]),"resultados:",len(data["resultados"]),"principal:",data["principal"]["valor"])
    except Exception as exc:
        print("ERROR: no se reemplazó data/resultados.json:",exc,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__": main()
