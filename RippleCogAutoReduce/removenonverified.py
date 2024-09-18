import discord
from redbot.core import commands
from redbot.core.bot import Red

class RemoveNonVerified(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        # Role IDs for age brackets and their names
        self.age_bracket_roles = {
            995348375719395388: "13-17",  # 13-17
            995348996841283674: "18-20",  # 18-20
            995349196876021811: "21-24",  # 21-24
            995349271664656514: "25+"    # 25+
        }
        # Unverified role ID
        self.unverified_role_id = 1062206841716744262
        # Log channel ID (replace with your actual log channel ID)
        self.log_channel_id = 1062195647056466021  # Replace with your log channel ID

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Automatically removes the 'unverified' role when a user gets an age bracket role."""
        guild = after.guild
        unverified_role = guild.get_role(self.unverified_role_id)
        log_channel = guild.get_channel(self.log_channel_id)

        if unverified_role is None:
            return  # Unverified role doesn't exist, stop.

        # Check if the user had the unverified role before and now has an age bracket role
        if unverified_role in after.roles:
            new_roles = [role for role in after.roles if role.id in self.age_bracket_roles]
            if new_roles:
                age_bracket = self.age_bracket_roles[new_roles[0].id]
                try:
                    # Remove unverified role
                    await after.remove_roles(unverified_role)
                    await after.send("Thanks for verifying and keeping The Ashen Grave safe!")
                    
                    # Log the verification in the log channel
                    if log_channel is not None:
                        await log_channel.send(
                            f"**{after.display_name}** has verified and is under the **{age_bracket}** age bracket. "
                            f"The 'unverified' role has been removed."
                        )
                except discord.Forbidden:
                    await after.send("I do not have permission to remove your 'unverified' role.")
                except discord.HTTPException:
                    await after.send("There was an error while removing your 'unverified' role, please contact Ripple.")

    @commands.hybrid_command(name="removenonverified", with_app_command=True)
    @commands.guild_only()
    @commands.admin_or_permissions(administrator=True)
    async def remove_non_verified(self, ctx: commands.Context):
        """Manually removes the 'unverified' role from all users who have it."""
        guild = ctx.guild
        unverified_role = guild.get_role(self.unverified_role_id)

        if unverified_role is None:
            await ctx.send("The 'unverified' role does not exist in this server.")
            return

        count = 0
        members_with_role = [member for member in guild.members if unverified_role in member.roles]
        for member in members_with_role:
            try:
                await member.remove_roles(unverified_role)
                count += 1
            except discord.Forbidden:
                await ctx.send(f"Missing permissions to remove role from {member}.")
            except discord.HTTPException:
                await ctx.send(f"Failed to remove role from {member} due to an HTTP error.")

        await ctx.send(f"Removed 'unverified' role from {count} member(s).")

# Setup function for RedBot to load the cog
async def setup(bot: Red):
    await bot.add_cog(RemoveNonVerified(bot))
