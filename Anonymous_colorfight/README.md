# ColorFight!

ColorFight is a game where you try to occupy as many cells as possible on the map.

## Rules

* When you join the game, you will be given a random cell as a start, this cell will be your first base.

* You can only attack the cell that's adjacent to your occupied cells.

* You can only attack one cell at a time. During that time, you are not able to attack other cells.

* Occupying an empty cell takes 2s.

* The time you need to attack an occupied cell is based on the last time when the cell is occupied. The longer the time is, the easier it would be to be attacked. The minimum time to occupy a cell is 3s. (The equation of the time to occupy is ```3 + 30 * (2 ^ (-x/30))```. So when it's just occupied, it takes 33s to attack it. After about 25s, it becomes 20s. After around 60s, it becomes 10s). If the cell is surrounded by more than 1 attacker's occupied cell, the time to take it is decreased. One extra adjacent cell takes off 25% to take the cell.

* You can attack your own cell to refresh the occupy time, but it would take the same amount of time as other players attacking it.

* Golden cells worth 10 times as normal cells.

* Your gold will accumulate 0.5 per second per golden cell you occupied. The maximum gold is 100.

* When your base cell is occupied by other players, one of your cells that's adjacent to it will become the base. If there's no adjacent cells without a building that's occupied by you, the base will disappear.

* If you lose all your bases, you will lose immediately. All your cells will become empty cells.

* You can build a base on any cell that you occupy using 60 gold. Building a base takes 30s and each player can only have 3 bases. You can only build a base every 30s, so even if your base building process is interrupt, you can't build another one until the time the base would finish.

* Your energy will accumulate 0.5 per second per energy cell you occupied. The maximum energy is 100.

* The time to take a cell will be divided by (1 + energy/200).

* Attacking other player's cell will cost you 5% of current energy.

* You have two active skills to use your energy or gold. You can either boost you attack speed or do a multiple attack/defense.

## How To Start

* First clone the git repository. `git clone https://github.com/gaogaotiantian/ColorFightAI.git`

* Then you can run the exampleAI by `python exampleAI.py`

* If your computer complains about `requests` module, try `pip install requests[security]` or `sudo pip install requests[security]` if it complains about privilege. 

* Or you can use python3 by `python3 exampleAI.py`. The library and the exampleAI support both python2 and python3. 

* You can watch the result here [https://colorfight.herokuapp.com/](https://colorfight.herokuapp.com)

## API

The module provided some API for the game. You are welcome to add your own API, even directly talk to the server with HTTP requests if you want.

`Game` is the main class for the API. You should instantiate an object for it like `g = Game()`.

### After that, you can do the following actions:

* `JoinGame(name)` will let you join the game with a name. ex. `g.JoinGame('MyAI')`. Notice the API is already optimized so when you try to join the game with the same name on the same computer(with the generated token file), it will not generate a user. You can continue to play the game as the user before. `name` has to be a `str`.

* `Refresh()` will get the current game data from the server. ex. `g.Refresh()`. This function will store the raw data into `self.data` which you can access if you want. Also this function will fill in `self.width` and `self.height` for the game, as well as `self.currTime` for the time of this information. For game that has a end time, `self.endTime` will be updated, otherwise it will be `0`.

* `GetCell(x,y)` is an easy way to access the data of one cell. ex. `g.GetCell(1,2)`. The function will return a `Cell` object which has all the data of a single cell at (x,y). If the pair (x,y) given is invalid, it will return `None`. x and y starts with `0`, and the maximum value is `g.width-1`, `g.height-1`, respectively.

* `AttackCell(x,y,boost=False)` is the attack action you need to play the game. ex. `g.AttackCell(2,2)`. It will try to attack the cell you specified. `boost` argument is `False` by default. If you set that to `True`, it will try to use 10 energy to boost the attack, which means it will take 1 second or 10% of the original take time(which is slower) to occupy the cell. If you don't have enough energy, the action will fail. The return value will be a tuple with 3 items. Returning `(True, None, None)` means the action is successful. Otherwise it will return a tuple `(False, err_code, err_msg)` where `err_code` will contain the error code from the server and `err_msg` will contain the reason it failed.

* `BuildBase(x,y)` is the action to build a new base. ex. `g.BuildBase(3,3)`. It will try to build a base on the cell you specified. The return value is similar to `AttackCell()`.

* `Blast(x,y,direction)` is a multi clear skill you can use if you have enough energy. `direction` should be either `"square"` or `"vertical"` or `"horizontal"`. `direction` defines how the multi clear will be take effect. `"square"` means around the cell you specified(a 3x3 square). `"vertical"` means 4 cells on both the top and bottom of the cell you specified(a 1x9 vertical line). `"horizontal"` means 4 cells on both the left and right of the cell you specified(a 9x1 horizontal line). The skill takes 1 second and 30 energy and make all the cells you choose(excluding your specified cell and the cell that's already owned by you) empty(no owners). Also it needs to be used on the cell that you own. 

* `MultiAttack(x, y)` is a multi attack skill you can use if you have enough gold. You will attack all four cells that are adjacent to the specified cell simultaneously if the cells are attackable(if it's adjacent to at least one of your cell and is not being attacked now). The skill takes 40 gold and your cd time will become the longest time of all take times of the cells you attack.

### You also have the following data in `Game`:

* `uid` contains your user id. That's the unique identification for you.

* `gameId` is a unique id for the current game. This is generated randomly for each game.

* `endTime` is the time when the current game will end. If it's `0`, it's unlimited time game. This is a timestamp from the server.

* `joinEndTime` is the time when the current game will stop allowing player to join. If it's `0`, then there's no limit for join time. This is a timestamp from the server.

* `width` and `height` contains the width and height of the current game.

* `currTime` is the current time of the current data from the server. This is a timestamp from the server.

* `users` is a list of `User` object which has all the user info.

* `cdTime` is your cd time.

* `gold` is your current gold.

* `energy` is your current energy.

* `cellNum` is your cell number.

* `baseNum` is your base number.

* `goldCellNum` is your golden cell number.

* `energyCellNum` is your energy cell number.

## Cell Data

* `owner`: who owns this cell now. It's a user id.

* `x`: x coordinate.

* `y`: y coordinate.

* `isTaking`: is this cell being attacked. If it's `True` then you can't attack it.

* `attacker`: who is attacking this cell now. Invalid if `isTaking` is `False`.

* `occupyTime`: when is this cell occupied. Server side time in seconds. This is a timestamp from the server.

* `attackTime`: when is this cell attacked. Invalid if `isTaking` is `False`. This is a timestamp from the server.

* `takeTime`: how long it would take if you attack this cell. This is a number of seconds.

* `finishTime`: when will the attack finish. Invalid if `isTaking` is `False`. This is a timestamp from the server.

* `cellType`: `'gold'` if it's a golden cell, 'energy' if it's a energy cell and `'normal'` if it's a normal cell.

* `buildType`: `'base'` if there's a base built on it.
 
* `isBase`: if it's a base of the player.

* `isBuilding`: if there's a base being built on the cell.

* `buildTime`: when is the base built on this cell.

## User Data

* `id`: unique user identification.

* `name`: user name.

* `cdTime`: when can this user attack again. This is a timestamp from the server.

* `cellNum`: how many cells does this user occupy.

* `baseNum`: how many bases does this user occupy.

* `energyCellNum`: how many energy cells does this user occupy.

* `goldCellNum`: how many golden cells does this user occupy.

* `gold`: hou much gold does this user have.

* `energy`: hou much energy does this user have.

## Error Code from AttackCell() and BuildBase()

* 0: Success.

* 1: The cell you attack is invalid. It could be that your input is out of the map, or the cell you attack is not adjacent to your occupied cells.

* 2: The cell you attack is being taken by another player.

* 3: You are in CD time. You can't attack any cell now.

* 4: The game already ends.

* 5: You don't have enough gold or energy.

* 6: The cell is already a base.

* 7: You are already building a base.

* 8: You reached the base number limit.
