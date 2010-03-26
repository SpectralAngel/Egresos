#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright © 2008 Carlos Flores <cafg10@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from datetime	import datetime, date
from elixir		import Entity, Field, OneToMany, ManyToOne, ManyToMany
from elixir		import options_defaults, using_options, setup_all
from elixir		import Integer, Boolean, Numeric
from elixir		import String, Unicode, Text
from elixir		import DateTime, Date
from turbogears	import identity

Currency = Numeric

options_defaults['autosetup'] = False

class Afiliado(Entity):
	
	"""Datos sobre un miembro
	
	Contiene los datos básicos sobre un miembro del COPEMH. Estos datos son en
	realidad parte de otra aplicación y no deben ser modificados por el gestor
	de recibos."""
	
	using_options(tablename='affiliate')
	
	nombre = Field(Unicode(50), colname='first_name')
	apellidos = Field(Unicode(50), colname='last_name')
	
	cotizacion = Field(String(20), colname='payment')
	auxilios = OneToMany("Auxilio")
	sobrevivencias = OneToMany("Sobrevivencia")
	funebres = OneToMany("Funebre")
	devoluciones = OneToMany("Devolucion")
	seguros = OneToMany("Seguro")

class Auxilio(Entity):
	
	using_options(tablename='auxilio')
	
	afiliado = ManyToOne("Afiliado")
	cobrador = Field(String(100))
	fecha = Field(DateTime, required=True, default=datetime.now)
	monto = Field(Currency, required=True)
	cheque = Field(String(20))
	banco = Field(Unicode(50))

class Sobrevivencia(Entity):
	
	using_options(tablename='sobrevivencia')
	
	afiliado = ManyToOne("Afiliado")
	fecha = Field(DateTime, required=True, default=datetime.now)
	monto = Field(Currency, required=True)
	cheque = Field(String(20))
	banco = Field(Unicode(50))

class Funebre(Entity):
	
	using_options(tablename='ayuda_funebre')
	
	afiliado = ManyToOne("Afiliado")
	fecha = Field(DateTime, required=True, default=datetime.now)
	monto = Field(Currency, required=True)
	cheque = Field(String(20))
	pariente = Field(String(20))
	banco = Field(Unicode(50))

class Seguro(Entity):
	
	using_options(tablename='seguro')
	
	afiliado = ManyToOne("Afiliado")
	fecha = Field(DateTime, required=True, default=datetime.now)
	fallecimiento = Field(DateTime, required=True, default=datetime.now)
	beneficiarios = OneToMany("Beneficiario")
	
	def monto(self):
		
		return sum(beneficiario.monto for beneficiario in self.beneficiarios)

class Beneficiario(Entity):
	
	using_options(tablename='beneficiario')
	
	seguro = ManyToOne("Seguro")
	nombre = Field(String(50), required=True)
	monto = Field(Currency, required=True)
	cheque = Field(String(20), required=True)
	banco = Field(Unicode(50))

class Devolucion(Entity):
	
	using_options(tablename='devolucion')
	
	afiliado = ManyToOne("Afiliado")
	concepto = Field(Text)
	fecha = Field(DateTime, required=True, default=datetime.now)
	monto = Field(Currency, required=True)
	cheque = Field(String(20))
	banco = Field(Unicode(50))

class Departamento(Entity):
	
	using_options(tablename='departamento')
	
	nombre = Field(Unicode(60))
	filiales = OneToMany('Filial')

class Filial(Entity):
	
	using_options(tablename='filial')
	
	instituto = Field(Unicode(255))
	departamento = ManyToOne('Departamento')
	pagos = OneToMany('PagoFilial')
	
	def saldo(self):
		
		return sum(p.monto for p in self.pagos)

class PagoFilial(Entity):
	
	using_options(tablename='pago_filial')
	
	filial = ManyToOne('Filial')
	dia = Field(Date, required=True, default=date.today)
	detalle = Field(Unicode(255))
	cheque = Field(Unicode(255))
	valor = Field(Currency)
	monto = Field(Currency)
	saldo = Field(Currency)

# the identity model

class Visit(Entity):
	"""
	A visit to your site
	"""
	using_options(tablename='visit')

	visit_key = Field(String(40), primary_key=True)
	created = Field(DateTime, nullable=False, default=datetime.now)
	expiry = Field(DateTime)

	def lookup_visit(cls, visit_key):
		return Visit.get(visit_key)
	lookup_visit = classmethod(lookup_visit)


class VisitIdentity(Entity):
	"""
	A Visit that is link to a User object
	"""
	using_options(tablename='visit_identity')

	visit_key = Field(String(40), primary_key=True)
	user = ManyToOne('User', colname='user_id', use_alter=True)


class Group(Entity):
	"""
	An ultra-simple group definition.
	"""
	using_options(tablename='tg_group')

	group_id = Field(Integer, primary_key=True)
	group_name = Field(Unicode(16), unique=True)
	display_name = Field(Unicode(255))
	created = Field(DateTime, default=datetime.now)
	users = ManyToMany('User', tablename='user_group')
	permissions = ManyToMany('Permission', tablename='group_permission')


class User(Entity):
	"""
	Reasonably basic User definition.
	Probably would want additional attributes.
	"""
	using_options(tablename='tg_user')

	user_id = Field(Integer, primary_key=True,colname="id")
	user_name = Field(Unicode(16), unique=True)
	email_address = Field(Unicode(255), unique=True)
	display_name = Field(Unicode(255))
	password = Field(Unicode(40))
	created = Field(DateTime, default=datetime.now)
	groups = ManyToMany('Group', tablename='user_group')

	def permissions(self):
		p = set()
		for g in self.groups:
			p |= set(g.permissions)
		return p
	permissions = property(permissions)


class Permission(Entity):
	"""
	A relationship that determines what each Group can do
	"""
	using_options(tablename='permission')

	permission_id = Field(Integer, primary_key=True)
	permission_name = Field(Unicode(16), unique=True)
	description = Field(Unicode(255))
	groups = ManyToMany('Group', tablename='group_permission')

# Set up all Elixir entities declared above

setup_all()
