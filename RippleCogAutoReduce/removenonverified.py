import discord
from redbot.core import commands
from redbot.core.bot import Red

class RemoveNonVerified(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command(name="removenonverified")
    @commands.guild_only()
    @commands.admin_or_permissions(administrator=True)
    async def remove_non_verified(self, ctx):
        """Removes the 'unverified' role from all users who have it."""
        unverified_role_id = 1062206841716744262
        guild = ctx.guild
        role = guild.get_role(unverified_role_id)

        if role is None:
            await ctx.send("The 'unverified' role does not exist in this server.")
            return

        count = 0
        # Iterate through all members who have the 'unverified' role
        members_with_role = [member for member in guild.members if role in member.roles]
        for member in members_with_role:
            try:
                await member.remove_roles(role)
                count += 1
            except discord.Forbidden:
                await ctx.send(f"Missing permissions to remove role from {member}.")
            except discord.HTTPException:
                await ctx.send(f"Failed to remove role from {member} due to an HTTP error.")

        await ctx.send(f"Removed 'unverified' role from {count} member(s).")
