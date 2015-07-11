#!/usr/bin/env python3
import random, curses
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
	def __init__(self, index: int, name: str, color: InkColor, spawn: Cell):#-> None:
		self.index = index
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
		self.respawn()
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
	def __init__(self, row: int, col: int, cellType: CellType, numTeams: int):#-> None:
		self.row = row
		self.col = col
		self.inkLevels = [0.0 for i in range(0,numTeams)] # array of floats of ink levels for each color/team; sum ≤ 1 (?)
		self.cellType = cellType
	def take_hit(self, inkTeam: Team, size):#-> None:
		self.inkLevels[inkTeam.index] += size
		levelSum = sum(self.inkLevels)
		if self.inkLevels[inkTeam.index] >= 1.0:
			self.inkLevels[inkTeam.index] = 1.0
			for i in range(len(self.inkLevels)):
				if i != inkTeam.index:
					self.inkLevels[i] = 0.0
		elif levelSum > 1.0:
			otherSum = sum([self.inkLevels[i] for i in range(len(self.inkLevels)) if i != inkTeam.index])
			for i in range(len(self.inkLevels)):
				if i != inkTeam.index:
					self.inkLevels[i] /= otherSum
					self.inkLevels[i] *= 1.0 - self.inkLevels

class Map(object):
	"""docstring for Map"""
	_default_cells = [[Cell(row, col, CellType.floor, numTeams) for col in range(0,80)] for row in range(0,24)]
	def __init__(self, name: str, numTeams: int, cells: list = _default_cells):#-> None:
		self.name = name
		self.numTeams = numTeams
		self.cells = cells

