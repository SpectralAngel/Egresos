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

class Devolucion(controllers.Controller, identity.SecureResource):
	
	require = identity.not_anonymous()
	
	@expose()
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(devolucion=validators.Int()))
	def default(self, devolucion):
		
		return dict(devolucion=model.Devolucion.get(devolucion))
	
	@error_handler(index)
	@validate(validators=dict(devolucion=validators.Int()))
	def mostrar(self, devolucion):
		
		return self.default(devolucion)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(afiliado=validators.Int(),
							concepto=validators.String(),
							monto=validators.String(),
							fecha=validators.DateTimeConverter(format='%d/%m/%Y'),
							cheque=validators.String()))
	def agregar(self, afiliado, **kw):
		
		afiliado = model.Afiliado.get(afiliado)
		kw['monto'] = Decimal(kw['monto'])
		devolucion = model.Devolucion(**kw)
		devolucion.afiliado = afiliado
		devolucion.flush()
		
		flash('Se ha agregado la Devolción al afiliado %s' % afiliado.id)
		
		raise redirect(tg.url('/'))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(auxilio=validators.Int()))
	def eliminar(self, devolucion):
		
		devolucion = model.Devolucion.get(devolucion)
		afiliado = devolucion.afiliado
		devolucion.delete()
		
		flash('Se ha eliminado el devolución al afiliado %s' % afiliado.id)
		
		raise redirect(tg.url('/'))
	
	@error_handler(index)
	@expose(template="egresos.templates.devolucion.reporte")
	@validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
							fin=validators.DateTimeConverter(format='%d/%m/%Y')))
	def reporte(self, inicio, fin):
		
		devoluciones = model.Devolucion.query.all()
		
		return dict(devoluciones=[s for s in devoluciones if s.fecha >= inicio or s.fecha >= fin], inicio=inicio, fin=fin)

