# jogo-cinmon
Projeto da matéria introdução a programação ofertada pelo Cin-UFPE

# CINMON — protótipo de batalha (Pygame-CE)

Primeira versão jogável: tela de batalha 480×270, exibida em 960×540 (2x),
com pixel art sem suavização, Charcará contra Vampteuth e navegação por WASD.

## 1. Requisitos

- Python 3.10 ou superior (recomendado)
- Windows, macOS ou Linux

## 2. Instalação

Abra o terminal dentro da pasta `CINMON` e execute:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando):**
```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

Instale o Pygame-CE:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Executar

Na pasta do projeto:

```bash
python main.py
```

## 4. Controles

- Na tela inicial, clique em **JOGAR** ou pressione **Enter/Espaço** para abrir a placa.
- Na placa, clique em **BATALHA** para iniciar; **Esc** ou **ESC - Voltar** retorna à tela inicial.
- Na batalha, **W A S D** movem a seleção. **Enter/Espaço** confirmam.
- Também é possível clicar nas opções do menu de batalha e nos ataques. Cada ataque consome 1 QR.
- Depois do ataque do jogador, pressione **Enter/Espaço** ou clique na tela para o adversário contra-atacar.
- Nas mensagens de **MOCHILA** e **CINMON**, pressione **Enter/Espaço** ou clique para voltar ao menu.
- **FUGIR** ou **Esc** fecha a batalha e retorna ao menu principal.
- Na tela de fim da batalha, **Enter/Espaço** ou clique fecha a batalha.

## 5. Arquivos

```text
CINMON/
├── main.py
├── requirements.txt
├── README.md
└── assets/
    └── cinmons/
        ├── charcara_costas.png
        └── vampteuth_frente.png
```

Os fundos quadriculados/brancos das imagens de origem foram removidos nas bordas
para gerar PNGs com transparência. Revise os sprites; se algum detalhe de fundo
tiver permanecido, podemos ajustar a máscara.

## 6. Próximas etapas

1. Separar dados dos CINMON e ataques em arquivos JSON.
2. Adicionar animações de ataque e efeitos de dano.
3. Implementar troca de CINMON, bolsa e captura.
4. Adicionar vantagens e desvantagens entre tipos.
5. Adaptar a execução para navegador com Pygbag.
6. Publicar a versão web usando GitHub Pages.

## 7. Navegador e GitHub

Primeiro teste localmente com `python main.py`. Depois que o protótipo estiver
estável, vamos adaptar o loop principal para o modo assíncrono exigido pelo
Pygbag e preparar a publicação. O GitHub guarda o código; GitHub Pages hospeda
os arquivos web gerados, não executa Python/Pygame diretamente.

## Bibliotecas utilizada

pygame (pygame-ce)
sys
os
pathlib