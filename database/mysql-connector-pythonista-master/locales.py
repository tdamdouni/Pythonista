# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2012, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


__all__ = [
	'get_client_error'
]

import errorcode

def get_client_error(error, language='eng'):
	"""Lookup client error

	This function will lookup the client error message based on the given
	error and return the error message. If the error was not found,
	None will be returned.

	Error can be either an integer or a string. For example:
		error: 2000
		error: CR_UNKNOWN_ERROR

	The language attribute can be used to retrieve a localized message, when
	available.

	Returns a string or None.
	"""
	try:
		tmp = __import__('locales.%s' % language,
				   		 globals(), locals(), ['client_error'])
	except ImportError:
		raise ImportError("No localization support for language '%s'" % (
						  language))
	client_error = tmp.client_error

	if isinstance(error, int):
		errno = error
		for key, value in errorcode.__dict__.items():
		    if value == errno:
		        error = key
		        break

	if isinstance(error, (str)):
		try:
			return getattr(client_error, error)
		except AttributeError:
			return None

	raise ValueError("error argument needs to be either an integer or string")

