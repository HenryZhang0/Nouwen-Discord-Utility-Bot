import math
from weapon import Weapon
from shield import Shield


class Player:

    def __init__(self, name, hp=3, level=1): #constructor
        self.name = name
        self.level = level
        self.coins = 10
        self.hp = hp
        self.weapon = Weapon('Rusty Sidearm', 30, 1, 1)
        self.shield = Shield('Paper Shield', 1, 0)
        self.arsenal = list()
    #end of __init__()

    def __repr__(self): #for the pokemon name
        return str(self.name)
    def __str__(self):
        return str(self.name)
    def add_coin(self, amount):
        self.coins += amount

    def attack(self, enemy): #function to attack another pokemon
        amount = self.weapon.plus
        
        #dmg = int(amount*multiplier)
        dmg = amount
        msg = '<:pistol:698010815348998174> `' +str(self) +'\'s '+str(self.weapon) +' did ' + str(dmg)+ " damage!`"
        msg += '\n' + enemy.takeDamage(dmg) #damages opponent
        return msg
    #end of attack()

    def takeDamage(self, damage): #function to lose HP
        self.hp -= damage #takes damage
        msg = 'take damage message'
        if self.hp <= 0: #if the pokemon dies
            self.hp = 0
            msg = '**'+self.name + " is killed! ☠☠**"
        else:
            msg = '`'+str(self) + " has "+ str(self.getHp()) + " HP left` "+ self.getHp()*'💘'
        return msg
    #end of takeDamage()

    def printStats(self): #prints the stats lol... what else?
        print(self.name+" ---- lvl", self.__level)
        print("_"*14)
        print("HP\t\t", str(self.__hp)+"/" + str(self.maxHp))
        print("TYPE\t\t", self.element)
    #end of printStats()

    def revive(self): #revives the pokemon
        self.__hp = self.maxHp

    def heal(self): #heals the pokemon
        self.hp += 1
        if self.hp > 100: #subtracts extra if hp goes over maxHp
            self.hp = self.maxHp
    #end of heal()

    def getHp(self): 
        return self.hp

    def getLevel(self):
        return self.__level

    def levelUp(self, enemy): #levels up 
        gain = math.ceil(enemy.getLevel()*enemy.evo/3)
        self.__level += gain
        print("\n", self, "leveled up to", self.getLevel(), "HP!")
    #end of levelUp()