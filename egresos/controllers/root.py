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

from turbogears import (controllers, validators, expose, validate,
                        error_handler)
from turbogears.i18n.tg_gettext import gettext as _
from turbogears import identity, redirect, url
from cherrypy import request, response
from egresos import model
from egresos.controllers import (sobrevivencia, seguro, auxilio, funebre,
                                 devolucion, filial)


class Root(controllers.RootController):
    sobrevivencia = sobrevivencia.Sobrevivencia()
    seguro = seguro.Seguro()
    auxilio = auxilio.Auxilio()
    devolucion = devolucion.Devolucion()
    funebre = funebre.Funebre()
    filial = filial.Filial()

    @identity.require(identity.not_anonymous())
    @expose(template="egresos.templates.welcome")
    def index(self):

        return dict(indemnizaciones=list())

    @expose(template="egresos.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):
        if not identity.current.anonymous \
                and identity.was_login_attempted() \
                and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url = None
        previous_url = url(request.path_info)

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
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")

    @error_handler(index)
    @expose(template="egresos.templates.afiliado")
    @validate(validators=dict(afiliado=validators.Int()))
    def afiliado(self, afiliado):

        return dict(afiliado=model.Afiliado.get(afiliado))
