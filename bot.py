import os

import discord
import json
import operator

pointsfile = 'points.json'

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

with open('token', 'r') as f:
    TOKEN = f.read()

def load_points():
    if not os.path.exists(pointsfile):
        write_points({})
        return {}

    with open(pointsfile, 'r') as f:
        points = {int(key): value for key, value in json.load(f).items()} # make sure all keys are ints in python dict
        print(points)
        return points

def write_points(points):
    with open(pointsfile, 'w+') as f:
        f.write(json.dumps(points))
        return points

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('something here'))
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        command = message.content[1:].split(' ')[0]

        points = load_points()

        if command == 'assign':
            if len(message.content.split(' ')) < 2:
                await message.channel.send('no.')
                return

            due = message.content.split(' ')[1] # daily or weekly
            if due == 'daily':
                await message.channel.send('daily assignment created')
                return
            elif due == 'weekly':
                await message.channel.send('weekly asignment created')
                return
            else:
                await message.channel.send('error: argument must be daily or weekly')
            # start a timer based on that and in a different function --
               # at the end of the timer, check who has completed the assignment
               # check who is on a streak
               # set streak of those who didn't complete the assignment to 0
            return

        if command == 'daily' or command == 'weekly':
            if len(message.content.split(' ')) < 2:
                await message.channel.send('no.')
                return

            # !daily @Snow
            authorroles = [role.name for role in message.author.roles]
            if 'grader' in authorroles:
                try:
                    awardeeId = int(message.content.split(' ')[1][3:-1])
                    awardeeMember = discord.utils.find(lambda m: m.id == awardeeId, message.channel.guild.members)
                    assert awardeeMember.id == awardeeId
                except ValueError:
                    await message.channel.send(f'that doesn\'t seem to be a valid id, try pinging instead of using a username?')
                    return

                if awardeeMember.id in points:
                    points[awardeeMember.id] += 1 if command == 'daily' else 3
                else:
                    points[awardeeMember.id] = 1 if command == 'daily' else 3

                await message.channel.send(f'good job :^) {awardeeMember.name} now has {points[awardeeId]} points!!')
                write_points(points)
            else:
                await message.channel.send('you need the grader role to do that.')

        if command == 'cb':
            if message.author.id in points:
                await message.channel.send(f'you\'ve got {points[message.author.id]} points')
            else:
                await message.channel.send(f'you, 0, have NO points (loser)')


if __name__ == '__main__':
    client.run(TOKEN)
