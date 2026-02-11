# 🌌 Multiverso Bot - Sistema de Votação com Slash Commands

Bot para Discord que realiza votações mensais onde o vencedor tem seu apelido aplicado a **TODOS** os membros do servidor, criando um "multiverso" onde todos compartilham a mesma identidade temporária.

## 🎭 Como Funciona

1. **Admin cadastra** participantes com `/adicionar`
2. **Bot inicia** votação mensal com enquete nativa do Discord
3. **Membros votam** na enquete (24 horas)
4. **Vencedor é escolhido** baseado nos votos
5. **TODOS do servidor** recebem o apelido do vencedor automaticamente
6. **Sistema de rodízio** garante que todos sejam escolhidos pelo menos uma vez

## ✨ Funcionalidades

- 🗳️ **Enquetes nativas do Discord** - Interface profissional
- 🤖 **Votações automáticas** - Todo dia 1 de cada mês
- 🎭 **Alteração massiva** de apelidos
- 🔄 **Sistema de rodízio** - Garante que todos participem
- 📊 **Histórico completo** de vencedores
- 💾 **Persistência de dados** em JSON
- ⚡ **Slash Commands** - Comandos modernos e fáceis de usar
- 🔘 **Botões interativos** - Confirmações visuais

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Permissões de administrador no servidor Discord
- Bot com permissões específicas (ver seção de instalação)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/lucas5/amongversito-bot.git
cd amongversito-bot
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv bot_env
source bot_env/bin/activate  # Linux/Mac
# ou
bot_env\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Bot no Discord

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications)
2. Clique em **"New Application"**
3. Dê um nome ao bot (ex: "Multiverso Bot")
4. Vá em **"Bot"** no menu lateral
5. Clique em **"Add Bot"**
6. Em **"Privileged Gateway Intents"**, ative:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT
7. Clique em **"Reset Token"** e copie o token

### 5. Convide o Bot para seu Servidor

⚠️ **IMPORTANTE:** Para Slash Commands funcionarem, você precisa marcar a opção correta!

1. No Portal de Desenvolvedores, vá em **"OAuth2"** > **"URL Generator"**
2. Em **"Scopes"**, marque:
   - ✅ `bot`
   - ✅ `applications.commands` ← **OBRIGATÓRIO para Slash Commands!**
3. Em **"Bot Permissions"**, marque:
   - ✅ Manage Nicknames
   - ✅ Send Messages
   - ✅ Add Reactions
   - ✅ Read Message History
4. Copie o URL gerado e cole no navegador
5. Selecione seu servidor e autorize

### 6. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
nano .env  # ou use seu editor preferido
```

Preencha com suas informações:

```env
# Token do bot Discord
DISCORD_TOKEN=seu_token_aqui

# ID do canal onde as votações serão postadas automaticamente
# Para pegar o ID: Ative o Modo Desenvolvedor no Discord
# Clique direito no canal → Copiar ID
CANAL_VOTACAO_ID=123456789012345678
```

### 7. Inicie o Bot

```bash
python multiverso_bot.py
```

Você deve ver:

```
🔄 Sincronizando slash commands...
✅ 9 slash commands sincronizados!
🎭 MultiversoBot está online!
🌌 Sistema Multiverso ativado!
⏰ Agendador automático ativado!
```

### 8. Sincronize os Comandos (Se necessário)

Se os comandos não aparecerem ao digitar `/`, use:

```
!sync
```

Aguarde alguns segundos e tente novamente. Pode demorar até 1 hora para sincronizar globalmente.

## 🎯 Como Usar

### Comandos de Slash (/)

Digite `/` no Discord para ver todos os comandos disponíveis!

#### 📝 Gerenciamento (Apenas Admin)

```
/adicionar @Usuario apelido
```
Adiciona um participante ao Multiverso
- **Exemplo:** `/adicionar @João SuperJoão`

```
/remover @Usuario
```
Remove um participante do Multiverso

```
/lista
```
Mostra todos os participantes cadastrados
- ✅ = Já foi escolhido
- ⏳ = Aguardando
- 👑 = Atual campeão

#### 🗳️ Votação (Apenas Admin)

```
/multiverso
```
Inicia uma votação manualmente
- Cria enquete nativa do Discord
- Duração: 24 horas
- Máximo: 10 candidatos

```
/finalizar
```
Encerra a votação antes do prazo
- Conta os votos
- Aplica o apelido vencedor a todos

#### 📊 Consulta (Todos podem usar)

```
/historico
```
Mostra os últimos 10 vencedores com datas e votos

```
/help
```
Mostra o guia completo do bot

#### 🔧 Manutenção (Apenas Admin)

```
/resetar
```
⚠️ Reseta TODO o sistema (com confirmação por botões)

```
/resetar_escolhidos
```
Reseta apenas a lista de "já escolhidos"
- Permite que todos participem novamente

## 🤖 Sistema Automático

### Votação Mensal Automática

- **Início:** Todo dia 1 às 00:00 UTC
- **Duração:** 24 horas
- **Encerramento:** Automático
- **Aplicação:** Automática

O bot:
1. Verifica a cada hora se é dia 1
2. Cria a enquete automaticamente no canal configurado
3. Após 24h, finaliza e aplica o resultado
4. Exclui vencedores das próximas votações
5. Reseta quando todos já foram escolhidos

### Sistema de Rodízio

- Quem ganhou não participa de novo
- Quando todos foram escolhidos, a lista reseta
- Garante que todos participem pelo menos uma vez

## 📖 Exemplo Completo

```bash
# 1. Admin adiciona participantes
/adicionar @João SuperJoão
/adicionar @Maria MariaDasGalaxias
/adicionar @Pedro PedroVerse
/adicionar @Ana AnaCosmico

# 2. Verifica a lista
/lista

# 3. Inicia votação (ou aguarda dia 1 automático)
/multiverso

# 4. Enquete aparece - Todos votam clicando nas opções

# 5. Após 24h, bot finaliza automaticamente
# OU use /finalizar para encerrar antes

# RESULTADO: Todos do servidor agora são "SuperJoão"!

# 6. Próximo mês:
# João não aparece na votação
# Quando todos ganharem, João volta a participar
```

## ⚙️ Configuração Avançada

### Hierarquia de Cargos

⚠️ **IMPORTANTE:** O cargo do bot deve estar **ACIMA** dos cargos que ele vai gerenciar!

1. Configurações do Servidor → Cargos
2. Arraste o cargo do bot para cima
3. Deve ficar assim:
   ```
   👑 Dono (imutável)
   🤖 Multiverso Bot  ← DEVE ESTAR AQUI
   👥 Outros cargos
   @everyone
   ```

### Alterar Horário/Dia da Votação

Edite `multiverso_bot.py`:

```python
# Para dia 15 em vez de dia 1
if now.day == 15 and now.hour == 0:

# Para às 12:00 em vez de 00:00
if now.day == 1 and now.hour == 12:
```

### Alterar Duração da Votação

```python
# Para 48 horas em vez de 24
duration=timedelta(hours=48)
```

## 📁 Estrutura do Projeto

```
amongversito-bot/
├── multiverso_bot.py          # Código principal
├── multiverso_data.json       # Dados salvos (auto-criado)
├── requirements.txt           # Dependências Python
├── .env                       # Configurações (NÃO commitar!)
├── .env.example              # Template de configuração
├── .gitignore                # Arquivos ignorados pelo Git
├── README.md                 # Este arquivo
└── LICENSE                   # Licença MIT
```

## 💾 Formato dos Dados (JSON)

```json
{
  "participantes": {
    "123456789": {
      "nome": "João",
      "apelido": "SuperJoão",
      "user_id": 123456789
    }
  },
  "ja_escolhidos": ["123456789"],
  "atual_escolhido": "123456789",
  "historico": [
    {
      "user_id": "123456789",
      "nome": "João",
      "apelido": "SuperJoão",
      "data": "2026-02-10T20:00:00",
      "votos": 15,
      "automatico": true
    }
  ]
}
```

## ⚠️ Limitações

1. **Hierarquia:** Bot não pode alterar apelidos de membros com cargos superiores
2. **Dono do Servidor:** Normalmente não pode ter apelido alterado
3. **Bots:** São automaticamente excluídos
4. **Máximo de Candidatos:** 10 por votação (limitação do Discord)
5. **Tamanho do Apelido:** 55 caracteres (limitação das enquetes)

## 🐛 Solução de Problemas

### Slash Commands não aparecem

**Problema:** Ao digitar `/` os comandos do bot não aparecem

**Soluções:**
1. Verifique se marcou `applications.commands` ao convidar o bot
2. Use `!sync` no Discord para forçar sincronização
3. Aguarde até 1 hora (sincronização global demora)
4. Reconvide o bot com as permissões corretas
5. Reinicie o Discord completamente

### Bot não altera apelidos

**Problema:** Votação funciona mas apelidos não mudam

**Soluções:**
- ✅ Cargo do bot está **acima** dos outros?
- ✅ Bot tem permissão "Gerenciar Apelidos"?
- ✅ Você é dono ou tem cargo alto demais?

### Votação não inicia automaticamente

**Problema:** Dia 1 chegou mas nada aconteceu

**Soluções:**
- ✅ `CANAL_VOTACAO_ID` está configurado no `.env`?
- ✅ Bot tem permissão para enviar mensagens no canal?
- ✅ Há participantes cadastrados?
- ✅ Bot está rodando 24/7?

### Erro ao finalizar

**Problema:** `/finalizar` dá erro

**Soluções:**
- ✅ Há uma votação ativa?
- ✅ A mensagem da enquete ainda existe?
- ✅ Aguarde alguns segundos após criar a enquete

## 🔒 Segurança

- ✅ Nunca compartilhe o arquivo `.env`
- ✅ Nunca commite o token no Git
- ✅ Use `.gitignore` (já configurado)
- ✅ Faça backup do `multiverso_data.json`
- ✅ Limite acesso admin a pessoas confiáveis

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🎉 Créditos

- Desenvolvido para criar caos controlado no Discord 🎭
- Baseado em discord.py 2.3+
- Usa as enquetes nativas do Discord

## 📞 Suporte

- 🐛 [Reportar Bug](https://github.com/lucas5/amongversito-bot/issues)
- 💡 [Sugerir Funcionalidade](https://github.com/lucas5/amongversito-bot/issues)
- 📖 [Documentação do Discord.py](https://discordpy.readthedocs.io/)

## 🚀 Roadmap

Futuras melhorias planejadas:

- [ ] Dashboard web para gerenciamento
- [ ] Estatísticas avançadas de votação
- [ ] Suporte a múltiplos servidores
- [ ] Notificações por DM
- [ ] Temas personalizáveis
- [ ] Integração com bancos de dados
- [ ] Comandos de contexto (clique direito)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!

**Transforme seu servidor em um multiverso! 🌌**
