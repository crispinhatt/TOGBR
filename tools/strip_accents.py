#!/usr/bin/env python3
"""
Gera uma versao sem acentos dos arquivos Story*.int, para contornar a
limitacao de fonte da caixa de dialogo (ver COMO_FUNCIONA.md).

Uso: python3 strip_accents.py <pasta_origem> <pasta_destino>
Copia TOGGame.int/TOGGameUI.int/CastleGame.int sem alteracao (a fonte deles
suporta acento) e remove acentos apenas dos arquivos Story*.
"""
import unicodedata
import glob
import os
import sys
import shutil

def remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize('NFD', text)
    return ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 strip_accents.py <pasta_origem> <pasta_destino>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)

    for path in sorted(glob.glob(os.path.join(src, "*"))):
        fname = os.path.basename(path)
        if fname.lower().startswith("story"):
            with open(path, 'r', encoding='cp1252', newline='') as f:
                content = f.read()
            with open(os.path.join(dst, fname), 'w', encoding='cp1252', newline='') as f:
                f.write(remove_accents(content))
            print(f"Sem acento: {fname}")
        else:
            shutil.copy(path, os.path.join(dst, fname))
            print(f"Copiado sem alteracao: {fname}")

if __name__ == "__main__":
    main()
