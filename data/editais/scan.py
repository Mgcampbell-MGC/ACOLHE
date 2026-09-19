import urllib.request, json, sys, re, datetime, concurrent.futures, threading
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
PAT=re.compile(r'NATALIDAD|ENXOVAL|MATERNIDADE|LAYETTE|BEBE|BEBÊ', re.I)
BASE="https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
lock=threading.Lock(); hits=[]; errors=[]
def get(url, tries=4):
    for t in range(tries):
        try:
            r=urllib.request.Request(url, headers={'User-Agent':UA,'Accept':'application/json'})
            with urllib.request.urlopen(r, timeout=45) as f: return json.loads(f.read().decode('utf-8'))
        except Exception as e:
            if t==tries-1: 
                with lock: errors.append((url,str(e)[:120]))
                return None
            import time; time.sleep(2*(t+1))
def day(d, mod):
    ds=d.strftime('%Y%m%d'); p=1
    while True:
        j=get(f"{BASE}?dataInicial={ds}&dataFinal={ds}&codigoModalidadeContratacao={mod}&pagina={p}&tamanhoPagina=50")
        if not j or not j.get('data'): return
        for rec in j['data']:
            o=(rec.get('objetoCompra') or '')
            if PAT.search(o):
                with lock: hits.append(rec)
        if p>=j.get('totalPaginas',1): return
        p+=1
start=datetime.date(2026,3,1); end=datetime.date(2026,9,19)
days=[start+datetime.timedelta(days=i) for i in range((end-start).days+1)]
tasks=[(d,m) for d in days for m in (6,8)]   # 6=pregao eletronico, 8=dispensa
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    list(ex.map(lambda t: day(*t), tasks))
json.dump({'hits':hits,'errors':errors}, open('/home/user/ACOLHE/data/editais/pncp_familyA_scan_kit.json','w'), ensure_ascii=False, indent=1)
print("hits",len(hits),"errors",len(errors))
