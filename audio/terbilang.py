from __future__ import print_function
# TERBILANG
# Menyebut angka dalam bahasa Indonesia
# by: @beezing
# https://gist.github.com/git-bee/ed124e127896009b12f3

angka = {'0':'nol',
         '1':'satu ',
         '2':'dua ',
         '3':'tiga ',
         '4':'empat ',
         '5':'lima ',
         '6':'enam ',
         '7':'tujuh ',
         '8':'delapan ',
         '9':'sembilan '
         }
belas = 'belas '
puluh = 'puluh '
ratus = 'ratus '
group = ('', # this can be used for unit
         'ribu ',
         'juta ',
         'milyar ',
         'trilyun ',
         'dwiyar ',
         'tirta ',
         'triyar '
         )
se = 'se'
seribu = se+'ribu '

def terbilang(a):
  # split number into groups of 3 digits
  h = '{:,}'.format(a).split(',')
  # make sure left group contains 3 digits
  h[0] = '{:0>3d}'.format(int(h[0]))
  # count of groups
  g = len(h)-1
  f = False

  t = ''
  # iterate each group
  for i in h:
    # split digits of group
    iR,iP,iS = i

    # determine 'ratusan'
    if iR != '0':
      if iR == '1':
        t += se+ratus
      else:
        t += angka[iR]+ratus

    # determine 'puluhan'
    if iP != '0':
      # belasan
      if iP == '1':
        if i[1:] == '10':
          t += se+puluh
        elif i[1:] == '11':
          t += se+belas
        else:
          t += angka[iS]+belas
      # puluhan
      else:
        t += angka[iP]+puluh

    # determine 'satuan'
    if iS != '0':
      # skip 'sepuluh' and 'belas'
      if iP != '1':
        # fix for 'satu ribu'
        f = (i == '001' and g == 1)
        if f:
          t += se+group[g]
        else:
          t += angka[iS]

    # determine name of group
    if i != '000':
      # skip fix for 'seribu'
      if not f: t += group[g]

    # decrease group
    g -= 1

  # fix for 'nol'
  if a == 0: t = angka['0']

  return t

# ___ main program ___ #

import speech
from random import randint

def ngomong(txt):
  speech.say(txt,'id',0.25)

def rand_digit(d):
  b = ''
  digit = randint(1,d)
  for i in range(digit):
    b += str(randint(0,9))
  return int(b)

v = rand_digit(12)
s = '{:,}'.format(v).replace(',','.')
bilang = terbilang(v)

print(s+' = '+bilang)
ngomong(bilang)