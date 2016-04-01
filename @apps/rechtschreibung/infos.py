#coding: utf-8
info_messages =  { 
                  'simplification_sch_s' : 'In slavischen Sprachen wird zum Teil der Buchstabe "š" verwendet, um den Laut des deutschen "sch" zu repräsentieren. Wegen der Kürze liegt eine Ersetzung nahe. Auch in den Buchstabenkombinationen "sp" und "st" ist zum Teil der gleiche Laut enthalten und wird daher entsprechend ersetzt. Dadurch wird dem Leser ermöglicht, zwischen den beiden vorkommenden Sprechweisen zu unterscheiden: "st" als Laut "s"+"t" bleibt gleich, wohingegen "st" als Laut "scht" zu "št" wird. Entsprechendes gilt für "sp".',
                  
                  'simplification_tsch_c' : 'In slavischen Sprachen wird zum Teil der Buchstabe "č" verwendet, um den Laut des deutschen "tsch" zu repräsentieren. Wegen der Kürze liegt eine Ersetzung nahe.',
                  
                  'harmonization_homophony_elongated_vowels' : 'In manchen Fällen wird bewusst darauf verzichtet, lange Vokale exlizit zu denen. Das tritt vor allem in einfachen einsilbigen Worten auf. Zum Beispiel wird "dem" mit einfachem "e" geschrieben, wohingegen das gleichklingende "Lehm" mit Dehnung geschrieben wird. ' + chr(10) + chr(10) + 'Diese Regel sorgt dafür, dass in all diesen Fällen die gewählte Vokaldehnung (standardmäßig über "h") verwendet wird.',
                  
                  'harmonization_homophony_terminating_consonants' : 'In manchen Fällen wird bewusst darauf verzichtet, Konsonanten nach kurzen Vokalen am Ende von Worten zu verdoppeln. Dies tritt besonders bei bei einfachen einsilbigen Worten auf. Zum Beispiel wird "tritt" mit Dopplung geschrieben, wohingegen das gleichklingende "mit" mit einfachem Konsonant geschrieben wird.' + chr(10) + chr(10) + 'Diese Regel sorgt dafür, dass in all diesen Fällen die Verdopplung der Konsonanten aktiviert wird, außer die Konsonantendopplung wurde global abgeschaltet (siehe "Vereinfachung").',
                  
                  'elongation':'Dieser Schalter regelt die Darstellung eines langen Vokals. Es gibt sechs Varianten: ' + chr(10) + chr(10) + 'Standard: wählt die derzeit gültige Variante (dies ist uneinheitlich!),' + chr(10) + chr(10) + 'keine: stellt lange Vokale einfach, d.h. wie kurze dar,' + chr(10) + chr(10) + '"e": hängt an Vokale ein "e" an,' + chr(10) + chr(10) + '"h": hängt an Vokale ein "h" an,' + chr(10) + chr(10) + 'Dopplung: verdoppelt den Vokal,' + chr(10) + chr(10) + 'Makron: setzt einen Strich (Makron) als Akzent über den Vokal. Hinweis: Es ist zur Zeit unklar, wie das Makron mit dem Umlautzeichen kombiniert werden kann. Deswegen wird bei Umlauten die Dopplung verwendet.'} 

def get_info_messages():
  return info_messages
