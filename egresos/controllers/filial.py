#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright (c) 2010 Carlos Flores <cafg10@gmail.com>
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
from turbogears import controllers, identity, validators
from turbogears import expose, validate, redirect
from egresos import model
from decimal import Decimal

class PagoFilial(controllers.Controller, identity.SecureResource):
    
    require = identity.not_anonymous()
    
    @expose()
    @validate(validators=dict(
              filial=validators.Int(),
              monto=validators.UnicodeString(),
              detalle=validators.UnicodeString(),
              valor=validators.UnicodeString()
              ))
    def agregar(self, filial, **kw):
        
        filial = model.Filial.get(filial)
        kw['monto'] = Decimal(kw['monto'])
        kw['valor'] = Decimal(kw['valor'])
        
        kw['saldo'] = filial.saldo() + kw['monto']
         
        pago = model.PagoFilial(**kw)
        pago.filial = filial
        pago.flush()
        
        raise redirect(tg.url('/filial/%s' % filial.id))
    
    @expose()
    @validate(validators=dict(pago=validators.Int()))
    def eliminar(self, pago):
        
        pago = model.PagoFilial.get(pago)
        filial = pago.filial
        pago.delete()
        
        raise redirect(tg.url('/filial/%s' % filial.id))

class Filial(controllers.Controller, identity.SecureResource):
    
    require = identity.not_anonymous()
    
    pago = PagoFilial()
    
    @expose(template='egresos.templates.filial.index')
    def index(self):
        
        return dict(departamentos=model.Departamento.query.all(),
                    filiales=model.Filial.query.all())
    
    @expose(template='egresos.templates.filial.filial')
    @validate(validators=dict(filial=validators.Int()))
    def default(self, filial):
        
        return dict(filial=model.Filial.get(filial))
    
    @expose()
    @validate(validators=dict(filial=validators.Int()))
    def mostrar(self, filial):
        
        return self.default(filial)
    
    @expose()
    @validate(validators=dict(departamento=validators.Int(), instituto=validators.UnicodeString()))
    def agregar(self, departamento, **kw):
        
        departamento = model.Departamento.get(departamento)
        
        filial = model.Filial(**kw)
        filial.departamento = departamento
        filial.flush()
        
        raise redirect(tg.url('/filial/%s' % filial.id))
