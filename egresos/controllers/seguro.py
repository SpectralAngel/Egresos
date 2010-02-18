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

import turbogears as tg
from turbogears	import controllers, identity, validators
from turbogears	import flash, redirect
from turbogears	import expose, paginate, validate, error_handler
from cherrypy	import request, response
from egresos	import model
from decimal	import *

class Beneficiario(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	@expose()
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(seguro=validators.Int(),
							nombre=validators.String(),
							cheque=validators.String(),
							monto=validators.String()))
	def agregar(self, seguro, **kw):
		
		seguro = model.Seguro.get(seguro)
		kw['monto'] = Decimal(kw['monto'])
		beneficiario = model.Beneficiario(**kw)
		beneficiario.seguro = seguro
		beneficiario.flush()
		
		raise redirect(tg.url('/seguro/%s' % seguro.id))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(beneficiario=validators.Int()))
	def eliminar(self, beneficiario):
		
		beneficiario = model.Beneficiario.get(beneficiario)
		seguro = beneficiario.seguro
		beneficiario.delete()
		flash('Se ha eliminado el beneficiario')
		
		raise redirect(tg.url('/seguro/%s' % seguro.id))

class Seguro(controllers.Controller):
	
	beneficiario = Beneficiario()
	
	@expose()
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose(template="egresos.templates.seguro.seguro")
	@validate(validators=dict(seguro=validators.Int()))
	def default(self, seguro):
		
		return dict(seguro=model.Seguro.get(seguro))
	
	@error_handler(index)
	@validate(validators=dict(seguro=validators.Int()))
	def mostrar(self, seguro):
		
		return self.default(seguro)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(afiliado=validators.Int(),
							fecha=validators.DateTimeConverter(format='%d/%m/%Y'),
							fallecimiento=validators.DateTimeConverter(format='%d/%m/%Y')))
	def agregar(self, afiliado, **kw):
		
		afiliado = model.Afiliado.get(afiliado)
		
		seguro = model.Seguro(**kw)
		seguro.afiliado = afiliado
		seguro.flush()
		
		flash('Se ha agregado el Seguro de Vida al afiliado %s' % afiliado.id)
		
		return self.default(seguro.id)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(seguro=validators.Int()))
	def eliminar(self, seguro):
		
		seguro = model.Seguro.get(seguro)
		afiliado = seguro.afiliado
		seguro.delete()
		
		flash('Se ha eliminado el Seguro de Vida al afiliado %s' % afiliado.id)
		
		raise redirect(tg.url('/'))
	
	@error_handler(index)
	@expose(template="egresos.templates.seguro.reporte")
	@validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
							fin=validators.DateTimeConverter(format='%d/%m/%Y')))
	def reporte(self, inicio, fin):
		
		seguros = model.Seguro.query.all()
		
		return dict(seguros=[s for s in seguros if s.fecha >= inicio or s.fecha >= fin], inicio=inicio, fin=fin)
