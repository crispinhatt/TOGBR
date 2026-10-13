#!/usr/bin/env python3
import re
import json
import glob
import os

SRC_DIR = "original"
OUT_DIR = "extracted_data"
os.makedirs(OUT_DIR, exist_ok=True)

QUOTED_RE = re.compile(r'"([^"]*)"')
UNQUOTED_KV_RE = re.compile(r'^([A-Za-z0-9_\[\]\(\)]+)\s*[=:]\s*([^\r\n;]+?)\s*(;.*)?$')
UNQUOTED_BLOCKLIST = {'true', 'false', 'none', 'yes', 'no'}

def is_translatable(s: str) -> bool:
    s_stripped = s.strip()
    if not s_stripped:
        return False
    if re.fullmatch(r'-?\d+(\.\d+)?%?', s_stripped):
        return False
    if re.fullmatch(r'\d{1,2}[a-zA-Z]', s_stripped):
        return False
    if not re.search(r'[A-Za-zÀ-ÿ]', s_stripped):
        return False
    return True

def process_file(path):
    with open(path, 'r', encoding='utf-8-sig', errors='strict', newline='') as f:
        lines = f.readlines()

    entries = []
    for i, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if re.match(r'^\d+Mug\s*=', stripped, re.IGNORECASE):
            continue
        matches = list(QUOTED_RE.finditer(raw_line))
        if matches:
            strings = []
            for idx, m in enumerate(matches):
                text = m.group(1)
                strings.append({
                    "idx": idx,
                    "text": text,
                    "translatable": is_translatable(text),
                    "kind": "quoted"
                })
            if any(s["translatable"] for s in strings):
                entries.append({
                    "line_no": i,
                    "raw_line": raw_line.rstrip('\r\n'),
                    "strings": strings
                })
            continue

        if not stripped or stripped.startswith('[') or stripped.startswith(';'):
            continue
        m = UNQUOTED_KV_RE.match(stripped)
        if not m:
            continue
        value = m.group(2).strip()
        if value.lower() in UNQUOTED_BLOCKLIST:
            continue
        if is_translatable(value):
            val_start = raw_line.find(value)
            if val_start == -1:
                continue
            entries.append({
                "line_no": i,
                "raw_line": raw_line.rstrip('\r\n'),
                "strings": [{
                    "idx": 0,
                    "text": value,
                    "translatable": True,
                    "kind": "unquoted",
                    "start": val_start,
                    "end": val_start + len(value)
                }]
            })
    return entries, lines

def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*")))
    summary = {}
    for path in files:
        fname = os.path.basename(path)
        if fname.lower().endswith('.txt'):
            continue
        try:
            entries, lines = process_file(path)
        except Exception as e:
            print(f"ERRO em {fname}: {e}")
            continue
        out_path = os.path.join(OUT_DIR, fname + ".json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump({"source_file": fname, "total_lines": len(lines), "entries": entries}, f, ensure_ascii=False, indent=2)
        n_translatable = sum(1 for e in entries for s in e["strings"] if s["translatable"])
        summary[fname] = n_translatable
        print(f"{fname}: {len(entries)} linhas, {n_translatable} strings traduziveis")

    print("\n=== RESUMO ===")
    print(f"Total de strings traduziveis: {sum(summary.values())}")

if __name__ == "__main__":
    main()
