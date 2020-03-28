# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 23:37:52 2020

@author: rreal
"""
import pandas as _pd

edosmx_iso = _pd.DataFrame(
    data={'ISO 3166-2':
          ['AGU', 'BCN', 'BCS', 'CAM', 'CHP', 'CHH', 'CMX', 'COA', 'COL',
           'DUR', 'GUA', 'GRO', 'HID', 'JAL', 'MEX', 'MIC', 'MOR', 'NAY',
           'NLE', 'OAX', 'PUE', 'QUE', 'ROO', 'SLP', 'SIN', 'SON', 'TAB',
           'TAM', 'TLA', 'VER', 'YUC', 'ZAC']
          },
    index=['Aguascalientes', 'Baja California', 'Baja California Sur',
          'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México',
          'Coahuila', 'Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
          'Jalisco', 'México', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León',
          'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí',
          'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz',
          'Yucatán', 'Zacatecas'],
    )

edosmx_abr = _pd.DataFrame(
    data={'ABREVIATURA':
          ['Ags.',  'B.C.', 'B.C.S.', 'Camp.', 'Chis.', 'Chih.', 'C.D.Mx.',
           'Coah.', 'Col.', 'Dgo.', 'Gto.', 'Gro.', 'Hgo.', 'Jal.',
           'Edo. Méx.', 'Mich.', 'Mor.', 'Nay.', 'N.L.', 'Oax.', 'Pue.',
           'Qro.', 'Q. Roo.', 'S.L.P.', 'Sin.', 'Son.', 'Tab.', 'Tamps.',
           'Tlax.', 'Ver.', 'Yuc.', 'Zac.']
          },
    index=['Aguascalientes', 'Baja California', 'Baja California Sur',
          'Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México',
          'Coahuila', 'Colima', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
          'Jalisco', 'México', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León',
          'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí',
          'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz',
          'Yucatán', 'Zacatecas'],
    )