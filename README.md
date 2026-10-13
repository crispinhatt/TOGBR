# Tower of Guns — Tradução PT-BR

> Tradução não-oficial **parcial** de Tower of Guns para o Português do Brasil.

> ## 🛑 Projeto abandonado
> Este projeto **não receberá novas versões**. O texto traduzido que passa pelos arquivos `.int` está pronto e funciona, mas parte da interface do jogo (menu principal, opções, perks) não é alcançada por esse método e continua em inglês, e a fonte da caixa de diálogo não tem letras acentuadas minúsculas. Resolver isso exigiria editar pacotes binários do jogo (`.upk`), o que não foi possível. Detalhes na seção *Limitações conhecidas* abaixo e em [COMO_FUNCIONA.md](COMO_FUNCIONA.md). Fique à vontade para fazer um fork e continuar.

---

## 📋 Sobre o projeto

Este projeto assim como sua documentação foram feitos inteiramente com o uso da plataforma CLAUDE, sendo apenas alguns poucos termos revisados manualmente.

Tower of Guns (Terrible Posture Games, 2014) é um FPS roguelite feito em UDK (Unreal Engine 3). O jogo sorteia, a cada corrida, uma de 27 mini-histórias absurdas e cômicas (paródias de Exterminador do Futuro, apocalipse zumbi, DETRAN, Senhor dos Anéis, espionagem canina e outras). Este projeto traduz **2.499 entradas** dos arquivos de localização `.int` do jogo.

**Versão do jogo testada:** Steam, em PC. O teste foi **parcial**: menus, HUD, tela de estatísticas e algumas falas de diálogo foram vistos em jogo; o jogo não foi zerado com a tradução instalada.

---

## ✅ O que foi traduzido

| Arquivo(s) | Entradas | Descrição |
| --- | --- | --- |
| `Story0` a `Story26` + `Story999` | 1.706 | Os 27 capítulos de história aleatória e as mensagens do desenvolvedor (marcos de corridas e glitches) |
| `TOGGame.int` | 741 | HUD, tela de estatísticas, títulos de "rank" de fim de vida, mensagens de loading, nomes de modos de jogo, textos de itens e power-ups |
| `TOGGameUI.int` | 50 | Rótulos de menu e opções (ver limitações: o jogo não os exibe) |
| `CastleGame.int` | 2 | Placar Preto/Branco |
| **Total** | **2.499** | de 2.574 entradas identificadas |

As ~75 entradas restantes são nomes próprios de armas, itens e inimigos (ex.: `Kegerator`, `Mini-LHC`, `Blatherskite`, `Hugbot`), mantidos em inglês de propósito, como nomes de "marca".

Arquivos herdados do template Unreal Tournament 3/UDK (`utgame.int`, `UTGameUI.int`, `UTGameContent.int`, `UDKGameUI.int`, `GFxUI.int`) ficaram de fora por não serem usados neste jogo.

---

## ⚠️ Limitações conhecidas

Observadas em testes dentro do jogo:

- **Menu principal e opções continuam em inglês.** `NEW GAME`, `COLLECTION`, `OPTIONS`, `CREDITS`, `EXIT` e quase todas as opções gráficas/áudio aparecem em inglês, apesar de `TOGGameUI.int` estar traduzido. Esses textos provavelmente estão embutidos nos pacotes `.upk` do jogo (interface em Flash/GFx), fora do alcance dos `.int`. Só aparecem em português alguns rótulos, como `Modo Demo` e `Ativar Console`.
- **Perks continuam em inglês** na tela de seleção (nomes e descrições), pelo mesmo motivo provável. Armas e itens aparecem com nome em inglês (intencional); as descrições de armas ao passar o mouse estão em português.
- **Fonte da caixa de diálogo sem acentos minúsculos.** O corpo das falas mostra uma caixinha vazia no lugar de `á é ê í ó ô õ ú ã ç`. O título acima da caixa e a interface/HUD/estatísticas usam outra fonte e exibem acentos normalmente. Por isso existem duas pastas de instalação (veja abaixo).
- **Pequenos problemas de layout:** no HUD, o aviso "Pressione E / Para Usar" aparece sobreposto/cortado; na tela de fim de fase, o ícone do botão sobrepõe parte de "ESPAÇO" e aparece `META DA FASE: NONE` (valor vindo do jogo).
- Não foi feita uma partida completa para procurar outros erros.

---

## 🛠️ Como instalar

Escolha **uma** das duas pastas:

| Pasta | Quando usar |
| --- | --- |
| [`Localization_SemAcentos/`](Localization_SemAcentos/) | **Recomendada.** Falas dos capítulos sem acentuação (`voce`, `nao`, `alem`), evitando as caixinhas vazias. HUD, estatísticas e demais arquivos continuam acentuados. |
| [`Localization_ComAcentos/`](Localization_ComAcentos/) | Tradução completa acentuada. As falas mostram caixinhas vazias nas letras acentuadas minúsculas. |

Você também pode baixar os `.zip` prontos na seção [Releases](https://github.com/crispinhatt/TOGBR/releases).

### Passo a passo

**1. Faça backup dos arquivos originais**

Copie a pasta abaixo para outro lugar (ou use "Verificar integridade dos arquivos" da Steam depois, para restaurar):

```
<pasta do jogo>\UDKGame\Localization\INT\
```

Na Steam o caminho costuma ser `...\steamapps\common\TowerofGuns\UDKGame\Localization\INT\`.

**2. Copie os arquivos traduzidos**

Copie os 31 arquivos `.int` da pasta escolhida para dentro de `UDKGame\Localization\INT\`, confirmando a substituição.

**3. Jogue**

Abra o jogo normalmente. Não é preciso trocar nenhuma configuração de idioma.

---

## 🔄 Como desinstalar / restaurar

1. Feche o jogo.
2. Restaure o backup de `UDKGame\Localization\INT\`, **ou** na Steam clique com o botão direito no jogo → Propriedades → Arquivos Instalados → *Verificar integridade dos arquivos*.

---

## ⚠️ Avisos

- Esta é uma tradução **não-oficial**, sem relação com a Terrible Posture Games.
- Se o jogo for atualizado, pode ser necessário reaplicar os arquivos.
- Como o projeto está abandonado, **não há suporte** e issues podem não ser respondidas.

---

## 🔧 Para desenvolvedores / quem quiser continuar

Veja [COMO_FUNCIONA.md](COMO_FUNCIONA.md): formato dos `.int`, funcionamento das ferramentas em [`tools/`](tools/), as traduções em [`translations/`](translations/) (um JSON por arquivo) e um resumo do que foi tentado para resolver as limitações acima. Dois pontos que valem a atenção de quem for mexer:

- Os `.int` do UDK precisam ser gravados em **Windows-1252**, não em UTF-8 (senão cada acento vira lixo no jogo).
- Os pontos de partida mais promissores para resolver as limitações estão listados no fim do COMO_FUNCIONA.md.

---

## 📜 Licença

Este projeto está licenciado sob a MIT License (veja [LICENSE](LICENSE)).

Tower of Guns © Joe Mirabello / Terrible Posture Games LLC. Este projeto é uma tradução não-oficial e não possui vínculo com os detentores da propriedade intelectual.
