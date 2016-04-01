# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista
#
# The only purpose of this module is to preserve the variable g_log_state over
# over reloads of module "log". This module is imported by "log" but it is not
# reloaded. It does not have to be since the likelyhood of any change is small. :-)

global g_log_started

g_log_started = False

def get_log_started():    
  global g_log_started
  
  return g_log_started
  
  
def set_log_started(log_started):
  global g_log_started
  
  g_log_started = log_started