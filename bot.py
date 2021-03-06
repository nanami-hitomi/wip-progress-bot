# Work in Progress Bot

# Import discord and necessary libraries for it
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import middle
import errors as e
import manga as mn
import chapter as ch

client = discord.Client()
bot = commands.Bot(command_prefix='p!') # bot prefix, for eg p!manga

# Remove default help command
bot.remove_command('help')


# <--- Console Ready --->
@bot.event
async def on_ready():
    print("Successfully Booted Up!")
    await bot.change_presence(activity=discord.Game(name="Progress-chan | p!help"))

# p!progress
@bot.command()
async def progress(ctx, *args):
    chapter = None
    if len(args)==0:
        await ctx.send("No arguments provided. Usage:")
        await ctx.send(middle.get_help("progress"))
        return
    elif len(args)==1: #If there is no chapter provided, get latest
        chapter = middle.get_chapter_or_latest(args[0])
    elif len(args)==2:
        chapter = middle.get_chapter_or_latest(args[0],args[1])
    else:
        await ctx.send("Too many arguments. Usage:")
        await ctx.send(middle.get_help("progress"))
        return

    if chapter is None:
        await ctx.send("Manga or chapter is invalid.")
        return

    embed = discord.Embed(
        title="Progress for chapter %i of %s\n%s" 
                % (chapter.chapter_number,
                    chapter.related_manga.full_name or chapter.related_manga.nickname,
                    "https://mangadex.org/title/%i" % chapter.related_manga_id),
        color=0xfc6c85)
    if not chapter.uploaded:
        fields_to_send = middle.get_progress(chapter)
        for name,value in fields_to_send.items():
            embed.add_field(name=name,value=value,inline=True)
    embed.add_field(name="Uploaded", value=chapter.uploaded, inline=False)
    await ctx.send(embed=embed)


# p!manga
@bot.command()
async def manga(ctx, *args):
    if len(args)==0:
        await ctx.send("No arguments. Usage:")
        await ctx.send(middle.get_help("manga"))
    elif len(args)==1:
        await ctx.send("Need to provide both ID and manga")
    elif len(args)==2:
        if args[0].isnumeric() == False or int(args[0]) < 1 or len(args[0]) > 6 or len(args[1]) > 30:
            await ctx.send("ID must be positive up to 6 numbers and up to 30 characters for manga")
            return
        try:
            manga = mn.Manga(int(args[0]), args[1])
            await ctx.send(middle.new_manga(manga))
        except ValueError:
            await ctx.send("ID needs to be a number. Usage:")
            await ctx.send(middle.get_help("manga"))
    else:
        await ctx.send("Too many arguments. Usage:")
        await ctx.send(middle.get_help("manga"))



#p!chapter
@bot.command()
async def chapter(ctx, *args):
    if len(args)==0:
        await ctx.send("No arguments provided. Usage:")
        await ctx.send(middle.get_help("chapter"))
    elif len(args)==1:
            await ctx.send("Need to provide both manga ID/nickname and chapter")
    elif len(args)==2:
        if len(args[0]) > 30 or args[1].isnumeric() == False or int(args[1]) < 1 or len(args[1]) > 4:
            await ctx.send("Chapter must be positive up to 4 numbers and up to 30 characters for ID/nickname")
            return
        manga = middle.get_manga(args[0])
        if manga is None:
            await ctx.send("Invalid manga")
            return
        else:
            chapter = middle.get_chapter_or_latest(args[0],args[1])

            if chapter is not None:
                await ctx.send("Chapter already exist")
                return
        await ctx.send(middle.new_chapter(manga,args[1]))
    else:
        await ctx.send("Too many arguments. Usage:")
        await ctx.send(middle.get_help("chapter"))


# p!edit 
@bot.command()
async def edit(ctx):
    await ctx.send("¯\_(ツ)_/¯")


# p!estimate
@bot.command()
async def estimate(ctx):
    await ctx.send("Sometime")

# p!help
@bot.command()
async def help(ctx, arg=""):
    await ctx.send(middle.get_help(arg))

# Example embed message
@bot.command()
async def userinfo1(ctx, user: discord.Member = None):
        """
        Gives you info on a user. If a user isn't passed then the shown info is yours.
        """
        if not user:
            user = ctx.author

        embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's What the end product should probably look like.", color=0x0072ff)
        embed.add_field(name="Name", value=user.name)
        embed.add_field(name="Discrim", value=user.discriminator, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Status", value=user.status, inline=False)
        embed.add_field(name="Highest Role", value=user.top_role, inline=False)
        embed.add_field(name="Joined At", value=user.joined_at, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Progress Bot for WiP")
        await ctx.send(embed=embed)

