import os
import glob
import html

def oku(dosya):
    with open(dosya, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def temiz_ad(ad):
    ad = ad.replace("_", " ").strip()
    ad = " ".join([x for x in ad.split(" ") if x])
    return ad

def ayikla(dosya_adi):
    base = os.path.basename(dosya_adi)
    base = os.path.splitext(base)[0]
    parca = base.split("_")
    if len(parca) >= 2:
        case = parca[-1]
        algo = "_".join(parca[:-1])
        return algo, case
    return base, "case?"

def yaz(hedef, icerik):
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    with open(hedef, "w", encoding="utf-8") as f:
        f.write(icerik)

def uret():
    cikti_klasor = "cikti"
    dosyalar = sorted(glob.glob(os.path.join(cikti_klasor, "*.txt")))

    kartlar = []
    algolar = set()
    caseler = set()

    for yol in dosyalar:
        algo, case = ayikla(yol)
        algolar.add(algo)
        caseler.add(case)
        metin = oku(yol)
        kartlar.append({
            "algo": algo,
            "case": case,
            "yol": yol,
            "baslik": f"{temiz_ad(algo)} / {case}",
            "icerik": metin
        })

    algolar = sorted(list(algolar))
    caseler = sorted(list(caseler))

    kart_html = []
    for i, k in enumerate(kartlar):
        icerik = html.escape(k["icerik"])
        kart_html.append(f"""
        <div class="kart" data-algo="{html.escape(k["algo"])}" data-case="{html.escape(k["case"])}">
          <div class="ust">
            <div class="baslik">{html.escape(k["baslik"])}</div>
            <div class="alt">{html.escape(k["yol"])}</div>
          </div>
          <pre class="icerik" id="k{i}">{icerik}</pre>
        </div>
        """)

    algo_ops = ['<option value="hepsi">Hepsi</option>'] + [f'<option value="{html.escape(a)}">{html.escape(temiz_ad(a))}</option>' for a in algolar]
    case_ops = ['<option value="hepsi">Hepsi</option>'] + [f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in caseler]

    sayfa = f"""
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CPU Zamanlama - Rapor</title>
<style>
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 0; background: #0b0f14; color: #e8eef6; }}
  .kapsam {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
  .bas {{ display:flex; gap:12px; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; }}
  h1 {{ margin:0; font-size: 22px; }}
  .kontroller {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }}
  .kontroller label {{ font-size: 12px; opacity: .9; display:flex; flex-direction:column; gap:6px; }}
  select, input {{
    background:#121a24; color:#e8eef6; border:1px solid #243244; border-radius:10px; padding:10px 12px;
    outline:none;
  }}
  input {{ width: 260px; }}
  .sayac {{ font-size: 12px; opacity: .85; margin-top: 10px; }}
  .grid {{ display:grid; grid-template-columns: 1fr; gap: 14px; margin-top: 16px; }}
  .kart {{ background:#0f1620; border:1px solid #1f2b3a; border-radius:16px; overflow:hidden; }}
  .ust {{ padding: 14px 14px 0 14px; }}
  .baslik {{ font-size: 15px; font-weight: 650; }}
  .alt {{ font-size: 12px; opacity: .75; margin-top: 4px; }}
  pre {{
    margin: 12px 0 0 0; padding: 14px; background:#0b0f14; border-top:1px solid #1f2b3a;
    overflow:auto; max-height: 420px; white-space: pre-wrap; word-break: break-word;
  }}
  .yok {{ padding: 22px; border: 1px dashed #2b3a4f; border-radius: 16px; opacity: .85; }}
</style>
</head>
<body>
  <div class="kapsam">
    <div class="bas">
      <div>
        <h1>CPU Zamanlama – Interaktif Rapor</h1>
        <div class="sayac" id="sayac"></div>
      </div>
      <div class="kontroller">
        <label>Case
          <select id="caseSec">
            {''.join(case_ops)}
          </select>
        </label>
        <label>Algoritma
          <select id="algoSec">
            {''.join(algo_ops)}
          </select>
        </label>
        <label>Arama
          <input id="ara" type="text" placeholder="P001, Ortalama, Throughput...">
        </label>
      </div>
    </div>

    <div class="grid" id="grid">
      {''.join(kart_html) if kart_html else '<div class="yok">cikti/ klasöründe .txt dosyası bulunamadı.</div>'}
    </div>
  </div>

<script>
  const caseSec = document.getElementById("caseSec");
  const algoSec = document.getElementById("algoSec");
  const ara = document.getElementById("ara");
  const grid = document.getElementById("grid");
  const sayac = document.getElementById("sayac");

  function filtrele() {{
    const c = caseSec.value;
    const a = algoSec.value;
    const q = (ara.value || "").toLowerCase().trim();

    let goster = 0;
    const kartlar = grid.querySelectorAll(".kart");

    kartlar.forEach(k => {{
      const kc = k.getAttribute("data-case");
      const ka = k.getAttribute("data-algo");
      const metin = k.innerText.toLowerCase();

      let ok = true;
      if (c !== "hepsi" && kc !== c) ok = false;
      if (a !== "hepsi" && ka !== a) ok = false;
      if (q && !metin.includes(q)) ok = false;

      k.style.display = ok ? "" : "none";
      if (ok) goster++;
    }});

    sayac.textContent = `Görünen sonuç: ${goster}`;
  }}

  caseSec.addEventListener("change", filtrele);
  algoSec.addEventListener("change", filtrele);
  ara.addEventListener("input", filtrele);
  filtrele();
</script>
</body>
</html>
"""
    yaz(os.path.join("rapor", "rapor.html"), sayfa)

if __name__ == "__main__":
    uret()
