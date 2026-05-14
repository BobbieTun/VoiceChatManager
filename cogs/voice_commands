import discord
from discord.ext import commands
from discord import app_commands
import database as db

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def verify_owner(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("Yêu cầu tham gia kênh thoại.", ephemeral=True)
            return None
        
        channel = interaction.user.voice.channel
        owner_id = await db.get_channel_owner(channel.id)
        
        if owner_id != interaction.user.id:
            await interaction.response.send_message("Từ chối truy cập. Yêu cầu quyền sở hữu kênh.", ephemeral=True)
            return None
            
        return channel

    @app_commands.command(name="setup", description="Thiết lập hệ thống VoiceMaster")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_system(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = await guild.create_category("V O I C E  C H A N N E L S")
        creator_channel = await guild.create_voice_channel("➕ Join to Create", category=category)
        
        await db.set_server_config(guild.id, category.id, creator_channel.id)
        await interaction.response.send_message("Hệ thống đã được thiết lập thành công.", ephemeral=True)

    @app_commands.command(name="lock", description="Khóa kênh thoại")
    async def lock(self, interaction: discord.Interaction):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        overwrites = channel.overwrites
        overwrites[interaction.guild.default_role].connect = False
        await channel.edit(overwrites=overwrites)
        await interaction.response.send_message("Kênh đã khóa.", ephemeral=True)

    @app_commands.command(name="unlock", description="Mở khóa kênh thoại")
    async def unlock(self, interaction: discord.Interaction):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        overwrites = channel.overwrites
        overwrites[interaction.guild.default_role].connect = True
        await channel.edit(overwrites=overwrites)
        await interaction.response.send_message("Kênh đã mở.", ephemeral=True)

    @app_commands.command(name="name", description="Đổi tên kênh thoại")
    async def name(self, interaction: discord.Interaction, new_name: str):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        await channel.edit(name=new_name)
        await interaction.response.send_message(f"Tên kênh thay đổi thành: {new_name}", ephemeral=True)

    @app_commands.command(name="limit", description="Giới hạn số lượng thành viên")
    async def limit(self, interaction: discord.Interaction, user_limit: int):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        if not (0 <= user_limit <= 99):
            return await interaction.response.send_message("Giới hạn từ 0 đến 99.", ephemeral=True)
            
        await channel.edit(user_limit=user_limit)
        await interaction.response.send_message(f"Giới hạn người dùng được đặt thành: {user_limit}", ephemeral=True)

    @app_commands.command(name="permit", description="Cấp quyền tham gia cho người dùng cụ thể")
    async def permit(self, interaction: discord.Interaction, user: discord.Member):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        overwrites = channel.overwrites
        overwrites[user] = discord.PermissionOverwrite(connect=True, view_channel=True)
        await channel.edit(overwrites=overwrites)
        await interaction.response.send_message(f"Đã cấp quyền cho {user.mention}.", ephemeral=True)

    @app_commands.command(name="claim", description="Chiếm quyền kênh nếu chủ cũ đã rời đi")
    async def claim(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("Yêu cầu tham gia kênh thoại.", ephemeral=True)
            
        channel = interaction.user.voice.channel
        owner_id = await db.get_channel_owner(channel.id)
        
        if not owner_id:
            return await interaction.response.send_message("Kênh này không thuộc hệ thống tự động.", ephemeral=True)
            
        if owner_id == interaction.user.id:
            return await interaction.response.send_message("Bạn đã là chủ kênh.", ephemeral=True)
            
        owner_member = channel.guild.get_member(owner_id)
        if owner_member in channel.members:
            return await interaction.response.send_message("Chủ kênh vẫn đang ở trong kênh.", ephemeral=True)
            
        await db.update_channel_owner(channel.id, interaction.user.id)
        await interaction.response.send_message("Đã chuyển quyền sở hữu kênh cho bạn.", ephemeral=True)

    @app_commands.command(name="transfer", description="Chuyển quyền sở hữu kênh cho người khác")
    async def transfer(self, interaction: discord.Interaction, user: discord.Member):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        if user not in channel.members:
            return await interaction.response.send_message("Người dùng mục tiêu phải ở trong kênh.", ephemeral=True)
            
        await db.update_channel_owner(channel.id, user.id)
        await interaction.response.send_message(f"Quyền sở hữu đã chuyển cho {user.mention}.", ephemeral=True)

    @app_commands.command(name="ghost", description="Bật/Tắt chế độ ẩn kênh")
    async def ghost(self, interaction: discord.Interaction, toggle: bool):
        channel = await self.verify_owner(interaction)
        if not channel: return
        
        overwrites = channel.overwrites
        overwrites[interaction.guild.default_role].view_channel = not toggle
        await channel.edit(overwrites=overwrites)
        state = "đã ẩn" if toggle else "hiển thị"
        await interaction.response.send_message(f"Kênh {state}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))
