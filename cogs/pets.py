from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
from tools.db import Database
from random import randint, choice
from asyncio import sleep as asyncsleep
import discord, json

ent = '\n'

class Pets:
    def __init__(self, bot):
        self.bot = bot
        self.petlist = ['cat', 'dog', 'tiger', 'fish', 'duck', 'penguin', 'horse', 'kiwi', 'camel', 'chicken', 'lion']
        self.rarepets = {
            'dictator': 3300,
            'dolphin': 6600,
            'unicorn': 14500,
            'fox': 19500,
            'shark': 22000,
            'octopus': 55000
        }
        self.countries = ['Russia', 'USA', 'Germany', 'Japan', 'Italy']
        self.database = Database('db/pets.db')
        self.inv = {}
        self.dbinv = Database('db/inv.db')
        self.data = {}
        self.itemview = {
            'snacks': '🍪',
            'meat': '🍖',
            'epicsnacks': '🥞',
            'basiccrate': '📦',
            'giveawaycrate': '🎀',
            'petpotion': '🍷'
        }

        self.petface = {
            'cat': '🐱',
            'dog': '🐶',
            'tiger': '🐯',
            'fish': '🐟',
            'duck': '🦆',
            'penguin': '🐧',
            'horse': '🐎',
            'dictator': '👮',
            'dolphin': '🐬',
            'kiwi': '🐦',
            'camel': '🐫',
            'chicken': '🐔',
            'unicorn': '🦄',
            'lion': '🦁',
            'shark': '🦈',
            'octopus': '🐙',
            'fox': '🦊'
        }

        self.attacks = {
            'cat': ['scratch', 'twinge', 'tail-slap'],
            'dog': ['bite', 'lunge', 'dog-kick'],
            'tiger': ['scratch', 'bite'],
            'fish': ['slap', 'jumpslap', 'fish-bite'],
            'duck': ['throw a feather', 'flew a wing', 'slap', 'duck-bite'],
            'penguin': ['penguin-jump-kick', 'mega-flip', 'peng-go'],
            'horse': ['kick', 'double-leg-kick'],
            'dictator': ['hand'],
            'dolphin': ['dolphin-bite'],
            'kiwi': ['fly-attack'],
            'camel': ['spit'],
            'chicken': ['Cluck'],
            'unicorn': ['uni-attack'],
            'lion': ['strong-bite'],
            'shark': ['strong-bite'],
            'octopus': ['arm-partition'],
            'fox': ['slap']
        }

        self.gamelist = {
            'throwing a ball': 1.05,
            'Running & Jumping': 1.07,
            'Treasure Hunting': 1.12
        }

        self.products = {
            'snacks': {
                'price': 65,
                'prize': [30, 60]
            },
            'meat': {
                'price': 125,
                'prize': [80, 160]
            },
            'epicsnacks': {
                'price': 550,
                'prize': [105, 405]
            },
            'basiccrate': {
                'price': 280
            },
            'petpotion': {
                'price': 1250
            }
        }

        self.potions = {
            'petpotion': self.func_petpotion
        }

        self.crates = {
            'basiccrate': {
                'items': ['snacks', 'meat', 'epicsnacks'],
                'recv': [1, 4]
            },
            'giveawaycrate': {
                'items': ['meat', 'epicsnacks'],
                'recv': [15, 65]
            }
        }

        bot.loop.create_task(self.setup())

    async def setup(self):
        await self.bot.wait_until_ready()
        with open('json/staff.json', 'r') as f:
            self.staff = json.loads(f.read())
        result = await self.database.fetch('SELECT * FROM list')
        for id, pet, petname, balance, xp, moves in result:
            if moves == None:
                moves = []
            else:
                moves = moves.split(',')
            self.data[id] = {'pet': pet, 'petname': petname, 'balance': balance, 'xp': xp, 'moves': moves}

        result = await self.dbinv.fetch('SELECT * FROM items')
        for id, snacks, meat, snacksEpic, basicCrate, giveawayCrate, petpotion in result:
            self.inv[id] = {'snacks': snacks, 'meat': meat, 'epicsnacks': snacksEpic, 'basiccrate': basicCrate, 'giveawaycrate': giveawayCrate, 'petpotion': petpotion}

        print('Setup Completed')

    def notexists(ctx):
        return not ctx.author.id in ctx.bot.get_cog('Pets').data

    def exists(ctx):
        return ctx.author.id in ctx.bot.get_cog('Pets').data

    def isStaff(ctx):
        return ctx.author.id in ctx.bot.get_cog('Pets').staff

    async def func_petpotion(self, ctx):
        self.inv[ctx.author.id]['petpotion'] -= 1
        await self.dbinv.query(f'UPDATE items SET petpotion="{self.inv[ctx.author.id]["petpotion"]}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, okay we gave ``petpotion`` to ``{self.data[ctx.author.id]["petname"]}``, the potion affects in 30 seconds')
        await asyncsleep(30)
        newpet = choice(self.petlist + list(self.rarepets.keys()))
        self.data[ctx.author.id]['pet'] = newpet
        await self.database.query(f'UPDATE list SET pet="{newpet}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, wow! your pet become a ``{newpet}``!')

    @commands.check(notexists)
    @commands.command()
    async def adopt(self, ctx, pet, *, petname):
        if pet in self.petlist:
            if len(petname) < 21 and len(petname) > 3 and not '@' in petname:
                self.data[ctx.author.id] = {'pet': pet, 'petname': petname, 'balance': 100, 'xp': 0, 'moves': []}
                self.inv[ctx.author.id] = {'snacks': 0, 'meat': 0, 'epicsnacks': 0, 'basiccrate': 0, 'giveawaycrate': 0, 'petpotion': 0}
                await self.database.query(f'INSERT INTO list (id, pet, petname, balance, xp, moves) VALUES ("{ctx.author.id}", "{pet}", "{petname}", "100", "0", NULL)')
                await self.dbinv.query(f'INSERT INTO items (id, snacks, meat, EpicSnacks, BasicCrate, giveawayCrate, petpotion) VALUES ("{ctx.author.id}", "0", "0", "0", "0", "0", "0")')
                await ctx.send(f'{ctx.author.mention}, You adopted a ``{pet}`` and called him ``{petname}``! You receive ``100 Tickets`` as a reward!')
            else:
                await ctx.send(f'{ctx.author.mention}, Pet name can contain from ``4`` to ``20`` chars! (Or you enter invaild char)')
        else:
            show = []
            for x in self.petlist:
                show.append(f'{self.petface[x]}{x}')
            await ctx.send(f'{ctx.author.mention}, You can choose animal from this list ``{", ".join(show)}``')

    @commands.check(exists)
    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if not member:
            embed = discord.Embed()
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='Balance', value=f'🎟 ``{self.data[ctx.author.id]["balance"]} Tickets``')
            embed.add_field(name='Pet', value=f'{self.petface[self.data[ctx.author.id]["pet"]]} ``{self.data[ctx.author.id]["pet"]} ({self.data[ctx.author.id]["petname"]}) | ({self.data[ctx.author.id]["xp"]} XP)``')
            await ctx.send(embed=embed)
        else:
            if member.id in self.data:
                embed = discord.Embed()
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                embed.add_field(name='Balance', value=f'🎟 ``{self.data[member.id]["balance"]} Tickets``')
                embed.add_field(name='Pet', value=f'{self.petface[self.data[member.id]["pet"]]} ``{self.data[member.id]["pet"]} ({self.data[member.id]["petname"]}) | ({self.data[member.id]["xp"]} XP)``')
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'{ctx.author.mention}, {member} Is not adopt a pet!')

    @commands.cooldown(1, 86400, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def daily(self, ctx):
        receive = randint(1024, 2048)
        self.data[ctx.author.id]['balance'] += receive
        await self.database.query(f'UPDATE list SET balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, You received ``{receive} Tickets`` as a daily reward')

    @commands.cooldown(1, 3600, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def hourly(self, ctx):
        receive = randint(102, 204)
        self.data[ctx.author.id]['balance'] += receive
        await self.database.query(f'UPDATE list SET balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, You received ``{receive} Tickets`` as a hourly reward')

    @commands.cooldown(1, 15, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def pet(self, ctx):
        receive = randint(3, 15)
        self.data[ctx.author.id]['xp'] += receive
        dt = self.data[ctx.author.id]['xp']
        await self.database.query(f'UPDATE list SET xp="{dt}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, Your {self.data[ctx.author.id]["pet"]} ({self.data[ctx.author.id]["petname"]}) received ``{receive} XP`` while you pet him!')

    @commands.check(exists)
    @commands.command()
    async def rename(self, ctx, *, name):
        if len(name) < 21 and len(name) > 3 and not '@' in name:
            if self.data[ctx.author.id]['balance'] >= 250:
                self.data[ctx.author.id]['balance'] -= 250
                self.data[ctx.author.id]['petname'] = name
                dt = self.data[ctx.author.id]['balance']
                await self.database.query(f'UPDATE list SET petname="{name}", balance="{dt}" WHERE id="{ctx.author.id}"')
                await ctx.send(f'{ctx.author.mention}, Your {self.data[ctx.author.id]["pet"]} name renamed to ``{name}`` for ``250 Tickets``')
            else:
                await ctx.send(f'{ctx.author.mention}, You need ``250 Tickets`` to rename your pet name')
        else:
            await ctx.send(f'{ctx.author.mention}, Pet name can contain from ``4`` to ``20`` chars! (Or you enter invaild char)')

    @commands.cooldown(1, 300, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def play(self, ctx):
        cg = choice(list(self.gamelist.keys()))
        receive = [int(randint(20, 50)*self.gamelist[cg]), int(randint(10, 20)*self.gamelist[cg])]
        self.data[ctx.author.id]['xp'] += receive[0]
        self.data[ctx.author.id]['balance'] += receive[1]
        await self.database.query(f'UPDATE list SET xp="{self.data[ctx.author.id]["xp"]}", balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, You played with your {self.data[ctx.author.id]["pet"]} ({self.data[ctx.author.id]["petname"]}) by ``{cg}`` and your {self.data[ctx.author.id]["pet"]} received ``{receive[0]}`` XP & ``{receive[1]}`` Tickets!')

    @commands.check(exists)
    @commands.command(aliases=['buy', 'store'])
    async def shop(self, ctx, *, product = None):
        if not product:
            embed = discord.Embed()
            embed.set_author(name='Store', icon_url=ctx.me.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            for x in list(self.products.keys()):
                embed.add_field(name=f'{self.itemview[x]} {x}', value=f'``{self.products[x]["price"]} Tickets``', inline=True)
            await ctx.send(embed=embed)
        else:
            try:
                int(product.split(' ')[-1])
                spx = int(product.split(' ')[-1])
                product = ' '.join(product.split(' ')[:-1])
            except:
                spx = 1
            if product in list(self.products.keys()):
                if self.data[ctx.author.id]['balance'] >= self.products[product]['price']*spx:
                    self.data[ctx.author.id]['balance'] -= self.products[product]['price']*spx
                    self.inv[ctx.author.id][product] += spx
                    await self.database.query(f'UPDATE list SET balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
                    await self.dbinv.query(f'UPDATE items SET {product}="{self.inv[ctx.author.id][product]}" WHERE id="{ctx.author.id}"')
                    await ctx.send(f'{ctx.author.mention}, You bought ``{product} x{spx}`` for ``{self.products[product]["price"]*spx} Tickets``')
                else:
                    await ctx.send(f'{ctx.author.mention}, You need ``{self.products[product]["price"]*spx} Tickets`` to buy ``{product} x{spx}``!')
            else:
                await ctx.send(f'{ctx.author.mention}, This product not found!')

    @commands.check(exists)
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, member: discord.Member = None):
        if not member:
            embed = discord.Embed()
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            for x in list(self.inv[ctx.author.id].keys()):
                embed.add_field(name=f'{self.itemview[x]} {x}', value=f'{self.inv[ctx.author.id][x]} {x}', inline=True)
            await ctx.send(embed=embed)
        else:
            if member.id in self.inv:
                embed = discord.Embed()
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
                for x in list(self.inv[ctx.author.id].keys()):
                    embed.add_field(name=f'{self.itemview[x]} {x}', value=f'{self.inv[member.id][x]} {x}', inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'{ctx.author.mention}, {member} Is not adopt a pet!')

    @commands.cooldown(1, 6, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def feed(self, ctx, product, count=1):
        if product in self.products and not product in self.potions and not product in self.crates:
            if count <= 50:
                if self.inv[ctx.author.id][product] > count-1:
                    self.inv[ctx.author.id][product] -= count
                    receive = 0
                    for x in range(count):
                        receive += randint(self.products[product]['prize'][0], self.products[product]['prize'][1])
                    self.data[ctx.author.id]['xp'] += receive
                    await self.database.query(f'UPDATE list SET xp="{self.data[ctx.author.id]["xp"]}" WHERE id="{ctx.author.id}"')
                    await self.dbinv.query(f'UPDATE items SET {product}="{self.inv[ctx.author.id][product]}" WHERE id="{ctx.author.id}"')
                    await ctx.send(f'{ctx.author.mention}, You feed your {self.data[ctx.author.id]["pet"]} ({self.data[ctx.author.id]["petname"]}) with ``{self.itemview[product]} {product} x{count}`` and received ``{receive} XP``')
                else:
                    await ctx.send(f'{ctx.author.mention}, You can\'t feed your {self.data[ctx.author.id]["pet"]} with ``{self.itemview[product]} {product}``!')
            else:
                await ctx.send(f'{ctx.author.mention}, You can feed your animal with max ``50`` items in one time!')
        else:
            await ctx.send(f'{ctx.author.mention}, This food wasn\'t found!')

    @commands.cooldown(1, 30, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def fight(self, ctx, member: discord.Member):
        if member.id != ctx.author.id:
            if member.id in self.data:
                main = f'{ctx.author} VS {member}'
                fip = 'Fight in progress...'
                msg = await ctx.send(f'{main}\n{fip}')
                moves = []
                chance = []
                chance.append(ctx.author)
                chance.append(member)
                if self.data[ctx.author.id]['xp'] > self.data[member.id]['xp']:
                    chance.append(ctx.author)
                    weaker = member
                else:
                    chance.append(member)
                    weaker = ctx.author
                while True:
                    turn = choice(chance)
                    if turn == ctx.author:
                        vs = member
                    else:
                        vs = ctx.author
                    await asyncsleep(1)
                    if randint(0, 1) or len(moves) > 5:
                        reward = randint(100, 250)
                        if weaker == turn:
                            reward *= 3
                        add = f'{turn.name}\'s {self.data[turn.id]["pet"]} beat {vs.name}\'s {self.data[vs.id]["pet"]} with a ``{choice(self.attacks[self.data[turn.id]["pet"]]+self.data[turn.id]["moves"])}`` and won ``{reward} Tickets``!'
                        moves.append(add)
                        self.data[turn.id]['balance'] += reward
                        await self.database.query(f'UPDATE list SET balance="{self.data[turn.id]["balance"]}" WHERE id="{turn.id}"')
                        await msg.edit(content=f'{main}\n{ent.join(moves)}')
                        break
                    else:
                        add = f'{turn.name}\'s {self.data[turn.id]["pet"]} tried to ``{choice(self.attacks[self.data[turn.id]["pet"]]+self.data[turn.id]["moves"])}`` {vs.name}\'s {self.data[vs.id]["pet"]}'
                        moves.append(add)
                        await msg.edit(content=f'{main}\n{ent.join(moves)}\n{fip}')
            else:
                await ctx.send(f'{ctx.author.mention}, {member} Is not adopt a pet!')
        else:
            await ctx.send(f'{ctx.author.mention}, you can\'t fight yourself')

    @commands.cooldown(1, 360, BucketType.user)
    @commands.check(exists)
    @commands.command(aliases=['adv'])
    async def adventure(self, ctx):
        if self.data[ctx.author.id]['xp'] > 499:
            await ctx.send(f'{ctx.author.mention}, your {self.data[ctx.author.id]["pet"]} has gone to adventure in {choice(self.countries)}! It will come back in 1 minute')
            await asyncsleep(60)
            if randint(0, 1):
                item = choice(list(self.products.keys()))
                itemt = randint(1, 4)
                found = f'``{item} x{itemt}``'
                self.inv[ctx.author.id][item] += itemt
                await self.dbinv.query(f'UPDATE items SET {item}="{self.inv[ctx.author.id][item]}" WHERE id="{ctx.author.id}"')
            else:
                found = '``Nothing``'
            xpt = randint(12, 108)
            tickett = randint(52, 252)
            got = f'``{xpt} XP``, ``{tickett} Tickets``'
            self.data[ctx.author.id]['xp'] += xpt
            self.data[ctx.author.id]['balance'] += tickett
            await self.database.query(f'UPDATE list SET xp="{self.data[ctx.author.id]["xp"]}", balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
            await ctx.send(f'{ctx.author.mention}, your {self.data[ctx.author.id]["pet"]} came back and found {found}. You also earned {got}!')
        else:
            await ctx.send(f'{ctx.author.mention}, you need minimum ``500 XP`` to send your pet to adventure!')

    @commands.cooldown(1, 15, BucketType.user)
    @commands.check(exists)
    @commands.command(name='crate')
    async def box(self, ctx, name, count=1):
        if count <= 100:
            name = name.lower()
            if name in self.crates:
                if self.inv[ctx.author.id][name] > count-1:
                    self.inv[ctx.author.id][name] -= count
                    await self.dbinv.query(f'UPDATE items SET {name}="{self.inv[ctx.author.id][name]}" WHERE id="{ctx.author.id}"')
                    loot = []
                    titems = {}
                    for x in range(count):
                        item = choice(self.crates[name]['items'])
                        itemt = randint(self.crates[name]['recv'][0], self.crates[name]['recv'][1])
                        try:
                            titems[item] += itemt
                        except:
                            titems[item] = itemt
                        self.inv[ctx.author.id][item] += itemt
                    for x in titems:
                        loot.append(f'``{x} x{titems[x]}``')
                        await self.dbinv.query(f'UPDATE items SET {x}="{self.inv[ctx.author.id][x]}" WHERE id="{ctx.author.id}"')
                    await ctx.send(f'{ctx.author.mention}, **loot** {", ".join(loot)}')
                else:
                    await ctx.send(f'{ctx.author.mention}, You can\'t open this crate!')
            else:
                await ctx.send(f'{ctx.author.mention}, This crate not found!')
        else:
            await ctx.send(f'{ctx.author.mention}, Maximum crates you can open in one time is ``100``!')

    @commands.check(exists)
    @commands.command()
    async def readopt(self, ctx, pet, petname):
        if self.data[ctx.author.id]['xp'] > 9999:
            if pet in self.petlist:
                if len(petname) < 21 and len(petname) > 3 and not '@' in petname:
                    before = self.data[ctx.author.id]['petname']
                    self.data[ctx.author.id]['xp'] = 0
                    self.data[ctx.author.id]['balance'] += 20000
                    self.data[ctx.author.id]['pet'] = pet
                    self.data[ctx.author.id]['petname'] = petname
                    await self.database.query(f'UPDATE list SET xp="{self.data[ctx.author.id]["xp"]}", balance="{self.data[ctx.author.id]["balance"]}", pet="{self.data[ctx.author.id]["pet"]}", petname="{self.data[ctx.author.id]["petname"]}" WHERE id="{ctx.author.id}"')
                    await ctx.send(f'{ctx.author.mention}, readopt completed!, you gave ``{before}`` to a good hands and you adopted a ``{pet}`` and called him ``{petname}``. Also you receive ``20000 Tickets``!')
                else:
                    await ctx.send(f'{ctx.author.mention}, Pet name can contain from ``4`` to ``20`` chars! (Or you enter invaild char)')
            else:
                show = []
                for x in self.petlist:
                    show.append(f'{self.petface[x]}{x}')
                await ctx.send(f'{ctx.author.mention}, You can choose animal from this list ``{", ".join(show)}``')
        else:
            await ctx.send(f'{ctx.author.mention}, your {self.data[ctx.author.id]["pet"]} don\'t reach to ``10000 XP``. You can\'t readopt')

    @commands.check(exists)
    @commands.command()
    async def delete(self, ctx):
        del self.data[ctx.author.id]
        del self.inv[ctx.author.id]
        await self.database.query(f'DELETE FROM list WHERE id="{ctx.author.id}"')
        await self.dbinv.query(f'DELETE FROM items WHERE id="{ctx.author.id}"')
        await ctx.send(f'{ctx.author.mention}, your pet deleted from the system ✅')

    @commands.check(isStaff)
    @commands.command(aliases=['give'])
    async def giveitem(self, ctx, item, member: discord.Member, count=1):
        if member.id in self.data:
            self.inv[member.id][item] += count
            await self.dbinv.query(f'UPDATE items SET {item}="{self.inv[member.id][item]}" WHERE id="{ctx.author.id}"')
            await ctx.send(f'{ctx.author.mention}, ``{member}({self.itemview[item]} {item})`` ``+{count}`` [👍]')
        else:
            await ctx.send(f'{ctx.author.id}, member not exists in database!')

    @commands.check(exists)
    @commands.command()
    async def addmove(self, ctx, *, name):
        if len(self.data[ctx.author.id]['moves']) < 4:
            if not name in self.data[ctx.author.id]['moves']:
                if self.data[ctx.author.id]['balance'] >= 550:
                    for x in name:
                        if x in ['@', ',', '\\', '#', '*', '^', '_', '`']:
                            await ctx.send(f'{ctx.author.mention}, You enter invalid char in your move name!')
                            return
                    if name and len(name) > 2 and len(name) < 16:
                        self.data[ctx.author.id]['balance'] -= 550
                        self.data[ctx.author.id]['moves'].append(name)
                        await self.database.query(f'UPDATE list SET moves="{",".join(self.data[ctx.author.id]["moves"])}", balance="{self.data[ctx.author.id]["balance"]}" WHERE id="{ctx.author.id}"')
                        await ctx.send(f'{ctx.author.mention}, move ``{name}`` added to your custom move list for ``550 Tickets`` Have fun!')
                    else:
                        await ctx.send(f'{ctx.author.mention}, move name can contain from ``3`` to ``15`` chars!')
                else:
                    await ctx.send(f'{ctx.author.mention}, you need ``550 Tickets`` to create custom move!')
            else:
                await ctx.send(f'{ctx.author.mention}, you already have a move named "{name}"')
        else:
            await ctx.send(f'{ctx.author.mention}, you reach the limt! ``4`` custom moves is it!')

    @commands.check(exists)
    @commands.command()
    async def delmove(self, ctx, *, name):
        if name in self.data[ctx.author.id]['moves']:
            self.data[ctx.author.id]['moves'].remove(name)
            await self.database.query(f'UPDATE list SET moves="{",".join(self.data[ctx.author.id]["moves"])}" WHERE id="{ctx.author.id}"')
            await ctx.send(f'{ctx.author.mention}, ``{name}`` move removed from your move-list by request')
        else:
            await ctx.send(f'{ctx.author.mention}, this move not found!')

    @commands.check(exists)
    @commands.command()
    async def moves(self, ctx, member: discord.Member = None):
        if not member:
            if len(self.data[ctx.author.id]["moves"]) > 0:
                await ctx.send(f'{ctx.author.mention}, your move-list is: ``{", ".join(self.attacks[self.data[ctx.author.id]["pet"]]) + ", " + ", ".join(self.data[ctx.author.id]["moves"])}``')
            else:
                await ctx.send(f'{ctx.author.mention}, your move-list is: ``{", ".join(self.attacks[self.data[ctx.author.id]["pet"]])}``')
        else:
            if len(self.data[member.id]["moves"]) > 0:
                await ctx.send(f'{ctx.author.mention}, {member}\'s move-list is: ``{", ".join(self.attacks[self.data[member.id]["pet"]]) + ", " + ", ".join(self.data[member.id]["moves"])}``')
            else:
                await ctx.send(f'{ctx.author.mention}, {member}\'s move-list is: ``{", ".join(self.attacks[self.data[member.id]["pet"]])}``')

    @commands.check(exists)
    @commands.command()
    async def blackmarket(self, ctx, item=None):
        if not item:
            embed = discord.Embed()
            embed.set_author(name='Blackmarket', icon_url=ctx.me.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            for x in self.rarepets:
                embed.add_field(name=f'{self.petface[x]}{x}', value=f'``{self.rarepets[x]} Tickets``')
            await ctx.send(embed=embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))
        else:
            if item in self.rarepets:
                if item != self.data[ctx.author.id]['pet']:
                    if self.data[ctx.author.id]['balance'] >= self.rarepets[item]:
                        self.data[ctx.author.id]['balance'] -= self.rarepets[item]
                        self.data[ctx.author.id]['pet'] = item
                        await self.database.query(f'UPDATE list SET balance="{self.data[ctx.author.id]["balance"]}", pet="{self.data[ctx.author.id]["pet"]}" WHERE id="{ctx.author.id}"')
                        await ctx.send(f'{ctx.author.mention}, you bought rare pet ``{item}`` secretly for ``{self.rarepets[item]} Tickets``')
                    else:
                        await ctx.send(f'{ctx.author.mention}, you need ``{self.rarepets[item]} Tickets`` to buy ``{item}``!')
                else:
                    await ctx.send(f'{ctx.author.mention}, you already have ``{item}`` as a pet!')
            else:
                await ctx.send(f'{ctx.author.mention}, this pet not found!')

    @commands.command()
    async def list(self, ctx):
        show = []
        for x in self.petlist:
            show.append(f'{self.petface[x]}{x}')
        await ctx.send(f'{ctx.author.mention}, ``{", ".join(show)}``')

    @commands.is_owner()
    @commands.command()
    async def addstaff(self, ctx, member: discord.Member):
        self.staff.append(member.id)
        with open('json/staff.json', 'w') as f:
            json.dump(self.staff, f)
        await ctx.send(f'{ctx.author.mention}, {member} is now staff!')

    @commands.is_owner()
    @commands.command()
    async def rmvstaff(self, ctx, member: discord.Member):
        if member.id in self.staff:
            self.staff.remove(member.id)
            with open('json/staff.json', 'w') as f:
                json.dump(self.staff, f)
            await ctx.send(f'{ctx.author.mention}, {member} removed from stuff!')
        else:
            await ctx.send(f'{ctx.author.mention}, {member} **not in stuff list!**')

    @commands.check(exists)
    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, type='tickets'):
        board = []
        basic = {'user': None, 'now': 0}
        list = []
        highest = 0
        if type == 'tickets':
            for x in self.data:
                if self.data[x]['balance'] > highest:
                    highest = self.data[x]['balance']
                    list.insert(0, {'user': x, 'bal': self.data[x]['balance']})
                else:
                    for y in range(len(list)):
                        if list[y]['bal'] < self.data[x]['balance']:
                            list.insert(y, {'user': x, 'bal': self.data[x]['balance']})
                            break
                        if y == len(list):
                            list.append({'user': x, 'bal': self.data[x]['balance']})
                            break
            embed = discord.Embed()
            embed.set_author(name='Global Leaderboard', icon_url=ctx.me.avatar_url)
            for x in range(5):
                user = self.bot.get_user(list[x]['user'])
                embed.add_field(name=f'{user} #{x+1}', value=f'``{list[x]["bal"]} Tickets``', inline=False)
            del list
            await ctx.send(embed=embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))
        elif type == 'xp':
            for x in self.data:
                if self.data[x]['xp'] > highest:
                    highest = self.data[x]['xp']
                    list.insert(0, {'user': x, 'bal': self.data[x]['xp']})
                else:
                    for y in range(len(list)):
                        if list[y]['bal'] < self.data[x]['xp']:
                            list.insert(y, {'user': x, 'bal': self.data[x]['xp']})
                            break
                        if y == len(list):
                            list.append({'user': x, 'bal': self.data[x]['xp']})
                            break
            embed = discord.Embed()
            embed.set_author(name='Global Leaderboard', icon_url=ctx.me.avatar_url)
            for x in range(5):
                user = self.bot.get_user(list[x]['user'])
                embed.add_field(name=f'{user} #{x+1}', value=f'``{list[x]["bal"]} XP``', inline=False)
            del list
            await ctx.send(embed=embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url))

    @commands.cooldown(1, 180, BucketType.user)
    @commands.check(exists)
    @commands.command()
    async def potion(self, ctx, potion):
        if potion in self.potions:
            if self.inv[ctx.author.id][potion] > 0:
                await self.potions[potion](ctx)
            else:
                await ctx.send(f'{ctx.author.mention}, you\'re can\'t use {potion}!')
        else:
            await ctx.send(f'{ctx.author.mention}, This potion wasn\'t found!')

def setup(bot):
    bot.add_cog(Pets(bot))
