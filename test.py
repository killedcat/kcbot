import json
import operator

with open('points.json', 'r') as f:
    points = {int(key): value for key, value in json.load(f).items()} # make sure all keys are ints in python dict
    print(points)


sorted_points = sorted(points.items(), key=operator.itemgetter(1))

print(sorted_points)
