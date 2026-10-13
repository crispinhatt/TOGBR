# Como Funciona — Detalhes Técnicos

## O formato `.int`

Tower of Guns roda em UDK (Unreal Engine 3), cuja localização usa arquivos `.int`, um formato tipo INI com seções `[NomeDaClasse]` e pares `Chave=Valor`. Os arquivos ficam em:

```
<pasta do jogo>\UDKGame\Localization\INT\
```

(A pasta `Engine\Localization\INT\` contém só arquivos do motor, como `Core.int` e `Engine.int`; os textos do jogo não estão lá.)

Há duas variações no mesmo arquivo:

```ini
[Story0]
107="I could be the bad guy. Or a sidekick. Or your mother. WHO KNOWS!"
107Mug="04g"
```

```ini
[TOGGameUI]
LocExit=Exit
LocNewGame=NewGame
```

Nem todo valor traduzível vem entre aspas. Um extrator que só procura `"..."` perde texto real, como os títulos de "rank" e várias mensagens de loading.

## Ferramentas (`tools/`)

Todas rodam a partir de uma pasta de trabalho com esta estrutura:

```
trabalho/
  original/        <- copie aqui os .int originais do jogo (UDKGame\Localization\INT)
  translations/    <- os JSONs deste repositório
  tools/
```

- **`extract.py`**: varre `original/` e gera `extracted_data/*.json`, com cada string traduzível e sua posição exata (linha + índice, ou offset de caractere para valores sem aspas). Campos `NNNMug=` (código do retrato de quem fala) são sempre ignorados.
- **`reconstruct.py`**: lê `original/`, `extracted_data/` e `translations/` e grava os arquivos traduzidos em `output/`, trocando **só** o trecho traduzido e preservando o resto da linha, comentários e terminadores de linha.
- **`strip_accents.py <origem> <destino>`**: gera a variante sem acentos dos arquivos `Story*` (normalização Unicode NFD + remoção de diacríticos) e copia os demais sem alteração.

Cada arquivo em `translations/` é um JSON `{"linha|índice": "texto traduzido"}`. Chaves ausentes mantêm o texto original, o que foi usado de propósito para os nomes próprios de armas, itens e inimigos.

## Detalhes de encoding (importante)

- **Gravar em Windows-1252 (cp1252), não em UTF-8.** O UDK lê os `.int` byte a byte. Em UTF-8 cada acento ocupa 2 bytes e vira dois símbolos no jogo (`ã` → `Ã£`, `é` → `Ã©`, `Ê` → caixinha). O arquivo pode parecer perfeito num editor de texto e mesmo assim quebrar no jogo. Confirmado em testes: após trocar para cp1252, HUD e estatísticas passaram a exibir os acentos corretamente.
- **Sem BOM.** Os originais não têm BOM.
- **CRLF preservado.** Os arquivos usam `\r\n`.

## Um bug do jogo original

Vários arquivos (`Story0`, `Story8`, `Story9`, `Story11`, `Story12`) têm linhas `NNNMug="XXg` com a aspa de fechamento faltando. Isso já existe no jogo original. O parser ignora essas linhas e a reconstrução não as altera.

## Decisões de localização

- **Nomes próprios em inglês:** armas, itens e inimigos (`Kegerator`, `Mini-LHC`, `Hugbot`, `Spinbot`, `Amoebombot`...) foram tratados como nomes de "marca", como o próprio título "Tower of Guns".
- **Falas, descrições, mensagens de loading e títulos de rank foram traduzidos**, adaptando trocadilhos quando a tradução literal não funcionava. Exemplos: o capítulo "Bro" virou "Mano"; "DMV" virou "Detran"; "Murder, She Wrote" virou "Costa a Costa".
- **Arquivos de fora do escopo:** `utgame.int`, `UTGameUI.int`, `UTGameContent.int`, `UDKGameUI.int`, `GFxUI.int` (herança do template UT3/UDK, não usados aqui) e `NwwChar-Sheet.txt` (nota de desenvolvimento sobre os códigos de retrato).

## Limitações e o que foi tentado

### 1. Fonte da caixa de diálogo sem acentos minúsculos

O corpo das falas mostra uma caixinha vazia no lugar de `á é ê í ó ô õ ú ã ç`, enquanto o título da caixa e o HUD mostram acentos normalmente. A explicação mais provável (hipótese, não verificada) é que a fonte do corpo de texto seja um atlas de glifos gerado só com os caracteres do inglês. Isso não se resolve editando `.int`.

**Contorno aplicado:** a pasta `Localization_SemAcentos/`.

### 2. Menu principal, opções e perks em inglês

Em testes, o menu principal, quase todas as opções e a lista de perks apareceram em inglês, mesmo com `TOGGameUI.int` e a seção de perks do `TOGGame.int` traduzidos. Hipótese: esses textos estão embutidos em pacotes `.upk` (interface GFx/Flash) ou em valores padrão compilados em `TOGGame.u`, e não são lidos desses `.int`. **Não foi verificado.**

### 3. Tentativa de editar os pacotes (não concluída)

- `UDK.exe editor` na instalação da Steam trava com `Failed to find file for package EngineMaterials for async preloading`. A instalação é "cozida" (*cooked*): só existe `CookedPC/`, sem os pacotes de conteúdo originais que o UnrealEd exige. Há código do editor dentro do `.exe`, mas ele não roda sobre essa instalação.
- O UDK-2015-02 (último SDK público) chegou a ser instalado em outra pasta, mas os testes de abrir os `.upk` do jogo nele **não foram concluídos**. Riscos conhecidos: o jogo usa uma build mais antiga do UDK, e pacotes cozidos podem não abrir direto no editor.

## Pontos de partida para quem quiser continuar

1. Descobrir qual `UFont` a caixa de diálogo usa. Candidatos: classes de HUD dentro de `CookedPC\TOGGame.u` (decompilável com ferramentas como UE Explorer) e os pacotes em `CookedPC\TOGupk\GFx\` e `CookedPC\baseUEDstuff\UT3\GFx\`.
2. Estender o charset dessa fonte com os acentos do português (reimportar no UnrealEd ou editar o pacote por outra via) e testar com a pasta `Localization_ComAcentos/`.
3. Descobrir de onde vêm os textos do menu e dos perks (SWF/GFx dentro de `.upk`?) e traduzi-los lá.
4. Se algum dia as traduções forem atualizadas: refazer `extract.py` → `reconstruct.py` → `strip_accents.py`, sempre testando acentos dentro do jogo.
