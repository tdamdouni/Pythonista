#!/usr/bin/env python3
# coding: utf-8

# https://github.com/daniel-jozsef/Pythonista

# https://forum.omz-software.com/topic/3925/deterministic-password-management-util

import hashlib
import keychain
import math
import ui
import dialogs

appname = 'spellGen'
mysalt = b'123' #change this value!
myiter = 200000

class Magic(object):
	
	syllabs = (['N'] +
	  ['a','i','u','e','o'] +
	  ['ka','ki','ku','ke','ko'] +
	  ['ga','gi','gu','ge','go'] +
	  ['sa','si','su','se','so'] +
	  ['za','zi','zu','ze','zo'] +
	  ['ta','ti','tu','te','to'] +
	  ['da','di','du','de','do'] +
	  ['na','ni','nu','ne','no'] +
	  ['ha','hi','hu','he','ho'] +
	  ['ba','bi','bu','be','bo'] +
	  ['pa','pi','pu','pe','po'] +
	  ['ma','mi','mu','me','mo'] +
	  ['ra','ri','ru','re','ro'])
	
	base = 66
	
	def __init__( self, salt, maxiter ):
		self.salt = salt
		self.maxiter = maxiter
	
	def do_magic( self, basebytes, iteration ):
		hash = int.from_bytes(
		  hashlib.pbkdf2_hmac('sha256', basebytes, self.salt, self.maxiter - iteration ),
		  byteorder='big',
		  signed=False )
		spell=''
		while hash > 0:
			mod = hash % self.base
			spell = self.syllabs[mod] + spell
			hash = hash // self.base
		return spell
	
	def cook_basebytes( self, secret, service, account ):
		return ( service + account + secret ).encode(encoding='ascii',errors='replace')

class spellGenGui(ui.View):
	
	def did_load( self ):
		self.magic = Magic(mysalt, myiter)
		
		self.txt_service = self['txt_service']
		self.txt_account = self['txt_account']
		self.sld_iter = self['sld_iter']
		self.lbl_iter = self['lbl_iterdisp']
		self.btn_hash = self['btn_hash']
		self.btn_secret = self['btn_secret']
		self.txv_spell = self['txv_spell']
		
		self.sld_iter.action = self.sld_iter_update
		self.btn_hash.action = self.btn_hash_push
		self.btn_secret.action = self.btn_secret_push

		self.iter = 0
		self.secret = keychain.get_password(appname,appname)

		if self.secret is not None:
			self.activate_button()
	
	def mypresent( self ):
		if ui.get_screen_size()[1] >= 768:
			# iPad
			self.present('sheet')
		else:
			# iPhone
			self.present()

	def precook_string( self, rawstring ):
		return rawstring.casefold().strip()

	def activate_button( self ):
		self.btn_hash.enabled = True
		self.btn_hash.title = '✏️'

	def deactivate_button( self ):
		self.btn_hash.enabled = False
		self.btn_hash.title = '⛔️'

	def sld_iter_update( self, sender ):
		self.iter =  math.floor(self.sld_iter.value * 10)
		if self.iter == 10:
			self.iter = 9
		self.lbl_iter.text = str(self.iter)

	def btn_hash_push( self, sender ):
		service = self.precook_string(self.txt_service.text)
		account = self.precook_string(self.txt_account.text)
		self.txt_service.text = service
		self.txt_account.text = account
		if service:
			mybytes = self.magic.cook_basebytes(self.secret,service,account)
			spell = self.magic.do_magic( mybytes, self.iter )
			self.txv_spell.text = spell
		else:
			self.txv_spell.text = ''

	def btn_secret_push( self, sender ):
		tmpsecret = self.secret
		if tmpsecret is None:
			tmpsecret = ''
		tmpsecret = dialogs.text_dialog(
			title='Set secret',
			text=tmpsecret,
			autocorrection=False,
			autocapitalization=ui.AUTOCAPITALIZE_NONE,
			spellchecking=False)
		if tmpsecret is None:
			return
		tmpsecret = tmpsecret.strip()
		if tmpsecret:
			keychain.set_password(appname,appname,tmpsecret)
			self.secret = tmpsecret
			self.activate_button()
		else:
			keychain.delete_password(appname,appname)
			self.secret = None
			self.deactivate_button()

gui = ui.load_view(appname)
gui.mypresent()
