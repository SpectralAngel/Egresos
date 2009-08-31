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
from turbogears 	import controllers, flash, validators
from turbogears		import expose, paginate, validate, error_handler
# from egresos import model
from turbogears 	import identity, redirect
from cherrypy   	import request, response
from egresos		import breadcrumbs
from egresos		import model
from sobrevivencia  import Sobrevivencia
from seguro 		import Seguro
from auxilio		import Auxilio
from funebre		import Funebre
from devolucion 	import Devolucion
# from egresos import json
# import logging
# log = logging.getLogger("egresos.controllers")

class Root(controllers.RootController):
	
	sobrevivencia = Sobrevivencia()
	seguro = Seguro()
	auxilio = Auxilio()
	devolucion = Devolucion()
	funebre = Funebre()
	
	@identity.require(identity.not_anonymous())
	@expose(template="egresos.templates.welcome")
	# @identity.require(identity.in_group("admin"))
	def index(self):
		import time
		return dict(now=time.ctime())
	
	@error_handler(index)
	@expose(template="egresos.templates.afiliado")
	@validate(validators=dict(afiliado=validators.Int()))
	def afiliado(self, afiliado):
		
		return dict(afiliado=model.Afiliado.get(afiliado))

	@expose(template="egresos.templates.login")
	def login(self, forward_url=None, previous_url=None, *args, **kw):

		if not identity.current.anonymous and identity.was_login_attempted() \
				and not identity.get_identity_errors():
			raise redirect(tg.url(forward_url or previous_url or '/', kw))

		forward_url = None
		previous_url = request.path

		if identity.was_login_attempted():
			msg = _("The credentials you supplied were not correct or "
				   "did not grant access to this resource.")
		elif identity.get_identity_errors():
			msg = _("You must provide your credentials before accessing "
				   "this resource.")
		else:
			msg = _("Please log in.")
			forward_url = request.headers.get("Referer", "/")

		response.status = 403
		return dict(message=msg, previous_url=previous_url, logging_in=True,
			original_parameters=request.params, forward_url=forward_url)

	@expose()
	def logout(self):
		identity.current.logout()
		raise redirect("/")
