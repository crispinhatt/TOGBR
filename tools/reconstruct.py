#!/usr/bin/env python3
import re
import json
import os
import sys

SRC_DIR = "original"
EXTRACTED_DIR = "extracted_data"
TRANS_DIR = "translations"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

QUOTED_RE = re.compile(r'"([^"]*)"')

def reconstruct_file(fname):
    orig_path = os.path.join(SRC_DIR, fname)
    extracted_path = os.path.join(EXTRACTED_DIR, fname + ".json")
    trans_path = os.path.join(TRANS_DIR, fname + ".json")

    with open(orig_path, 'r', encoding='utf-8-sig', newline='') as f:
        lines = f.readlines()

    if not os.path.exists(trans_path):
        print(f"AVISO: sem traducoes para {fname}, copiando original sem alteracao")
        translations = {}
    else:
        with open(trans_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)

    with open(extracted_path, 'r', encoding='utf-8') as f:
        extracted = json.load(f)

    for entry in extracted["entries"]:
        line_no = entry["line_no"]
        raw_line = lines[line_no]
        line_ending = ''
        if raw_line.endswith('\r\n'):
            line_ending = '\r\n'
            body = raw_line[:-2]
        elif raw_line.endswith('\n'):
            line_ending = '\n'
            body = raw_line[:-1]
        else:
            body = raw_line

        matches = list(QUOTED_RE.finditer(body))
        new_body = body
        for s in reversed(entry["strings"]):
            if not s["translatable"]:
                continue
            key = f'{line_no}|{s["idx"]}'
            if key not in translations:
                continue
            translated_text = translations[key]
            if s.get("kind") == "unquoted":
                start, end = s["start"], s["end"]
                new_body = new_body[:start] + translated_text + new_body[end:]
            else:
                m = matches[s["idx"]]
                new_body = new_body[:m.start(1)] + translated_text + new_body[m.end(1):]

        lines[line_no] = new_body + line_ending

    out_path = os.path.join(OUT_DIR, fname)
    # CRITICO: o UDK nao decodifica .int como UTF-8 -- ele le byte a byte
    # como Windows-1252/ANSI. Escrever em UTF-8 faz cada acentuado (2 bytes)
    # virar mojibake no jogo (ex: "ã" -> "Ã£"). Por isso usamos cp1252 aqui.
    with open(out_path, 'w', encoding='cp1252', newline='') as f:
        f.writelines(lines)
    print(f"Gerado: {out_path}")

def main():
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = [f[:-5] for f in os.listdir(EXTRACTED_DIR) if f.endswith('.json')]
    for fname in targets:
        reconstruct_file(fname)

if __name__ == "__main__":
    main()
