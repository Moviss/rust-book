#!/usr/bin/env python3
"""Bramki G1 (.md), G2 (.toml) i G5 (ostrzeżenia) dla tłumaczenia.

Użycie:
  sprawdz.py [--ref REV] <pliki...>        porównanie z `git show REV:<ścieżka>`
  sprawdz.py --orig PLIK_EN <plik_pl>       porównanie z jawnie podanym oryginałem
Opcje: --cicho (tylko podsumowanie ostrzeżeń), --wyjatki PLIK.
Kod wyjścia 1, jeśli są BŁĘDY.
"""
import argparse
import difflib
import re
import sys
import tomllib
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wspolne import HEADING_ID_RE, REPO, git_show, parse, rel  # noqa: E402

WYJATKI = Path(__file__).resolve().parent / "wyjatki.toml"

TAG_RE = re.compile(
    r"<(/?)([A-Za-z][\w-]*)"
    r"((?:\s+[\w:.-]+(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'>]+))?)*)\s*/?>"
)
ATTR_RE = re.compile(r"([\w:.-]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s\"'>]+))?")
DIRECTIVE_RE = re.compile(r"\{\{#[^}]*\}\}")
PERM_RE = re.compile(r"@Perm(\[[^\]]*\])?\{[^}]*\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CODE_HTML_RE = re.compile(r"<code\b[^>]*>(.*?)</code>", re.S)
FOOTNOTE_RE = re.compile(r"\[\^[^\]\s]+\]")
ID_ATTR_RE = re.compile(r"\bid\s*=\s*\"([^\"]*)\"")
FENCE_RE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[`~]*\s*$")
NOTE_EN_RE = re.compile(r"(?m)^\s*>\s?Note: ")
NOTE_PL_RE = re.compile(r"(?m)^\s*>\s?Uwaga: ")
FILE_EN = '<span class="filename">Filename: '
FILE_PL = '<span class="filename">Plik: '
IGNORED_ATTRS = {"alt", "title", "caption"}
FUNCTION_WORDS = {
    "the", "and", "of", "is", "that", "with", "this", "which", "are", "you",
}
WORD_RE = re.compile(r"[A-Za-zÀ-žĄąĆćĘęŁłŃńÓóŚśŹźŻż’']+")


class Raport:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.bledy = []
        self.ostrzezenia = []

    def blad(self, gate, msg):
        self.bledy.append(f"BŁĄD [{gate}] {msg}")

    def ostrz(self, gate, msg):
        self.ostrzezenia.append(f"OSTRZEŻENIE [{gate}] {msg}")


# ---------------------------------------------------------------- Markdown


def tag_key(name, attrs, closing):
    pairs = []
    for m in ATTR_RE.finditer(attrs):
        k = m.group(1).lower()
        if k in IGNORED_ATTRS:
            continue
        pairs.append((k, m.group(2) or ""))
    return ("/" if closing else "") + name + "".join(
        f" {k}={v}" for k, v in sorted(pairs)
    )


def without_fences(text):
    return FENCE_RE.sub("", text)


def analiza_md(text):
    """Zwraca słownik cech dokumentu Markdown."""
    tokens = parse(text)
    lines = text.split("\n")
    szkielet = []  # (klucz, linia)
    urle = Counter()
    tagi = Counter()
    kod_inline = Counter()
    akapity = []  # (linia, tekst bez kodu)

    def add(key, tok):
        line = tok.map[0] + 1 if tok.map else 0
        szkielet.append((key, line))

    def walk(toks, top_line=None):
        for i, tok in enumerate(toks):
            if tok.type == "heading_open":
                raw = lines[tok.map[0]]
                m = HEADING_ID_RE.search(raw)
                add(("nagłówek", tok.tag, m.group(1) if m else None), tok)
            elif tok.type in ("fence", "code_block"):
                add(("kod", tok.info, tok.content), tok)
            elif tok.type == "blockquote_open":
                add(("cytat",), tok)
            elif tok.type == "table_open":
                rows, cols, j = 0, [], i + 1
                while toks[j].type != "table_close":
                    if toks[j].type == "tr_open":
                        rows += 1
                        cols.append(0)
                    elif toks[j].type in ("th_open", "td_open"):
                        cols[-1] += 1
                    j += 1
                add(("tabela", rows, tuple(cols)), tok)
            elif tok.type == "html_block":
                content = tok.content
                if content.lstrip().startswith("<pre"):
                    add(("pre", content.strip()), tok)
                for m in TAG_RE.finditer(content):
                    key = tag_key(m.group(2), m.group(3), m.group(1))
                    if m.group(2) == "Listing":
                        add(("listing", key), tok)
                    else:
                        tagi[key] += 1
                    for am in ATTR_RE.finditer(m.group(3)):
                        if am.group(1).lower() == "href" and am.group(2):
                            urle[am.group(2).strip("\"'")] += 1
            elif tok.type == "inline":
                plain = []
                for ch in tok.children or []:
                    if ch.type == "code_inline":
                        kod_inline[ch.content] += 1
                    elif ch.type == "link_open":
                        urle[ch.attrs.get("href", "")] += 1
                    elif ch.type == "image":
                        urle["img:" + ch.attrs.get("src", "")] += 1
                        plain.append(ch.content)
                    elif ch.type == "html_inline":
                        m = TAG_RE.fullmatch(ch.content.strip())
                        if m:
                            tagi[tag_key(m.group(2), m.group(3), m.group(1))] += 1
                            for am in ATTR_RE.finditer(m.group(3)):
                                if am.group(1).lower() == "href" and am.group(2):
                                    urle[am.group(2).strip("\"'")] += 1
                    elif ch.type == "text":
                        plain.append(ch.content)
                    elif ch.type == "softbreak":
                        plain.append(" ")
                akapity.append((tok.map[0] + 1 if tok.map else 0, "".join(plain)))

    walk(tokens)

    # Dyrektywy w kolejności (poza kodem, bo kod i tak musi być identyczny).
    nofence = without_fences(text)
    for m in DIRECTIVE_RE.finditer(nofence):
        szkielet.append((("dyrektywa", m.group(0)), 0))
    return {
        "szkielet": szkielet,
        "urle": urle,
        "tagi": tagi,
        "kod_inline": kod_inline,
        "perm": Counter(m.group(0) for m in PERM_RE.finditer(text)),
        "komentarze": Counter(COMMENT_RE.findall(text)),
        "code_html": Counter(CODE_HTML_RE.findall(nofence)),
        "przypisy": Counter(FOOTNOTE_RE.findall(nofence)),
        "id": Counter(ID_ATTR_RE.findall(nofence)),
        "uwagi": len(NOTE_EN_RE.findall(text)),
        "uwagi_pl": len(NOTE_PL_RE.findall(text)),
        "pliki": text.count(FILE_EN),
        "pliki_pl": text.count(FILE_PL),
        "akapity": akapity,
    }


def opis(key):
    s = " ".join(str(k) for k in key)
    return s if len(s) < 160 else s[:157] + "..."


def porownaj_szkielet(r, en, pl, dodatkowe):
    # Dyrektywy porównujemy osobno: szkielet bloków i lista dyrektyw.
    def split(sk):
        bloki = [(k, l) for k, l in sk if k[0] != "dyrektywa"]
        dyr = [k for k, _ in sk if k[0] == "dyrektywa"]
        return bloki, dyr

    en_b, en_d = split(en)
    pl_b, pl_d = split(pl)
    if en_d != pl_d:
        r.blad("G1", f"dyrektywy {{{{#...}}}} różnią się: EN={en_d} PL={pl_d}")
    a = [k for k, _ in en_b]
    b = [k for k, _ in pl_b]
    if a == b:
        return
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    wstawione = 0
    problemy = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "insert":
            wstawione += j2 - j1
        for j in range(j1, j2):
            problemy.append(
                f"linia PL {pl_b[j][1]}: nadmiarowy/zmieniony element: {opis(b[j])}"
            )
        for i in range(i1, i2):
            problemy.append(
                f"linia EN {en_b[i][1]}: brak/zmieniony element: {opis(a[i])}"
            )
        if op != "insert":
            wstawione = 10**9
    if wstawione <= dodatkowe:
        return
    for p in problemy[:20]:
        r.blad("G1", "szkielet: " + p)
    if len(problemy) > 20:
        r.blad("G1", f"szkielet: ... i {len(problemy) - 20} kolejnych różnic")


def porownaj_multizbior(r, gate, nazwa, en, pl, dozwolone=()):
    brak = en - pl
    nadmiar = pl - en
    for k in dozwolone:
        if nadmiar[k]:
            nadmiar[k] -= 1
    nadmiar = +nadmiar
    for k, n in brak.items():
        r.blad(gate, f"{nazwa}: brakuje {n}× {k!r}")
    for k, n in nadmiar.items():
        r.blad(gate, f"{nazwa}: nadmiarowe {n}× {k!r}")


def porownaj_kod_inline(r, gate, en, pl, gdzie=""):
    for k in pl:
        if k not in en:
            r.blad(gate, f"{gdzie}kod inline nie istnieje w oryginale: `{k}`")
    if en != pl:
        brak = en - pl
        nadmiar = pl - en
        roz = [f"-{n}× `{k}`" for k, n in brak.items()] + [
            f"+{n}× `{k}`" for k, n in nadmiar.items() if k in en
        ]
        if roz:
            r.ostrz(gate, f"{gdzie}liczność kodu inline inna: " + ", ".join(roz[:10]))


def g5_akapity(r, en_akapity, pl_akapity, gdzie=""):
    en_set = {t.strip() for _, t in en_akapity if len(WORD_RE.findall(t)) >= 4}
    for line, t in pl_akapity:
        tt = t.strip()
        words = WORD_RE.findall(tt)
        if len(words) < 4:
            continue
        if tt in en_set:
            r.ostrz("G5", f"{gdzie}linia {line}: akapit identyczny z oryginałem: {tt[:80]!r}")
            continue
        fw = sum(1 for w in words if w.lower() in FUNCTION_WORDS)
        if fw >= 3 and fw / len(words) >= 0.08:
            r.ostrz("G5", f"{gdzie}linia {line}: dużo angielskich słów: {tt[:80]!r}")


def sprawdz_md(r, en_text, pl_text, wyj):
    en = analiza_md(en_text)
    pl = analiza_md(pl_text)
    for key, line in pl["szkielet"]:
        if key[0] == "nagłówek" and key[2] is None and not r.nazwa.endswith("SUMMARY.md"):
            r.blad("G1", f"linia {line}: nagłówek bez {{#id}}")
    porownaj_szkielet(r, en["szkielet"], pl["szkielet"], wyj.get("dodatkowe_bloki", 0))
    extra_urls = list(wyj.get("dodatkowe_urle", []))
    porownaj_multizbior(r, "G1", "URL-e linków/obrazków", en["urle"], pl["urle"], extra_urls)
    porownaj_multizbior(r, "G1", "znaczniki HTML", en["tagi"], pl["tagi"],
                        wyj.get("dodatkowe_tagi", []))
    porownaj_multizbior(r, "G1", "@Perm", en["perm"], pl["perm"])
    porownaj_multizbior(r, "G1", "komentarze HTML", en["komentarze"], pl["komentarze"])
    porownaj_multizbior(r, "G1", "<code> w HTML", en["code_html"], pl["code_html"])
    porownaj_multizbior(r, "G1", "etykiety przypisów", en["przypisy"], pl["przypisy"])
    porownaj_multizbior(r, "G1", "atrybuty id", en["id"], pl["id"])
    if pl["uwagi_pl"] + pl["uwagi"] != en["uwagi"]:
        r.blad(
            "G1",
            f"notatki: oryginał ma {en['uwagi']}× '> Note: ', tłumaczenie "
            f"{pl['uwagi_pl']}× '> Uwaga: ' i {pl['uwagi']}× '> Note: '",
        )
    elif pl["uwagi"]:
        r.ostrz("G5", f"{pl['uwagi']}× nieprzetłumaczone '> Note: ' (ma być '> Uwaga: ')")
    if pl["pliki_pl"] + pl["pliki"] != en["pliki"]:
        r.blad(
            "G1",
            f"etykiety plików: oryginał ma {en['pliki']}× 'Filename: ', "
            f"tłumaczenie {pl['pliki_pl']}× 'Plik: ' i {pl['pliki']}× 'Filename: '",
        )
    elif pl["pliki"]:
        r.ostrz("G5", f"{pl['pliki']}× nieprzetłumaczone 'Filename: ' (ma być 'Plik: ')")
    porownaj_kod_inline(r, "G1", en["kod_inline"], pl["kod_inline"])
    g5_akapity(r, en["akapity"], pl["akapity"])


# -------------------------------------------------------------------- TOML

D8_ALWAYS = [
    ("prompt", "program"),
    ("answer", "doesCompile"),
    ("answer", "lineNumber"),
    ("answer", "stdout"),
    ("prompt", "answerIndex"),
    ("prompt", "sortAnswers"),
]
CODE_ONLY_RE = re.compile(r"`[^`]*`")


def tylko_kod(s):
    if not isinstance(s, str):
        return True
    st = s.strip()
    if st.startswith("```"):
        return True
    rest = CODE_ONLY_RE.sub("", st)
    return not re.search(r"[A-Za-zÀ-ž]{2,}", rest)


def flat_keys(d, prefix=""):
    out = set()
    for k, v in d.items():
        if isinstance(v, dict):
            out |= flat_keys(v, prefix + k + ".")
        else:
            out.add(prefix + k)
    return out


def tekst_cechy(s):
    fences = [m.group(0) for m in FENCE_RE.finditer(s)]
    a = analiza_md(s)
    return fences, a


def porownaj_tekst(r, gdzie, en, pl):
    if not isinstance(en, str) or not isinstance(pl, str):
        if en != pl:
            r.blad("G2", f"{gdzie}: zmieniony typ wartości")
        return
    ef, ea = tekst_cechy(en)
    pf, pa = tekst_cechy(pl)
    if ef != pf:
        r.blad("G2", f"{gdzie}: bloki kodu różnią się od oryginału")
    porownaj_multizbior(r, "G2", f"{gdzie}: URL-e", ea["urle"], pa["urle"])
    porownaj_multizbior(r, "G2", f"{gdzie}: @Perm", ea["perm"], pa["perm"])
    porownaj_kod_inline(r, "G2", ea["kod_inline"], pa["kod_inline"], f"{gdzie}: ")
    g5_akapity(r, ea["akapity"], pa["akapity"], f"{gdzie}: ")


def sprawdz_toml(r, en_text, pl_text):
    try:
        pl = tomllib.loads(pl_text)
    except tomllib.TOMLDecodeError as e:
        r.blad("G2", f"TOML nie parsuje się: {e}")
        return
    en = tomllib.loads(en_text)
    if set(en) != set(pl):
        r.blad("G2", f"klucze najwyższego poziomu: EN={sorted(en)} PL={sorted(pl)}")
    if "multipart" in en:
        mp_en, mp_pl = en["multipart"], pl.get("multipart", {})
        if set(mp_en) != set(mp_pl):
            r.blad("G2", f"klucze [multipart]: EN={sorted(mp_en)} PL={sorted(mp_pl)}")
        for k in mp_en:
            if k in mp_pl:
                porownaj_tekst(r, f"multipart.{k}", mp_en[k], mp_pl[k])
    qe, qp = en.get("questions", []), pl.get("questions", [])
    if len(qe) != len(qp):
        r.blad("G2", f"liczba pytań: EN={len(qe)} PL={len(qp)}")
        return
    for n, (a, b) in enumerate(zip(qe, qp), 1):
        g = f"pytanie {n}"
        for k in ("id", "type", "multipart"):
            if a.get(k) != b.get(k):
                r.blad("G2", f"{g}: zmienione pole {k}: {a.get(k)!r} → {b.get(k)!r}")
        if flat_keys(a) != flat_keys(b):
            r.blad("G2", f"{g}: inne klucze: EN={sorted(flat_keys(a))} PL={sorted(flat_keys(b))}")
        ap, bp = a.get("prompt", {}), b.get("prompt", {})
        aa, ba = a.get("answer", {}), b.get("answer", {})
        sec = {"prompt": (ap, bp), "answer": (aa, ba)}
        for s, k in D8_ALWAYS:
            x, y = sec[s]
            if x.get(k) != y.get(k):
                r.blad("G2", f"{g}: zmienione pole {s}.{k}")
        typ = a.get("type")
        if typ == "ShortAnswer":
            for k in ("answer", "alternatives"):
                if aa.get(k) != ba.get(k):
                    r.blad("G2", f"{g}: zmienione pole answer.{k} (ShortAnswer)")
        if "prompt" in ap:
            porownaj_tekst(r, f"{g}.prompt", ap["prompt"], bp.get("prompt"))
        if "context" in a:
            porownaj_tekst(r, f"{g}.context", a["context"], b.get("context"))
        if typ == "MultipleChoice":
            ea_, pa_ = aa.get("answer"), ba.get("answer")
            if type(ea_) is not type(pa_):
                r.blad("G2", f"{g}: answer.answer zmienił typ (napis/lista)")
                continue
            ea_l = ea_ if isinstance(ea_, list) else [ea_]
            pa_l = pa_ if isinstance(pa_, list) else [pa_]
            ed, pd = ap.get("distractors", []), bp.get("distractors", [])
            if len(ea_l) != len(pa_l):
                r.blad("G2", f"{g}: inna długość listy answer.answer")
            if len(ed) != len(pd):
                r.blad("G2", f"{g}: inna liczba dystraktorów")
            for nazwa, xs, ys in (("answer.answer", ea_l, pa_l), ("distractors", ed, pd)):
                for i, (x, y) in enumerate(zip(xs, ys)):
                    gg = f"{g}.{nazwa}[{i}]"
                    if tylko_kod(x):
                        if x != y:
                            r.blad("G2", f"{gg}: opcja złożona z kodu musi być identyczna")
                    else:
                        porownaj_tekst(r, gg, x, y)
            opcje = [str(o).strip() for o in pa_l + pd]
            if len(set(opcje)) != len(opcje):
                r.blad("G2", f"{g}: opcje odpowiedzi nie są wzajemnie różne")


# -------------------------------------------------------------------- main


def wczytaj_wyjatki(path):
    p = Path(path)
    if not p.exists():
        return {}
    return tomllib.loads(p.read_text(encoding="utf-8"))


def sprawdz_plik(pl_path, en_text, wyj):
    r = Raport(rel(pl_path))
    pl_text = Path(pl_path).read_text(encoding="utf-8")
    if str(pl_path).endswith(".toml"):
        sprawdz_toml(r, en_text, pl_text)
    else:
        sprawdz_md(r, en_text, pl_text, wyj)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="pl-source")
    ap.add_argument("--orig")
    ap.add_argument("--cicho", action="store_true")
    ap.add_argument("--wyjatki", default=str(WYJATKI))
    ap.add_argument("pliki", nargs="+")
    args = ap.parse_args()
    if args.orig and len(args.pliki) != 1:
        ap.error("--orig wymaga dokładnie jednego pliku")
    wyjatki = wczytaj_wyjatki(args.wyjatki)
    suma_b = suma_o = 0
    for f in args.pliki:
        sciezka = rel(f)
        if args.orig:
            en_text = Path(args.orig).read_text(encoding="utf-8")
        else:
            try:
                en_text = git_show(args.ref, sciezka)
            except Exception:
                print(f"== {sciezka}\nBŁĄD [G1] brak pliku w {args.ref}")
                suma_b += 1
                continue
        r = sprawdz_plik(f, en_text, wyjatki.get(sciezka, {}))
        suma_b += len(r.bledy)
        suma_o += len(r.ostrzezenia)
        if r.bledy or (r.ostrzezenia and not args.cicho):
            print(f"== {r.nazwa}")
            for m in r.bledy:
                print(m)
            if not args.cicho:
                for m in r.ostrzezenia:
                    print(m)
        elif r.ostrzezenia and args.cicho:
            pass
    print(f"Podsumowanie: BŁĘDY {suma_b}, OSTRZEŻENIA {suma_o}")
    return 1 if suma_b else 0


if __name__ == "__main__":
    sys.exit(main())
