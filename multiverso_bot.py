import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Sincroniza os slash commands quando o bot inicia
@bot.event
async def setup_hook():
    """Sincroniza os slash commands com o Discord"""
    print("🔄 Sincronizando slash commands...")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash commands sincronizados!")
    except Exception as e:
        print(f"❌ Erro ao sincronizar: {e}")

# Arquivo para salvar dados
DATA_FILE = 'multiverso_data.json'

# Estrutura de dados
def load_data():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'participantes': {},
        'ja_escolhidos': [],
        'atual_escolhido': None,
        'historico': [],
        'poll_message_id': None,
        'poll_channel_id': None
    }

def save_data(data):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@bot.event
async def on_ready():
    print(f'🎭 {bot.user} está online!')
    print(f'ID do Bot: {bot.user.id}')
    print(f'🌌 Sistema Multiverso ativado!')
    
    # Inicia as tarefas agendadas
    if not verificar_votacao.is_running():
        verificar_votacao.start()
    
    if not iniciar_votacao_automatica.is_running():
        iniciar_votacao_automatica.start()
    
    print(f'⏰ Agendador automático ativado!')
    print(f'📅 Próxima votação: Todo dia 1 de cada mês às 00:00')

# Comando de emergência para sincronizar (usar apenas uma vez)
@bot.command()
@commands.is_owner()
async def sync(ctx):
    """Sincroniza os slash commands manualmente"""
    print("🔄 Sincronizando comandos...")
    await bot.tree.sync()
    await ctx.send("✅ Comandos sincronizados! Agora digite `/` para ver os comandos.")
    print("✅ Comandos sincronizados com sucesso!")

# ============================================
# SLASH COMMANDS
# ============================================

@bot.tree.command(name="adicionar", description="Adiciona um participante ao Multiverso")
@app_commands.describe(
    membro="O membro que você quer adicionar",
    apelido="O apelido que será usado quando ele ganhar"
)
@app_commands.checks.has_permissions(administrator=True)
async def adicionar(interaction: discord.Interaction, membro: discord.Member, apelido: str):
    """Adiciona um participante ao Multiverso"""
    data = load_data()
    
    data['participantes'][str(membro.id)] = {
        'nome': membro.display_name,
        'apelido': apelido,
        'user_id': membro.id
    }
    
    save_data(data)
    
    embed = discord.Embed(
        title="✅ Participante Adicionado ao Multiverso!",
        description=f"**{membro.mention}** foi adicionado com o apelido:\n`{apelido}`",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="remover", description="Remove um participante do Multiverso")
@app_commands.describe(membro="O membro que você quer remover")
@app_commands.checks.has_permissions(administrator=True)
async def remover(interaction: discord.Interaction, membro: discord.Member):
    """Remove um participante do Multiverso"""
    data = load_data()
    
    user_id = str(membro.id)
    
    if user_id not in data['participantes']:
        await interaction.response.send_message(f"❌ {membro.mention} não está na lista do Multiverso!", ephemeral=True)
        return
    
    apelido = data['participantes'][user_id]['apelido']
    del data['participantes'][user_id]
    
    if user_id in data['ja_escolhidos']:
        data['ja_escolhidos'].remove(user_id)
    
    save_data(data)
    
    embed = discord.Embed(
        title="🗑️ Participante Removido",
        description=f"**{membro.mention}** (`{apelido}`) foi removido do Multiverso.",
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="lista", description="Mostra todos os participantes do Multiverso")
async def lista(interaction: discord.Interaction):
    """Mostra todos os participantes do Multiverso"""
    data = load_data()
    
    if not data['participantes']:
        await interaction.response.send_message("📝 A lista do Multiverso está vazia!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🌌 Lista do Multiverso",
        description="Participantes cadastrados:",
        color=0x9B59B6
    )
    
    for user_id, info in data['participantes'].items():
        ja_escolhido = "✅" if user_id in data['ja_escolhidos'] else "⏳"
        atual = "👑" if user_id == data['atual_escolhido'] else ""
        
        embed.add_field(
            name=f"",
            value=f"{ja_escolhido} Apelido: `{info['apelido']}` {atual}",
            inline=False
        )
    
    embed.add_field(
        name="",
        value="✅ = Já foi escolhido | ⏳ = Aguardando | 👑 = Atual campeão",
        inline=False
    )
    
    total = len(data['participantes'])
    escolhidos = len(data['ja_escolhidos'])
    restantes = total - escolhidos
    
    embed.set_footer(text=f"Total: {total} | Escolhidos: {escolhidos} | Restantes: {restantes}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="multiverso", description="Inicia a votação do Multiverso")
@app_commands.checks.has_permissions(administrator=True)
async def multiverso(interaction: discord.Interaction):
    """Inicia a votação do Multiverso"""
    data = load_data()
    
    if not data['participantes']:
        await interaction.response.send_message("❌ Não há participantes cadastrados! Use `/adicionar` primeiro.", ephemeral=True)
        return
    
    if len(data['ja_escolhidos']) >= len(data['participantes']):
        await interaction.response.send_message("🔄 Todos já foram escolhidos! Resetando a lista...")
        data['ja_escolhidos'] = []
        save_data(data)
    
    candidatos = {
        user_id: info 
        for user_id, info in data['participantes'].items() 
        if user_id not in data['ja_escolhidos']
    }
    
    if not candidatos:
        await interaction.response.send_message("❌ Nenhum candidato disponível!", ephemeral=True)
        return
    
    candidatos_lista = list(candidatos.items())[:10]
    
    pergunta = "🌌 VOTAÇÃO DO MULTIVERSO - Quem será o próximo escolhido?"
    
    poll = discord.Poll(
        question=discord.PollMedia(text=pergunta),
        duration=timedelta(hours=24)
    )
    
    for user_id, info in candidatos_lista:
        opcao_texto = f"{info['apelido']}"
        poll.add_answer(text=opcao_texto[:55])
    
    embed = discord.Embed(
        title="🎉 Votação Mensal Iniciada!",
        description=(
            "O vencedor terá seu apelido aplicado a **TODOS** do servidor!\n\n"
            "⏰ **Duração:** 24 horas\n"
            "🗳️ **Vote na enquete abaixo!**\n"
        ),
        color=0xFF00FF
    )

    await interaction.response.send_message(embed=embed)
    
    message = await interaction.followup.send(poll=poll)
    
    data['poll_message_id'] = message.id
    data['poll_channel_id'] = interaction.channel_id
    data['poll_candidatos'] = candidatos_lista
    data['poll_inicio'] = datetime.utcnow().isoformat()
    data['poll_fim_programado'] = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    
    save_data(data)
    
    await interaction.followup.send(f"✅ Votação iniciada! Termina em 24 horas. Use `/finalizar` para encerrar antes se necessário.", ephemeral=True)

@bot.tree.command(name="finalizar", description="Finaliza a votação do Multiverso e aplica o resultado")
@app_commands.checks.has_permissions(administrator=True)
async def finalizar(interaction: discord.Interaction):
    """Finaliza a votação do Multiverso e aplica o apelido vencedor"""
    data = load_data()
    
    if not data.get('poll_message_id'):
        await interaction.response.send_message("❌ Não há votação ativa!", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    channel = bot.get_channel(data['poll_channel_id'])
    try:
        message = await channel.fetch_message(data['poll_message_id'])
    except:
        await interaction.followup.send("❌ Não consegui encontrar a mensagem da votação!")
        return
    
    if not message.poll:
        await interaction.followup.send("❌ Esta mensagem não tem uma enquete!")
        return
    
    poll = message.poll
    
    if not poll.is_finalised():
        await message.poll.end()
        await asyncio.sleep(2)
        message = await channel.fetch_message(data['poll_message_id'])
        poll = message.poll
    
    votos_por_opcao = {}
    for answer in poll.answers:
        votos_por_opcao[answer.id] = answer.vote_count
    
    if not votos_por_opcao or all(v == 0 for v in votos_por_opcao.values()):
        await interaction.followup.send("❌ Nenhum voto foi registrado!")
        return
    
    id_vencedor = max(votos_por_opcao, key=votos_por_opcao.get)
    total_votos = votos_por_opcao[id_vencedor]
    
    candidatos_lista = data['poll_candidatos']
    user_id_vencedor, info_vencedor = candidatos_lista[id_vencedor - 1]
    
    embed = discord.Embed(
        title="🎉 TEMOS UM VENCEDOR! 🎉",
        description=(
            f"\n"
            f"🏆 **Apelido vencedor:** `{info_vencedor['apelido']}`\n"
            f"📊 **Votos recebidos:** {total_votos}\n\n"
            f"Alterando apelidos de todos do servidor..."
        ),
        color=discord.Color.gold()
    )
    
    await interaction.followup.send(embed=embed)
    
    guild = interaction.guild
    sucessos = 0
    falhas = 0
    
    status_msg = await interaction.followup.send("🔄 Alterando apelidos...")
    
    for member in guild.members:
        if member.bot:
            continue
        
        try:
            await member.edit(nick=info_vencedor['apelido'])
            sucessos += 1
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            falhas += 1
        except Exception as e:
            print(f"Erro ao alterar apelido de {member.name}: {e}")
            falhas += 1
    
    data['ja_escolhidos'].append(user_id_vencedor)
    data['atual_escolhido'] = user_id_vencedor
    data['historico'].append({
        'user_id': user_id_vencedor,
        'nome': info_vencedor['nome'],
        'apelido': info_vencedor['apelido'],
        'data': datetime.utcnow().isoformat(),
        'votos': total_votos
    })
    
    data['poll_message_id'] = None
    data['poll_channel_id'] = None
    data['poll_candidatos'] = []
    
    save_data(data)
    
    embed_final = discord.Embed(
        title="✅ Multiverso Ativado!",
        description=(
            f"**{info_vencedor['apelido']}** agora reina sobre o multiverso!\n\n"
            f"👑 Todos agora são: `{info_vencedor['apelido']}`\n\n"
            f"**Estatísticas:**\n"
            f"✅ Apelidos alterados: {sucessos}\n"
            f"❌ Falhas: {falhas}"
        ),
        color=discord.Color.purple()
    )
    
    await status_msg.edit(content="", embed=embed_final)

@bot.tree.command(name="resetar", description="⚠️ Reseta todo o sistema do Multiverso")
@app_commands.checks.has_permissions(administrator=True)
async def resetar(interaction: discord.Interaction):
    """Reseta todo o sistema do Multiverso"""
    embed = discord.Embed(
        title="⚠️ Confirmar Reset",
        description=(
            "Você tem certeza que deseja resetar TODO o sistema?\n\n"
            "Isso irá:\n"
            "❌ Limpar a lista de participantes\n"
            "❌ Resetar histórico de escolhidos\n"
            "❌ Cancelar votação ativa (se houver)\n\n"
            "**Esta ação não pode ser desfeita!**\n\n"
            "Use os botões abaixo para confirmar ou cancelar."
        ),
        color=discord.Color.orange()
    )
    
    view = discord.ui.View(timeout=30)
    
    async def confirm_callback(button_interaction: discord.Interaction):
        if button_interaction.user.id != interaction.user.id:
            await button_interaction.response.send_message("❌ Apenas quem iniciou pode confirmar!", ephemeral=True)
            return
        
        data = {
            'participantes': {},
            'ja_escolhidos': [],
            'atual_escolhido': None,
            'historico': [],
            'poll_message_id': None,
            'poll_channel_id': None
        }
        save_data(data)
        
        await button_interaction.response.edit_message(content="✅ Sistema resetado com sucesso!", embed=None, view=None)
    
    async def cancel_callback(button_interaction: discord.Interaction):
        if button_interaction.user.id != interaction.user.id:
            await button_interaction.response.send_message("❌ Apenas quem iniciou pode cancelar!", ephemeral=True)
            return
        
        await button_interaction.response.edit_message(content="❌ Reset cancelado.", embed=None, view=None)
    
    confirm_button = discord.ui.Button(label="✅ Confirmar", style=discord.ButtonStyle.danger)
    confirm_button.callback = confirm_callback
    
    cancel_button = discord.ui.Button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
    cancel_button.callback = cancel_callback
    
    view.add_item(confirm_button)
    view.add_item(cancel_button)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="resetar_escolhidos", description="Reseta apenas a lista de já escolhidos")
@app_commands.checks.has_permissions(administrator=True)
async def resetar_escolhidos(interaction: discord.Interaction):
    """Reseta apenas a lista de já escolhidos"""
    data = load_data()
    data['ja_escolhidos'] = []
    data['atual_escolhido'] = None
    save_data(data)
    
    await interaction.response.send_message("✅ Lista de escolhidos resetada! Todos podem participar novamente.")

@bot.tree.command(name="historico", description="Mostra o histórico de vencedores do Multiverso")
async def historico(interaction: discord.Interaction):
    """Mostra o histórico de vencedores do Multiverso"""
    data = load_data()
    
    if not data['historico']:
        await interaction.response.send_message("📜 Ainda não há histórico de vencedores!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📜 Histórico do Multiverso",
        description="Vencedores anteriores:",
        color=0xE67E22
    )
    
    for i, registro in enumerate(reversed(data['historico'][-10:]), 1):
        data_formatada = datetime.fromisoformat(registro['data']).strftime('%d/%m/%Y')
        
        embed.add_field(
            name=f"#{len(data['historico']) - i + 1} - {registro['apelido']}",
            value=(
                f"Apelido: `{registro['apelido']}`\n"
                f"Data: {data_formatada}\n"
                f"Votos: {registro.get('votos', 'N/A')}"
            ),
            inline=False
        )
    
    embed.set_footer(text=f"Total de eleições: {len(data['historico'])}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Mostra o guia completo do Multiverso Bot")
async def help_slash(interaction: discord.Interaction):
    """Menu de ajuda completo do Multiverso Bot"""
    embed = discord.Embed(
        title="🌌 Multiverso Bot - Guia Completo",
        description=(
            "Sistema automático de votação onde o vencedor tem seu apelido "
            "aplicado a **TODOS** os membros do servidor!\n\n"
            "**Como funciona?**\n"
            "1️⃣ Admin cadastra participantes e apelidos\n"
            "2️⃣ Bot cria votação (manual ou automática)\n"
            "3️⃣ Todos votam na enquete\n"
            "4️⃣ Vencedor tem seu apelido aplicado a TODOS\n"
            "5️⃣ Próxima votação exclui quem já ganhou\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0x9B59B6
    )
    
    embed.add_field(
        name="📝 GERENCIAMENTO (Apenas Admin)",
        value=(
            "`/adicionar` - Adiciona um participante\n"
            "`/remover` - Remove um participante\n"
            "`/lista` - Lista todos os participantes\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🗳️ VOTAÇÃO (Apenas Admin)",
        value=(
            "`/multiverso` - Inicia votação manual\n"
            "`/finalizar` - Encerra e aplica resultado\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 CONSULTA (Todos podem usar)",
        value=(
            "`/historico` - Vencedores anteriores\n"
            "`/help` - Este menu de ajuda\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 MANUTENÇÃO (Apenas Admin)",
        value=(
            "`/resetar` - ⚠️ Reseta TODO o sistema\n"
            "`/resetar_escolhidos` - Reseta lista de escolhidos\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⏰ SISTEMA AUTOMÁTICO",
        value=(
            "✅ Votação inicia todo dia 1 às 00:00 UTC\n"
            "✅ Duração: 24 horas\n"
            "✅ Encerramento automático\n"
            "✅ Rodízio inteligente (todos participam!)\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 DICAS IMPORTANTES",
        value=(
            "• Cargo do bot deve estar **acima** dos outros\n"
            "• Bot precisa de permissão **Gerenciar Apelidos**\n"
            "• Máximo de 10 candidatos por votação\n"
            "• Configure `CANAL_VOTACAO_ID` no .env para automação\n"
        ),
        inline=False
    )
    
    embed.set_footer(text="Multiverso Bot • Use / para ver todos os comandos!")
    embed.set_thumbnail(url="https://i.imgur.com/AfFp7pu.png")
    
    await interaction.response.send_message(embed=embed)

# ============================================
# SISTEMA DE AGENDAMENTO AUTOMÁTICO
# ============================================

@tasks.loop(hours=1)
async def iniciar_votacao_automatica():
    """Verifica a cada hora se é dia 1 do mês às 00:00"""
    now = datetime.utcnow()
    
    if now.day == 1 and now.hour == 0:
        print(f"📅 Dia 1 detectado! Iniciando votação automática...")
        
        data = load_data()
        
        if data.get('poll_message_id'):
            print(f"⚠️ Já existe uma votação ativa. Pulando...")
            return
        
        canal_id = os.getenv('CANAL_VOTACAO_ID')
        
        if not canal_id:
            print(f"❌ CANAL_VOTACAO_ID não configurado no .env!")
            return
        
        canal = bot.get_channel(int(canal_id))
        
        if not canal:
            print(f"❌ Canal de votação não encontrado!")
            return
        
        if not data['participantes']:
            print(f"⚠️ Sem participantes cadastrados. Votação cancelada.")
            return
        
        if len(data['ja_escolhidos']) >= len(data['participantes']):
            print(f"🔄 Todos já foram escolhidos! Resetando lista...")
            data['ja_escolhidos'] = []
            save_data(data)
        
        candidatos = {
            user_id: info 
            for user_id, info in data['participantes'].items() 
            if user_id not in data['ja_escolhidos']
        }
        
        if not candidatos:
            print(f"❌ Nenhum candidato disponível!")
            return
        
        candidatos_lista = list(candidatos.items())[:10]
        
        pergunta = "🌌 VOTAÇÃO MENSAL DO MULTIVERSO - Quem será o próximo escolhido?"
        
        poll = discord.Poll(
            question=discord.PollMedia(text=pergunta),
            duration=timedelta(hours=24)
        )
        
        for user_id, info in candidatos_lista:
            opcao_texto = f"{info['apelido']}"
            poll.add_answer(text=opcao_texto[:55])
        
        embed = discord.Embed(
            title="🎉 VOTAÇÃO MENSAL AUTOMÁTICA INICIADA!",
            description=(
                "**🗓️ É DIA 1! Hora da votação mensal!**\n\n"
                "O vencedor terá seu apelido aplicado a **TODOS** do servidor!\n\n"
                "⏰ **Duração:** 24 horas (encerramento automático)\n"
                "🗳️ **Vote na enquete abaixo!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=0xFF00FF
        )
        
        for i, (user_id, info) in enumerate(candidatos_lista, 1):
            embed.add_field(
                name=f"",
                value=f"{i}. Apelido: **{info['apelido']}**",
                inline=False
            )
        
        fim_votacao = datetime.utcnow() + timedelta(hours=24)
        embed.set_footer(text=f"Sistema automático • Encerra em 24h")
        embed.timestamp = fim_votacao
        
        try:
            await canal.send(embed=embed)
            message = await canal.send(poll=poll)
            
            data['poll_message_id'] = message.id
            data['poll_channel_id'] = canal.id
            data['poll_candidatos'] = candidatos_lista
            data['poll_inicio'] = datetime.utcnow().isoformat()
            data['poll_fim_programado'] = fim_votacao.isoformat()
            
            save_data(data)
            
            print(f"✅ Votação automática iniciada com sucesso!")
            print(f"📊 Candidatos: {len(candidatos_lista)}")
            print(f"⏰ Encerramento programado: {fim_votacao}")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar votação automática: {e}")

@tasks.loop(minutes=5)
async def verificar_votacao():
    """Verifica a cada 5 minutos se há votação que precisa ser encerrada"""
    data = load_data()
    
    if not data.get('poll_message_id'):
        return
    
    if not data.get('poll_fim_programado'):
        return
    
    fim_programado = datetime.fromisoformat(data['poll_fim_programado'])
    agora = datetime.utcnow()
    
    if agora < fim_programado:
        return
    
    print(f"⏰ Horário de encerramento atingido! Finalizando votação...")
    
    canal = bot.get_channel(data['poll_channel_id'])
    
    if not canal:
        print(f"❌ Canal não encontrado!")
        return
    
    try:
        message = await canal.fetch_message(data['poll_message_id'])
    except:
        print(f"❌ Mensagem não encontrada!")
        data['poll_message_id'] = None
        save_data(data)
        return
    
    if not message.poll:
        print(f"❌ Mensagem não tem enquete!")
        data['poll_message_id'] = None
        save_data(data)
        return
    
    poll = message.poll
    
    if not poll.is_finalised():
        try:
            await message.poll.end()
            await asyncio.sleep(2)
            message = await canal.fetch_message(data['poll_message_id'])
            poll = message.poll
        except Exception as e:
            print(f"❌ Erro ao finalizar enquete: {e}")
            return
    
    votos_por_opcao = {}
    for answer in poll.answers:
        votos_por_opcao[answer.id] = answer.vote_count
    
    if not votos_por_opcao or all(v == 0 for v in votos_por_opcao.values()):
        print(f"❌ Nenhum voto registrado!")
        await canal.send("😢 A votação automática não teve nenhum voto. Cancelando...")
        data['poll_message_id'] = None
        data['poll_fim_programado'] = None
        save_data(data)
        return
    
    id_vencedor = max(votos_por_opcao, key=votos_por_opcao.get)
    total_votos = votos_por_opcao[id_vencedor]
    
    candidatos_lista = data['poll_candidatos']
    user_id_vencedor, info_vencedor = candidatos_lista[id_vencedor - 1]
    
    embed = discord.Embed(
        title="🎉 VOTAÇÃO ENCERRADA AUTOMATICAMENTE! 🎉",
        description=(
            f"\n"
            f"🏆 **Apelido vencedor:** `{info_vencedor['apelido']}`\n"
            f"📊 **Votos recebidos:** {total_votos}\n\n"
            f"Alterando apelidos de todos do servidor..."
        ),
        color=discord.Color.gold()
    )
    
    await canal.send(embed=embed)
    
    guild = canal.guild
    sucessos = 0
    falhas = 0
    
    status_msg = await canal.send("🔄 Alterando apelidos...")
    
    for member in guild.members:
        if member.bot:
            continue
        
        try:
            await member.edit(nick=info_vencedor['apelido'])
            sucessos += 1
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            falhas += 1
        except Exception as e:
            print(f"Erro ao alterar apelido de {member.name}: {e}")
            falhas += 1
    
    data['ja_escolhidos'].append(user_id_vencedor)
    data['atual_escolhido'] = user_id_vencedor
    data['historico'].append({
        'user_id': user_id_vencedor,
        'nome': info_vencedor['nome'],
        'apelido': info_vencedor['apelido'],
        'data': datetime.utcnow().isoformat(),
        'votos': total_votos,
        'automatico': True
    })
    
    data['poll_message_id'] = None
    data['poll_channel_id'] = None
    data['poll_candidatos'] = []
    data['poll_fim_programado'] = None
    
    save_data(data)
    
    embed_final = discord.Embed(
        title="✅ Multiverso Ativado Automaticamente!",
        description=(
            f"**{info_vencedor['apelido']}** agora reina sobre o multiverso!\n\n"
            f"👑 Todos agora são: `{info_vencedor['apelido']}`\n\n"
            f"**Estatísticas:**\n"
            f"✅ Apelidos alterados: {sucessos}\n"
            f"❌ Falhas: {falhas}\n\n"
            f"🗓️ Próxima votação: Dia 1 do próximo mês"
        ),
        color=discord.Color.purple()
    )
    
    await status_msg.edit(content="", embed=embed_final)
    
    print(f"✅ Votação encerrada automaticamente!")
    print(f"👑 Vencedor: {info_vencedor['apelido']}")
    print(f"📊 Sucessos: {sucessos} | Falhas: {falhas}")

# Inicia o bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("❌ ERRO: Token não encontrado!")
        print("💡 Configure DISCORD_TOKEN no arquivo .env")
        exit(1)
    
    bot.run(TOKEN)