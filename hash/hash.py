#!/usr/bin/env python3
import operator
from collections import Counter

def read_pt_br_words(filename='/usr/share/dict/brazilian'):
    with open(filename) as f:
        lines = list(f)
    words = [line[:-1] for line in lines]
    print(f"Leu {len(words)} palavras em pt-BR")
    return words


def make_sbk_table(words):
    c = Counter()
    for word in words:
        c.update(word)
    chars = sorted(c.keys())
    print(f"Tabela SBK ({len(chars)} caracteres): {''.join(chars)}")
    return {ch: i for i, ch in enumerate(chars)}


def _sbk(text, char_to_int=ord):
    s = 0
    for ch in text:
        s += char_to_int(ch)
    return {'text': text, 'sum': s, 'sbk': s % 1000}


def _show_sbk(text, char_to_int=ord):
    info = _sbk(text, char_to_int)
    print(f'Texto: {info["text"]!r}')
    print(f'Soma: {info["sum"]}')
    print(f'SBK: {info["sbk"]:03d}')
    print()


tweet = """Uma função hash bem simples para um trecho de texto é

 "Atribua um valor pra cada caractere, some todos, e pegue os últimos 3 dígitos"

Vamos chamar essa função de SBK (Soma do Bruno Kim). Ela produz, pra qualquer texto, um número entre 000 e 999."""

def main():
    words = read_pt_br_words()
    table = make_sbk_table(words)
    def char_to_int(ch):
        if ch in table:
            return table[ch] + 1
        return ord(ch) + len(table) + 1

    def sbk(text):
        return _sbk(text, char_to_int)
    def show_sbk(text):
        return _show_sbk(text, char_to_int)
    print()
    show_sbk(tweet)
    show_sbk("patos")
    show_sbk("nadam")
    show_sbk("debaixo")
    show_sbk("d'água")
   
    from collections import Counter
    sbk_infos = [sbk(word) for word in words]
    sums = Counter(info['sum'] for info in sbk_infos)
    hashes = Counter(info['sbk'] for info in sbk_infos)

    import csv
    with open('sbk-sum-freq.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['sum', 'freq'])
        for i in range(max(sums)+1):
            w.writerow([i, sums[i]])
    with open('sbk-freq.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['hash', 'freq'])
        for i in range(1000):
            w.writerow([i, hashes[i]])

    cum = 0
    by_freq = sorted(hashes.items(), reverse=True, key=lambda entry: entry[1])
    for i, (h, freq) in enumerate(by_freq):
        #print(f"{h:03d}: {freq} (cum={cum:06d})")
        cum += freq
        if cum > len(words)/2:
            print(f"{i} hashes ocupam >50% de todas as palavras")
            break

    print()
    print("SBK:")
    print(f"  patos:   {sbk('patos')['sbk']:03d}")
    print(f"  patas:   {sbk('patas')['sbk']:03d}")
    print(f"  pat:     {sbk('pat')['sbk']:03d}")
    print(f"  patoso:  {sbk('patoso')['sbk']:03d}")

    words_201 = [word for word, info
        in zip(words, sbk_infos)
        if info['sbk'] == 201]
    smallest_201 = sorted(words_201, key = lambda s: len(s))[:200]
    print(smallest_201)

    import hashlib
    def sha256(text):
        m = hashlib.sha256()
        m.update(text.encode("utf-8"))
        x = 0
        for b in m.digest():
            x = 256*x + b
        return x
    print()
    print("SHA-256:")
    print(f"  patos:   {sha256('patos'):076d}")
    print(f"  patas:   {sha256('patas'):076d}")
    print(f"  pat:     {sha256('pat'):076d}")
    print(f"  patoso:  {sha256('patoso'):076d}")

if __name__ == '__main__':
    main()
