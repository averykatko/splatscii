#!/usr/bin/env python3
import random
from enum import Enum

class Weapon(object):
	"""docstring for Weapon"""
	def __init__(self, arg):
		super(Weapon, self).__init__()
		self.arg = arg

class InkColor(Enum):
	blue = 1
	orange = 2
	# TODO

class Projectile(object):
	"""superclass of all projectiles"""
	def __init__(self, pos: tuple, vel: tuple):#-> None:
		self.pos = pos
		self.vel = vel
	def hit(self, target):#-> None:
		pass

class InkBlob(Projectile):
	"""docstring for InkBlob"""
	def __init__(self, pos: tuple, vel: tuple, size, team: Team):#-> None:
		super(InkBlob, self).__init__(pos, vel)
		self.size = size
		self.team = team
	def hit(self, target):#-> None:
		if isinstance(target, Cell):
			target.take_hit(self.team, self.size)
		elif isinstance(target, Inkling):
			target.take_hit(self.team, self.size)
		else:
			pass # TODO: hcf

class Team(object):
	"""docstring for Team"""
	def __init__(self, name: str, color: InkColor, spawn: Cell):#-> None:
		self.name = name
		self.color = color
		self.spawn = spawn

class Inkling(object):
	"""docstring for Inkling"""
	def __init__(self, name: str, team: Team, shoes: Shoes, clothes: Clothes, headgear: Headgear, weapon: Weapon):#-> None:
		self.name = name
		self.team = team
		self.shoes = shoes
		self.clothes = clothes
		self.headgear = headgear
		self.weapon = weapon
		self.respawn() # respawn will init hp, ink, etc
	def take_hit(self, inkTeam: Team, size):#-> None:
		self.hp -= size * self.get_defense_modifier()
		if self.hp <= 0.0:
			self.respawn() # TODO: time-delayed respawn
	def get_max_hp(self):#-> float:
		return 100.0 # TODO
	def get_max_ink(self):#-> float:
		return 100.0 # TODO
	def get_offense_modifier(self):#-> float:
		return 1.0 # TODO
	def get_defense_modifier(self):#-> float:
		return 1.0 # TODO
	def get_hp_recharge_rate(self):#-> float:
		return 1.0 # TODO
	def get_ink_recharge_rate(self):#-> float:
		return 1.0 # TODO
	def respawn(self):#-> None:
		self.location = self.team.spawn
		self.hp = self.get_max_hp()
		self.ink = self.get_max_ink()

class CellType(Enum):
		floor = 1
		wall = 2

class Cell(object):
	"""docstring for Cell"""
	def __init__(self, row: int, col: int, cellType: CellType, teams: list):#-> None:
		self.row = row
		self.col = col
		self.inkLevels = {t: 0.0 for t in teams}
		self.cellType = cellType
	def take_hit(self, inkTeam: Team, size):#-> None:
		self.inkLevels[inkTeam] += size
		levelSum = sum(self.inkLevels.values())
		if self.inkLevels[inkTeam] >= 1.0:
			self.inkLevels[inkTeam] = 1.0
			for t in self.inkLevels:
				if t != inkTeam:
					self.inkLevels[t] = 0.0
		elif levelSum > 1.0:
			otherSum = sum([self.inkLevels[t] for t in inkLevels if t != inkTeam])
			for t in inkLevels:
				if t != inkTeam:
					self.inkLevels[t] /= otherSum
					self.inkLevels[t] *= 1.0 - self.inkLevels

class Map(object):
	"""docstring for Map"""
	def __init__(self, name: str, teams: list, cells: list = None):#-> None:
		self.name = name
		self.teams = teams
		self.cells = cells
		if cells is None:
			cells = [[Cell(row, col, CellType.floor, teams) for col in range(0,80)] for row in range(0,24)]

