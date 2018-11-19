# -*- coding: utf-8 -*-
# @file: Unicode Print Utility
# @author: Daniel Yuan

SUPER_SCRIPTS = {ord(c): ord(t) for c, t in zip(u"0123456789", u"⁰¹²³⁴⁵⁶⁷⁸⁹")}
SUB_SCRIPTS = {ord(c): ord(t) for c, t in zip(u"0123456789", u"₀₁₂₃₄₅₆₇₈₉")}
def super_script(number):
  return u'{}'.format(number).translate(SUPER_SCRIPTS)

def sub_script(number):
  return u'{}'.format(number).translate(SUB_SCRIPTS)
