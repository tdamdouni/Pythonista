# Ulam Zahlenspiralen

_Captured: 2017-03-08 at 09:38 from [musicdiver.com](http://musicdiver.com/wordpress/2017/02/ulam-zahlenspiralen/)_

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/numberspiralscreenshot-3-816x733.jpg)

Schuld an allem ist mein lieber Informatik Leistungskurs Lehrer, Herr Wolfgang Laubach, der mir schon damals - es mag ca. 1986 gewesen sein - den Floh ins Ohr setzte, als er uns eines Tages von [Stanislaw Ulam](https://de.wikipedia.org/wiki/Stanis%C5%82aw_Marcin_Ulam) und seiner „Zahlenspirale" berichtete. Ich bin Herrn Laubach fur so viele mathematische Kleinode so dankbar, nicht nur fur dieses!

### Primzahlen-Spiralen

Es geht um Primzahlen und deren Verteilung unter den naturlichen Zahlen. Die Story, die uns unser Lehrer erzahlte, ging in etwa so: Ulam saß mal wieder in einem langweiligen Vortrag und kritzelte gedankenverloren auf seinem Block vor ihm herum. Er begann, die naturlichen Zahlen in Form einer Spirale auf sein Kastchenpapier zu schreiben:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/img_0366.png)

> _Dann malte er all die Kastchen aus, in denen Primzahlen standen, also etwa so:_

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/img_0371.png)

Schon wenn man das fur wenige Zahlen, etwa die ersten 100 macht, gibt es interessanterweise ein paar Auffalligkeiten: die ausgemalten Kastchen scheinen sich gern auf Diagonalen Linien zu haufen!

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/img_0374.png)

Wenn man dann massiv herauszoomt, fallt es noch mehr auf (hier entspricht ein Pixel einer Zahl, schwarz wieder die Primzahlen):

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/img_0193.png)

> _Quelle: Wikipedia_

Hier sind die ersten 40.000 Zahlen zu sehen (200×200), darunter sind genau 4.203 Primzahlen, also sind ca. 10,5% schwarze Pixel im Bild. Man sieht klar v.a. diagonale Strukturen.

Aber keine Sorge: das wird keine Mathe-Abhandlung hier. _Warum_ das alles so ist, soll nicht Gegenstand dieses Blog-Beitrags sein, da gibt es [im Web schone Beitrage](http://ulamspiral.com). Ich will auf etwas ganz anderes hinaus.

### Computer Kurzweil

Solche mathematischen Spielereien haben mich schon immer fasziniert, spatestens seit der Oberstufe / dem Mathe LK. Was habe ich die Computer-Kurzweil Rubrik von [A.K. Dewdney](https://en.wikipedia.org/wiki/Alexander_Dewdney) in der [Spektrum der Wissenschaft](http://spektrum.de) immer verschlungen und die Specials Sammel-Ausgaben gekauft, spater dann im Mathe-Studium! Und naturlich Dewdneys Vorganger, [Martin Gardner](http://www.martin-gardner.org) und [Douglas Hofstadter](https://en.wikipedia.org/wiki/Douglas_Hofstadter), Autoren unzahliger Bucher uber mathematisch-informatische Gehirn-Verdreher. Und [Roger Penrose](https://en.wikipedia.org/wiki/Roger_Penrose)! Hach …

Damals habe ich das ein oder andere „Ding" dann an meinem PC in irgend eine Form von Software gegossen, mein großtes Projekt war wohl ein Fraktale-Generator, geschrieben in [Turbo-Pascal](https://de.wikipedia.org/wiki/Turbo_Pascal) mit eigener Fenster-Verwaltung, uberlagerten Menus etc.

### Mal eben auf dem iPad programmieren?

Auch heute faszinieren mich immer noch diese Dinge, aber heute ist das „mal eben"-Programmieren kleiner Programme, die einen mathematischen Zusammenhang visualisieren nicht mehr ganz so einfach. Na, oder sagen wir, es ist schlicht anders geworden. Fruher war es vielleicht „direkter" moglich, mal eben Pixel auf dem Bildschirm an- oder auszuknipsen, dafur hatte man noch keine Smartphones oder Tablets. Heute haben wir diese und nutzen sie immer haufiger als Desktops und Laptops, aber mal eben ein Pixel einschalten geht da auch nicht so leicht, da braucht es schon eine Menge an App-Framework drumherum. Und das will erstmal durchblickt werden.

Aber … genau fur solche Zwecke gibt es da _doch_ etwas, was es uns Mathe-Hacks-Bastlern einfach macht. Zumindest auf einem iOS Gerat: die geniale App [Pythonista](https://itunes.apple.com/de/app/pythonista-3/id1085978097?mt=8&at=10lHSv&ct=blog) vom deutschen Entwickler [Ole Zorn](https://twitter.com/olemoritz)! Innerhalb dieser App kann man namlich in der (ziemlich universellen) Programmiersprache Python durchaus (fast) „mal eben" Pixel setzen.

### Ulam-Spiralen auf dem iPad

Und das habe ich fur das Ulam Spiralen Thema dann mal gemacht. Aber bevor wir zum Programmcode kommen, noch ein bisschen Theorie. Denn bei meiner Recherche zum Thema „Ulam Zahlenspiralen" bin ich vor allem daruber gestolpert ([hier](http://www.naturalnumbers.org/sparticle.html) und [hier](http://www.numberspiral.com/index.html)), dass es noch interessanter ist, statt der rechteckigen Anordnung der Zahlen auf dem Kastchenpapier die naturlichen Zahlen tatsachlich auf einer Spiralkurve anzuorden - und zwar so, dass die Quadratzahlen genau auf der x-Achse zu liegen kommen. Das sieht dann also bei drei „Umdrehungen" so aus:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/numberspiralscreenshot.jpg)

Bei mehr Zahlen und Hervorhebung der Primzahlen sieht das dann z.B. so aus:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/numberspiralscreenshot-1.jpg)

Und wenn man noch mehr Zahlen unterbringt, die Spirale und die Zahlen selbst nicht „malt", bekommt man ein solches Bild:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/numberspiralscreenshot-2.jpg)

Und dann gab es da einen [Herrn Euler](https://de.wikipedia.org/wiki/Leonhard_Euler), der fand mal ein Polynom, bei dem man erst dachte, „Mensch! Das produziert ja lauter Primzahlen!". Das war [das Polynom n²+n+41](http://horstth.de/?p=1849). Das - und beliebige andere Polynom der Form an²+bn+c - lasst sich in meiner Software schon einblenden:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/numberspiralscreenshot-3.jpg)

Man sieht: auf der blauen „Kurve" (eher ein Polygonzug) liegen nur rote Punkte, also Primzahlen - zumindest ununterbrochen 40 Schritte lang (fur n von 0 bis 39).

### Die Software

Was ich in [Pythonista](https://itunes.apple.com/de/app/pythonista-3/id1085978097?mt=8&at=10lHSv&ct=blog) auf einem iPad dazu geschrieben habe, nenne ich „Number Spiral Explorer" und es sieht aktuell so aus:

![](http://musicdiver.com/wordpress/wp-content/uploads/2017/03/img_0211.jpg)

> _Number Spiral Explorer V1.0_

Wer jetzt Lust bekommen hat, mit meinem „Number Spirals Explorer" auf seinem iPad herumzuspielen, der braucht nur [Pythonista](https://itunes.apple.com/de/app/pythonista-3/id1085978097?mt=8&at=10lHSv&ct=blog) und meinen Quellcode.

[Ole himself](https://twitter.com/olemoritz) hat mich [darauf aufmerksam gemacht](https://twitter.com/olemoritz/status/838753638134779908), dass man diesen Dropbox Umweg gar nicht braucht. Das geht viel einfacher, namlich so:

  1. Den Link zum ZIP File unten auf dem iPad in Safari kurz antippen.
  2. „More …" tippen.
  3. „Run Pythonista Script" antippen.
  4. „Import File" antippen.
  5. Den Dialog „File Saved" mit OK bestatigen.
  6. Zu Pythonista wechseln. Hier ist in der Dateiliste jetzt das ZIP File hinzugekommen.
  7. Das ZIP File antippen.
  8. „Extract Archive…" tippen.
  9. Aus dem ZIP File ist ein gleichnamiger Ordner entstanden, der die drei im ZIP File enthaltenen Dateien (NumberSpirals.py, NumberSpirals.pyui, NumberSpiralsSettings.pyui) enthalt.
  10. NumberSpirals.py auswahlen und den Play Button rechts oben tippen. (Wenn man den Play Button gedruckt halt, kann man wahlen, ob das Programm mit Python 2 oder Python 3 laufen soll. Meins lauft mit Python 3.)

Hier alle drei Quelldateien als ZIP Datei: [NumberSpiralExplorer10source](http://musicdiver.com/wordpress/wp-content/uploads/2017/02/NumberSpiralExplorer10source.zip)

Viel Spaß beim Experimentieren! Hab ich euer Interesse geweckt?

Und bitte Nachsicht: ich lerne Python noch … Da sind Fehler bzw. ungeschickte Losungen drin, ich weiß. Auf freundliches Feedback freue ich mich naturlich!
