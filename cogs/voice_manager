import discord
from discord.ext import commands
import database as db

class VoiceManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel == after.channel:
            return

        # 1. Logic tạo kênh
        if after.channel is not None:
            config = await db.get_server_config(member.guild.id)
            if config and after.channel.id == config[1]:
                await self.create_temp_channel(member, config[0])

        # 2. Logic xóa kênh
        if before.channel is not None:
            owner_id = await db.get_channel_owner(before.channel.id)
            if owner_id:
                if len(before.channel.members) == 0:
                    await before.channel.delete(reason="Temporary channel empty")
                    await db.remove_channel(before.channel.id)

    async def create_temp_channel(self, member: discord.Member, category_id: int):
        guild = member.guild
        category = guild.get_channel(category_id)
        
        if not category:
            return
            
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=True, view_channel=True),
            member: discord.PermissionOverwrite(manage_channels=True, manage_permissions=True, connect=True)
        }

        try:
            new_channel = await guild.create_voice_channel(
                name=f"Kênh của {member.display_name}",
                category=category,
                overwrites=overwrites
            )
            await db.register_channel(new_channel.id, member.id, guild.id)
            await member.move_to(new_channel)
        except Exception as e:
            print(f"Error creating channel: {e}")

async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
