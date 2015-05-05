#!/usr/bin/python
import argparse
import nflgame

parser = argparse.ArgumentParser(description='Find player stats for season')
parser.add_argument('--player', '-p', help='name of player', required=True)
parser.add_argument('--year', '-y', help='year of season', required=True)
args = parser.parse_args()

print '%s: %s' % (args.player, args.year)

person = '%s.%s' % (args.player.split()[0][0], args.player.split()[1])


games = nflgame.games(int(args.year))
players = nflgame.combine(games)
player = players.name(person)

print player.formatted_stats()
quit()
for i in (vars(player)):
	if i == '_stats':
#		print "stats!"
		for j in vars(player)[i]:
			print '%s : %s' % (j, vars(player)[i][j])
	else:
		print '%s : %s' % (i,vars(player)[i])
#	print i + ':' + vars(player)[i]

