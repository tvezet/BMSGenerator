# BMSGenerator
Tool for generating random map sequences for Brawl Stars. Available maps for the different game types described in Type List Syntax will be taken from https://www.starlist.pro/maps/.
### Usage
`generator.py [OPTION]...`

|short| full option| description |
| --- | ---------- | ----------- |
|-g   | --gametype   | Additionally print the rotation separated by game types. |
|-k   | --keep   | Repeat from beginning while keeping the order of maps for a certain game type if all available maps have already been used instead of altering the order randomly. |
|-n=N   |    | Sets the number of matches to N. Default: N=1|
|-p   | --praise   | Praise the current most skilled Brawl Stars player. Use this option or the sequence shall be cursed! |
|-r=S   |   | Sets the random seed to S. Must be an integer number. |
|-s   | --shuffle   | Shuffle the game types for each match. |
|-t=T   |   | Sets the game types played within a single match to T. T must be a list of numbers referring to the types. See Type List Syntax for more information. Default: T=[0]|

##### Examples
To generate a rotation with 5 matches using all 3vs3 game types for each match and random seed 42:
```
generator.py -r=42 -n=5 -t=[1,2,3,4,5] 
```
To generate a rotation with 10 matches using only showdown for each match:
```
generator.py -n=10 -t=[0] 
```
To generate a rotation with 7 matches using only Brawl Ball and Bounty for each match, where each match should randomly start with Brawl Ball or Bounty:
```
generator.py -n=10 -t=[3,4] --shuffle
```
To generate a sequence using the game types Bounty, Bounty, Showdown, Brawl Ball, Brawl Ball, Siege (only once):
```
generator.py -t=[3,3,0,4,4,5]
```

### Type List Syntax
To pass the game types for the matches use `-t=T` option,
where `T` is a list of the form `[t1,t2,...,tn]` where `t1,t2,...,tn` are numbers corresponding to game types:
| number | Game Type |
| ------ | --------- |
| 0 | Showdown | 
| 1 | Gem Grab | 
| 2 | Heist |
| 3 | Bounty | 
| 4 | Brawl Ball | 
| 5 | Siege | 
| 6 | Robo Rumble | 
| 7 | Big Game | 
| 8 | Boss Fight |


### License
[Apache License](http://www.apache.org/licenses/LICENSE-2.0).
