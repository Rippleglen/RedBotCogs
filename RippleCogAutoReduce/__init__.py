from .removenonverified import RemoveNonVerified

async def setup(bot):
    await bot.add_cog(RemoveNonVerified(bot))
