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

- **W A S D**: mover a seleção
- **Enter** ou **Espaço**: confirmar
- **Esc**: voltar do menu de ataques ou sair

No menu principal:
- LUTAR abre os quatro ataques.
- CINMON e BOLSA exibem mensagens de função ainda não implementada.
- FUGIR encerra a batalha de teste.

No menu de ataques:
- Cada ataque consome 1 QR.
- O dano reduz o HP do adversário.
- Se o adversário sobreviver, ele contra-ataca.
- Ao fim da batalha, Enter reinicia o teste.

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
