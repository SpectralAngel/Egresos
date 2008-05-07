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

class Sobrevivencia(controllers.Controller):
	
	@expose()
	def index(self,  tg_errors=None):
		
		if tg_errors:
			tg_errors = [(param,inv.msg,inv.value) for param, inv in tg_errors.items()]
		
		return dict(tg_errors=tg_errors)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(sobrevivencia=validators.Int()))
	def default(self, sobrevivencia):
		
		return dict(sobrevivencia=model.Sobrevivencia.get(sobrevivencia))
	
	@error_handler(index)
	@validate(validators=dict(sobrevivencia=validators.Int()))
	def mostrar(self, sobrevivencia):
		
		return self.default(sobrevivencia)
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(afiliado=validators.Int(),
							monto=validators.Money(),
							fecha=validators.DateTimeConverter(format='%d/%m/%Y'),
							cheque=validators.String()))
	def agregar(self, afiliado, **kw):
		
		afiliado = model.Afiliado.get(afiliado)
		
		sobrevivencia = model.Sobrevivencia(**kw)
		sobrevivencia.afiliado = afiliado
		sobrevivencia.flush()
		
		flash('Se ha agregado el Beneficio de Sobrevivencia al afiliado %s' % afiliado.id)
		
		raise redirect(tg.url('/'))
	
	@error_handler(index)
	@expose()
	@validate(validators=dict(sobrevivencia=validators.Int()))
	def eliminar(self, sobrevivencia):
		
		sobrevivencia = model.Sobrevivencia.get(sobrevivencia)
		afiliado = sobrevivencia.afiliado
		sobrevivencia.delete()
		
		flash('Se ha eliminado el Beneficio de Sobrevivencia al afiliado %s' % afiliado.id)
		
		raise redirect(tg.url('/'))
	
	@error_handler(index)
	@expose(template="egresos.templates.sobrevivencia.reporte")
	@validate(validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
							fin=validators.DateTimeConverter(format='%d/%m/%Y')))
	def reporte(self, inicio, fin):
		
		sobrevivencias = model.Sobrevivencia.query.all()
		
		return dict(sobrevivencias=[s for s in sobrevivencias if s.fecha >= inicio or s.fecha >= fin], inicio=inicio, fin=fin)
