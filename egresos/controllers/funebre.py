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

from turbogears import controllers, identity, validators
from turbogears import flash, redirect
from turbogears import expose, validate, error_handler
from egresos import model
from decimal import Decimal


class Funebre(controllers.Controller, identity.SecureResource):
    require = identity.not_anonymous()

    @expose()
    def index(self, tg_errors=None):
        if tg_errors:
            tg_errors = [(param, inv.msg, inv.value) for param, inv in
                         tg_errors.items()]

        return dict(tg_errors=tg_errors)

    @error_handler(index)
    @expose()
    @validate(validators=dict(funebre=validators.Int()))
    def default(self, funebre):
        return dict(funebre=model.Funebre.get(funebre))

    @error_handler(index)
    @validate(validators=dict(funebre=validators.Int()))
    def mostrar(self, funebre):
        return self.default(funebre)

    @error_handler(index)
    @expose()
    @validate(validators=dict(afiliado=validators.Int(),
                              pariente=validators.UnicodeString(),
                              monto=validators.UnicodeString(),
                              fecha=validators.DateTimeConverter(
                                  format='%d/%m/%Y'),
                              cheque=validators.UnicodeString(),
                              banco=validators.UnicodeString()))
    def agregar(self, afiliado, **kw):
        afiliado = model.Afiliado.get(afiliado)
        kw['monto'] = Decimal(kw['monto'].replace(',', ''))
        funebre = model.Funebre(**kw)
        funebre.afiliado = afiliado
        funebre.flush()

        flash('Se ha agregado la Ayuda Funebre al afiliado %s' % afiliado.id)

        raise redirect('/')

    @error_handler(index)
    @expose()
    @validate(validators=dict(funebre=validators.Int()))
    def eliminar(self, funebre):
        funebre = model.Funebre.get(funebre)
        afiliado = funebre.afiliado
        funebre.delete()

        flash('Se ha eliminado la Ayuda Funebre al afiliado %s' % afiliado.id)

        raise redirect('/')

    @error_handler(index)
    @expose(template="egresos.templates.funebre.reporte")
    @validate(
        validators=dict(inicio=validators.DateTimeConverter(format='%d/%m/%Y'),
                        fin=validators.DateTimeConverter(format='%d/%m/%Y')))
    def reporte(self, inicio, fin):
        funebres = model.Funebre.query.all()

        return dict(funebres=
                    [s for s in funebres if
                     s.fecha >= inicio or s.fecha >= fin],
                    inicio=inicio, fin=fin)
