import os
import sys

from yardimci import dosyadan_cek

from fcfs import fcfs_rapor
from sjf_kesmesiz import sjf_kesmesiz_rapor
from oncelik_kesmesiz import oncelik_kesmesiz_rapor
from sjf_kesmeli import sjf_kesmeli_rapor

try:
    from oncelik_kesmeli import oncelik_kesmeli_rapor
except Exception:
    oncelik_kesmeli_rapor = None

try:
    from round_robin import round_robin_rapor
except Exception:
    round_robin_rapor = None


def calistir(case_yolu, etiket):
    surecler = dosyadan_cek(case_yolu)

    os.makedirs("cikti", exist_ok=True)

    fcfs_rapor(surecler, os.path.join("cikti", f"fcfs_{etiket}.txt"))
    sjf_kesmesiz_rapor(surecler, os.path.join("cikti", f"sjf_kesmesiz_{etiket}.txt"))
    sjf_kesmeli_rapor(surecler, os.path.join("cikti", f"sjf_kesmeli_{etiket}.txt"))
    oncelik_kesmesiz_rapor(surecler, os.path.join("cikti", f"oncelik_kesmesiz_{etiket}.txt"))

    if oncelik_kesmeli_rapor:
        oncelik_kesmeli_rapor(surecler, os.path.join("cikti", f"oncelik_kesmeli_{etiket}.txt"))

    if round_robin_rapor:
        round_robin_rapor(surecler, os.path.join("cikti", f"round_robin_{etiket}.txt"))


def main():
    case1 = os.path.join("veri", "case1.csv")
    case2 = os.path.join("veri", "case2.csv")

    if len(sys.argv) == 2:
        tek = sys.argv[1].strip().lower()
        if tek in ["1", "case1"]:
            calistir(case1, "case1")
            return
        if tek in ["2", "case2"]:
            calistir(case2, "case2")
            return

    calistir(case1, "case1")
    calistir(case2, "case2")


if __name__ == "__main__":
    main()
