import csv

def dosyadan_cek(yol):
    liste = []
    with open(yol, encoding="utf-8") as f:
        oku = csv.DictReader(f)
        for s in oku:
            liste.append({
                "id": s["Process_ID"],
                "g": int(s["Arrival_Time"]),
                "s": int(s["CPU_Burst_Time"]),
                "k": int(s["CPU_Burst_Time"]),
                "o": s["Priority"]
            })
    return liste


def sure_hesapla(zamanlar):
    ilk = {}
    son = {}
    calisti = {}

    for b, p, s in zamanlar:
        if p == "IDLE":
            continue
        if p not in ilk:
            ilk[p] = b
        son[p] = s
        calisti[p] = calisti.get(p, 0) + (s - b)

    bekle = {}
    donus = {}

    for p in son:
        donus[p] = son[p]
        bekle[p] = donus[p] - calisti[p]

    return bekle, donus


def ort_maks(veri):
    if len(veri) == 0:
        return 0, 0
    t = 0
    m = 0
    for v in veri.values():
        t += v
        if v > m:
            m = v
    return t / len(veri), m


def kac_tane_bitti(zamanlar, noktalar):
    cikti = {}
    for n in noktalar:
        bitti = []
        for _, p, s in zamanlar:
            if p != "IDLE" and s <= n and p not in bitti:
                bitti.append(p)
        cikti[n] = len(bitti)
    return cikti


def degisim_say(zamanlar):
    once = ""
    say = 0
    for _, p, _ in zamanlar:
        if p != once:
            if once != "":
                say += 1
            once = p
    if say > 0:
        say -= 1
    return say


def cpu_oran(zamanlar, cs_sure=0.001):
    top = 0
    bos = 0

    for b, p, s in zamanlar:
        fark = s - b
        top += fark
        if p == "IDLE":
            bos += fark

    cs = degisim_say(zamanlar)
    dolu = top - bos - (cs * cs_sure)

    if top == 0:
        return 0
    return dolu / top
