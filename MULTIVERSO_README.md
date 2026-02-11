# 🌌 Multiverso Bot - Sistema de Votação e Apelidos Coletivos

Bot para Discord que realiza votações mensais onde o vencedor tem seu apelido aplicado a **TODOS** os membros do servidor, criando um "multiverso" onde todos compartilham a mesma identidade temporária.

## 🎭 Como Funciona

1. **Admin cadastra** participantes e seus apelidos
2. **Bot inicia** votação mensal com enquete automática
3. **Membros votam** reagindo aos emojis
4. **Vencedor é escolhido** baseado nos votos
5. **TODOS do servidor** recebem o apelido do vencedor
6. **Processo se repete** todo mês, garantindo que todos sejam escolhidos pelo menos uma vez

## ✨ Funcionalidades

- 🗳️ **Votações automáticas** com enquetes nativas do Discord
- 🎭 **Alteração massiva** de apelidos de todos os membros
- 📊 **Sistema de rodízio** - garante que todos sejam escolhidos
- 🔄 **Auto-reset** quando todos já foram escolhidos
- 📜 **Histórico completo** de vencedores
- 🔒 **Proteção contra duplicatas** - ninguém é escolhido duas vezes antes de todos participarem
- 💾 **Persistência de dados** em JSON

## 📋 Pré-requisitos

- Python 3.8+
- Permissões de administrador no servidor
- Bot com permissões para:
  - Gerenciar Apelidos
  - Enviar Mensagens
  - Adicionar Reações
  - Ler Histórico de Mensagens

## 🚀 Instalação

### 1. Clone ou baixe os arquivos

```bash
# Se estiver usando Git
git clone https://github.com/seu-usuario/multiverso-bot.git
cd multiverso-bot
```

### 2. Crie ambiente virtual

```bash
python3 -m venv bot_env
source bot_env/bin/activate  # Linux/Mac
# ou
bot_env\Scripts\activate  # Windows
```

### 3. Instale dependências

```bash
pip install discord.py python-dotenv
```

### 4. Configure o Bot no Discord

1. Vá em https://discord.com/developers/applications
2. Crie uma nova aplicação
3. Vá em "Bot" e crie um bot
4. Ative os **Intents**:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT
5. Copie o token

### 5. Configure variáveis de ambiente

Crie um arquivo `.env`:

```env
DISCORD_TOKEN=seu_token_aqui
```

### 6. Convide o bot

Use o OAuth2 URL Generator com:
- **Scopes:** `bot`
- **Permissions:** 
  - Manage Nicknames
  - Send Messages
  - Add Reactions
  - Read Message History

## 🎯 Como Usar

### Comandos de Administrador

#### Adicionar Participantes

```
!adicionar @Usuario Apelido Legal
```
Exemplo:
```
!adicionar @João SuperJoão
!adicionar @Maria MariaDasGalaxias
```

#### Remover Participantes

```
!remover @Usuario
```

#### Ver Lista de Participantes

```
!lista
```
Mostra todos os participantes, quem já foi escolhido e o atual campeão.

#### Iniciar Votação

```
!multiverso
```
- Cria enquete automática com os candidatos disponíveis
- Adiciona reações numeradas (1️⃣, 2️⃣, etc.)
- Exclui automaticamente quem já foi escolhido
- Duração: 24 horas

#### Finalizar Votação

```
!finalizar
```
- Conta os votos
- Anuncia o vencedor
- **Altera o apelido de TODOS** no servidor
- Marca o vencedor como "já escolhido"
- Salva no histórico

#### Resetar Sistema

```
!resetar
```
⚠️ **CUIDADO:** Apaga tudo (participantes, histórico, votações)

```
!resetar_escolhidos
```
Apenas reseta a lista de "já escolhidos", permitindo nova rodada de votações.

### Comandos Públicos

#### Ver Histórico

```
!historico
```
Mostra os últimos 10 vencedores com datas e votos.

#### Ajuda

```
!ajuda_multiverso
```
Mostra todos os comandos disponíveis.

## 📖 Exemplo de Uso Completo

```bash
# 1. Admin adiciona participantes
!adicionar @João SuperJoão
!adicionar @Maria MariaDasGalaxias
!adicionar @Pedro PedrinhoDoMal
!adicionar @Ana AnaVortex

# 2. Admin verifica a lista
!lista

# 3. Admin inicia votação mensal
!multiverso

# 4. Membros votam reagindo aos emojis (automático)

# 5. Após 24h ou quando quiser, admin finaliza
!finalizar

# Resultado: TODOS do servidor agora se chamam "SuperJoão"!

# 6. Próximo mês, repete o processo
# João não vai aparecer na próxima votação
# Quando todos forem escolhidos, a lista reseta automaticamente
```

## 🎨 Exemplo Visual da Enquete

```
🌌 VOTAÇÃO DO MULTIVERSO 🌌

É hora de decidir quem será o próximo escolhido!
Vote reagindo com os números abaixo.

1️⃣ João
   Apelido: SuperJoão

2️⃣ Maria
   Apelido: MariaDasGalaxias

3️⃣ Pedro
   Apelido: PedrinhoDoMal

Como votar? Reaja com o emoji do candidato!
Duração: 24 horas
```

## 🔧 Configuração Avançada

### Alterar Duração da Votação

Edite a linha em `multiverso_bot.py`:

```python
embed.timestamp = datetime.utcnow() + timedelta(hours=24)  # Mude 24 para o que quiser
```

### Limitar Número de Candidatos

Por padrão, máximo de 10 candidatos por votação (limitação de emojis).

### Agendamento Automático

Para iniciar votações automaticamente todo mês, você pode usar cron jobs ou Windows Task Scheduler chamando um comando do bot.

## 📁 Estrutura de Arquivos

```
multiverso-bot/
├── multiverso_bot.py          # Código principal
├── multiverso_data.json       # Dados salvos (criado automaticamente)
├── .env                       # Token do bot
├── .env.example              # Template
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
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
      "votos": 15
    }
  ]
}
```

## ⚠️ Limitações e Avisos

1. **Hierarquia de Cargos**: O bot não pode alterar apelidos de membros com cargos superiores ao dele
2. **Donos do Servidor**: Normalmente não podem ter apelidos alterados
3. **Bots**: São automaticamente excluídos
4. **Máximo de Candidatos**: 10 por votação (limitação de emojis do Discord)

## 🐛 Solução de Problemas

### Bot não altera apelidos

- ✅ Verifique se o cargo do bot está **acima** dos outros
- ✅ Confirme que o bot tem permissão "Gerenciar Apelidos"
- ✅ Alguns membros (dono, cargos altos) podem ser imutáveis

### Votação não inicia

- ✅ Verifique se há participantes cadastrados
- ✅ Confirme que há candidatos disponíveis (não todos já escolhidos)

### Dados são perdidos

- ✅ Não delete o arquivo `multiverso_data.json`
- ✅ Faça backup regular deste arquivo

### Erro ao finalizar

- ✅ Certifique-se que há uma votação ativa
- ✅ Verifique se a mensagem da enquete ainda existe

## 🔒 Segurança

- Nunca compartilhe o arquivo `.env`
- Adicione ao `.gitignore`:

```gitignore
.env
bot_env/
multiverso_data.json
__pycache__/
*.pyc
```

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Abra uma issue ou pull request.

## 📄 Licença

MIT License - Use livremente!

## 👨‍💻 Autor

Desenvolvido com ❤️ para criar caos controlado no Discord

## 🎉 Ideias de Expansão

- ⏰ Agendamento automático mensal
- 📊 Gráficos de votação
- 🏆 Sistema de pontos/ranking
- 🎨 Customização de embeds
- 📢 Notificações automáticas
- 🔔 Lembretes de votação

---

⭐ Se curtiu a ideia, dê uma estrela no repositório!

**Transforme seu servidor em um multiverso! 🌌**
