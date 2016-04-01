Original Repository: [airbnb/javascript](https://github.com/airbnb/javascript)

# Airbnb JavaScript Style Guide() {

*Ein vernünftiger Ansatz für einen JavaScript-Style-Guide*


## <a name='TOC'>Inhaltsverzeichnis</a>

  1. [Datentypen](#types)
  1. [Objekte](#objects)
  1. [Arrays](#arrays)
  1. [Zeichenketten](#strings)
  1. [Funktionen](#functions)
  1. [Eigenschaften](#properties)
  1. [Variablen](#variables)
  1. [Hoisting](#hoisting)
  1. [Bedingungen und Gleichheit](#conditionals)
  1. [Blöcke](#blocks)
  1. [Kommentare](#comments)
  1. [Whitespace](#whitespace)
  1. [Führende Kommas](#leading-commas)
  1. [Semikolons](#semicolons)
  1. [Typumwandlung](#type-coercion)
  1. [Namenskonventionen](#naming-conventions)
  1. [Zugriffsmethoden](#accessors)
  1. [Konstruktoren](#constructors)
  1. [Events](#events)
  1. [Module](#modules)
  1. [jQuery](#jquery)
  1. [ES5 Kompatibilität](#es5)
  1. [Testing](#testing)
  1. [Performance](#performance)
  1. [Ressourcen](#resources)
  1. [In the Wild](#in-the-wild)
  1. [Übersetzungen](#translation)
  1. [The JavaScript Style Guide Guide](#guide-guide)
  1. [Contributors](#contributors)
  1. [Lizenz](#license)

## <a name='types'>Datentypen</a>

  - **Primitive Typen**: Bei primitiven Datentypen wird immer direkt auf deren Wert zugegriffen.

    + `string`
    + `number`
    + `boolean`
    + `null`
    + `undefined`

    ```javascript
    var foo = 1,
        bar = foo;

    bar = 9;

    console.log(foo, bar); // => 1, 9
    ```
  - **Komplexe Typen**: Bei komplexen Datentypen wird immer auf eine Referenz zugegriffen.

    + `object`
    + `array`
    + `function`

    ```javascript
    var foo = [1, 2],
        bar = foo;

    bar[0] = 9;

    console.log(foo[0], bar[0]); // => 9, 9
    ```

    **[[⬆]](#TOC)**

## <a name='objects'>Objekte</a>

  - Benutze die `literal syntax`, um Objekte zu erzeugen.

    ```javascript
    // schlecht
    var item = new Object();

    // gut
    var item = {};
    ```

  - Benutze keine [reservierten Wörter](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Reserved_Words) für Attribute.

    ```javascript
    // schlecht
    var superman = {
      class: 'superhero',
      default: { clark: 'kent' },
      private: true
    };

    // gut
    var superman = {
      klass: 'superhero',
      defaults: { clark: 'kent' },
      hidden: true
    };
    ```
  - Benutze wenn dann geeignete Synonyme für die reservierten Wörter.
  
    ```javascript
    // schlecht
    var superman = {
      class: 'alien'
    };

    // schlecht
    var superman = {
      klass: 'alien'
    };
    
    // gut
    var superman = {
      type: 'alien'
    };
    ```
    **[[⬆]](#TOC)**

## <a name='arrays'>Arrays</a>

  - Benutze die `literal syntax`, um Arrays zu erzeugen.

    ```javascript
    // schlecht
    var items = new Array();

    // gut
    var items = [];
    ```

  - Wenn du die Array-Länge nicht kennst, benutze `Array#push`.

    ```javascript
    var someStack = [];


    // schlecht
    someStack[someStack.length] = 'abracadabra';

    // gut
    someStack.push('abracadabra');
    ```

  - Wenn du ein Array kopieren möchtest, benutze `Array#slice`. [jsPerf](http://jsperf.com/converting-arguments-to-an-array/7)

    ```javascript
    var len = items.length,
        itemsCopy = [],
        i;

    // schlecht
    for (i = 0; i < len; i++) {
      itemsCopy[i] = items[i];
    }

    // gut
    itemsCopy = items.slice();
    ```
  
  - Wenn du ein Array ähnliches Objekt kopieren möchtest, benutze `Array#slice`.
    
    ```javascript
    function trigger() {
      var args = Array.prototype.slice.call(arguments);
      ...
    }
    ```

    **[[⬆]](#TOC)**


## <a name='strings'>Zeichenketten</a>

  - Benutze einfache Anführungszeichen `''` für Zeichenketten

    ```javascript
    // schlecht
    var name = "Bob Parr";

    // gut
    var name = 'Bob Parr';

    // schlecht
    var fullName = "Bob " + this.lastName;

    // gut
    var fullName = 'Bob ' + this.lastName;
    ```

  - Zeichenketten die länger als 80 Zeichen lang sind, sollten mit Hilfe von `string concatenation` auf mehrere Zeilen aufgeteilt werden.
  - Beachte: Benutzt man `string concatenation` zu oft kann dies die performance beeinträchtigen. [jsPerf](http://jsperf.com/ya-string-concat) & [Discussion](https://github.com/airbnb/javascript/issues/40)

    ```javascript
    // schlecht
    var errorMessage = 'This is a super long error that was thrown because of Batman. When you stop to think about how Batman had anything to do with this, you would get nowhere fast.';

    // schlecht
    var errorMessage = 'This is a super long error that \
    was thrown because of Batman. \
    When you stop to think about \
    how Batman had anything to do \
    with this, you would get nowhere \
    fast.';


    // gut
    var errorMessage = 'This is a super long error that ' +
      'was thrown because of Batman.' +
      'When you stop to think about ' +
      'how Batman had anything to do ' +
      'with this, you would get nowhere ' +
      'fast.';
    ```

  - Wenn man im Programmverlauf eine Zeichenkette dynamisch zusammensetzen muss, sollte man `Array#join` einer `string concatenation` vorziehen. Vorallem für den IE. [jsPerf](http://jsperf.com/string-vs-array-concat/2).

    ```javascript
    var items,
        messages,
        length, i;

    messages = [{
        state: 'success',
        message: 'This one worked.'
    },{
        state: 'success',
        message: 'This one worked as well.'
    },{
        state: 'error',
        message: 'This one did not work.'
    }];

    length = messages.length;

    // schlecht
    function inbox(messages) {
      items = '<ul>';

      for (i = 0; i < length; i++) {
        items += '<li>' + messages[i].message + '</li>';
      }

      return items + '</ul>';
    }

    // gut
    function inbox(messages) {
      items = [];

      for (i = 0; i < length; i++) {
        items[i] = messages[i].message;
      }

      return '<ul><li>' + items.join('</li><li>') + '</li></ul>';
    }
    ```

    **[[⬆]](#TOC)**


## <a name='functions'>Funktionen</a>

  - Funktionsausdrücke:

    ```javascript
    // anonyme Fuktionsausdrücke
    var anonymous = function() {
      return true;
    };

    // benannte Funktionsausdrücke
    var named = function named() {
      return true;
    };

    // direkt ausgeführte Funktionsausdrücke (IIFE)
    (function() {
      console.log('Welcome to the Internet. Please follow me.');
    })();
    ```

  - Vermeide Funktionen in `non-function blocks` zu deklarieren. Anstelle sollte die Funktion einer Variablen zugewiesen werden. Dies hat den Grund, dass die verschiedenen Browser dies unterschiedlich interpretieren.
  - **Beachte:** ECMA-262 definiert einen Block als eine Abfolge/Liste von Statements. Eine Funktion hingegen ist **kein** Statement. [Read ECMA-262's note on this issue](http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf#page=97).

    ```javascript
    // schlecht
    if (currentUser) {
      function test() {
        console.log('Nope.');
      }
    }

    // gut
    if (currentUser) {
      var test = function test() {
        console.log('Yup.');
      };
    }
    ```

  - Benenne einen Parameter nie `arguments`, denn dies wird das `arguments`-Objekt, dass in jedem Funktionskörper zur Verfügung steht, überschreiben.

    ```javascript
    // schlecht
    function nope(name, options, arguments) {
      // ...stuff...
    }

    // gut
    function yup(name, options, args) {
      // ...stuff...
    }
    ```

    **[[⬆]](#TOC)**



## <a name='properties'>Eigenschaften</a>

  - Benutze die Punktnotation, um auf die Eigenschaften eines Objekts zuzugreifen.

    ```javascript
    var luke = {
      jedi: true,
      age: 28
    };

    // schlecht
    var isJedi = luke['jedi'];

    // gut
    var isJedi = luke.jedi;
    ```

  - Benutze die Indexnotation `[]`, um auf die Eigenschaften eines Objekts zuzugreifen, sofern der Index eine Variable ist.

    ```javascript
    var luke = {
      jedi: true,
      age: 28
    };

    function getProp(prop) {
      return luke[prop];
    }

    var isJedi = getProp('jedi');
    ```

    **[[⬆]](#TOC)**


## <a name='variables'>Variablen</a>

  - Benutze immer `var`, um Variablen zu deklarieren. Tut man dies nicht, werden die Variablen im globalen Namespace erzeugt – was nicht gewüscht werden sollte.

    ```javascript
    // schlecht
    superPower = new SuperPower();

    // gut
    var superPower = new SuperPower();
    ```

  - Benutze immer nur ein `var`, um mehrere aufeinanderfolgende Variablen zu deklarieren. Deklariere jede Variable auf einer eigenen Zeile.

    ```javascript
    // schlecht
    var items = getItems();
    var goSportsTeam = true;
    var dragonball = 'z';

    // gut
    var items = getItems(),
        goSportsTeam = true,
        dragonball = 'z';
    ```

  - Deklariere Variablen ohne direkte Zuweisung immer als letztes. Dies ist vorallem hilfreich, wenn man später eine Variable anhand einer zuvor deklarierten Variable initialisieren möchte.

    ```javascript
    // schlecht
    var i, len, dragonball,
        items = getItems(),
        goSportsTeam = true;

    // schlecht
    var i, items = getItems(),
        dragonball,
        goSportsTeam = true,
        len;

    // gut
    var items = getItems(),
        goSportsTeam = true,
        dragonball,
        length,
        i;
    ```

  - Weise den Wert einer Variable, wenn möglich, immer am Anfang des Gültigkeitsbereichs zu. Dies hilft Problemen mit der Variablendeklaration vorzubeugen.

    ```javascript
    // schlecht
    function() {
      test();
      console.log('doing stuff..');

      //..other stuff..

      var name = getName();

      if (name === 'test') {
        return false;
      }

      return name;
    }

    // gut
    function() {
      var name = getName();

      test();
      console.log('doing stuff..');

      //..other stuff..

      if (name === 'test') {
        return false;
      }

      return name;
    }

    // schlecht
    function() {
      var name = getName();

      if (!arguments.length) {
        return false;
      }

      return true;
    }

    // gut
    function() {
      if (!arguments.length) {
        return false;
      }

      var name = getName();

      return true;
    }
    ```

    **[[⬆]](#TOC)**


## <a name='hoisting'>Hoisting</a>

  - Variablendeklarationen werden vom Interpreter an den Beginn eines Gültigkeitbereichs genommen, genannt (`hoisting`). Wohingegen die Zuweisung an der ursprünglichen Stelle bleibt.

    ```javascript
    // Dies wird nicht funktionen (angenommen
    // notDefined ist keine globale Variable)
    function example() {
      console.log(notDefined); // => throws a ReferenceError
    }

    // Wird eine Variable nach seiner ersten
    // Referenzierung deklariert, funktioniert
    // dies dank des hoistings.
    // Beachte aber, dass die Zuweisung von true
    // erst nach der Referenzierung stattfindet.
    function example() {
      console.log(declaredButNotAssigned); // => undefined
      var declaredButNotAssigned = true;
    }

    // Der Interpreter nimmt die Variablendeklaration
    // an den Beginn des Gültigkeitbereichs.
    // So kann das Beispiel wiefolgt umgeschrieben
    // werden:
    function example() {
      var declaredButNotAssigned;
      console.log(declaredButNotAssigned); // => undefined
      declaredButNotAssigned = true;
    }
    ```

  - Anonyme Funktionen `hoisten` ihren Variablennamen, aber nicht die Funktionszuweisung.

    ```javascript
    function example() {
      console.log(anonymous); // => undefined

      anonymous(); // => TypeError anonymous is not a function

      var anonymous = function() {
        console.log('anonymous function expression');
      };
    }
    ```

  - Benannte Funktionen `hoisten` ihren Variablennamen, aber nicht der Funktionsname oder Funktionskörper.

    ```javascript
    function example() {
      console.log(named); // => undefined

      named(); // => TypeError named is not a function

      superPower(); // => ReferenceError superPower is not defined

      var named = function superPower() {
        console.log('Flying');
      };


      // Das gleiche gilt, wenn der Funktionsname
      // derselbe ist, wie der Variablenname
      function example() {
        console.log(named); // => undefined

        named(); // => TypeError named is not a function

        var named = function named() {
          console.log('named');
        };
      }
    }
    ```

  - Funktionsdeklarationen `hoisten` ihren Namen und ihren Funktionskörper.

    ```javascript
    function example() {
      superPower(); // => Flying

      function superPower() {
        console.log('Flying');
      }
    }
    ```

  - Für weitere Informationen siehe hier: [JavaScript Scoping & Hoisting](http://www.adequatelygood.com/2010/2/JavaScript-Scoping-and-Hoisting) by [Ben Cherry](http://www.adequatelygood.com/)

    **[[⬆]](#TOC)**



## <a name='conditionals'>Bedingungen und Gleichheit</a>

  - Ziehe `===` und `!==` gegenüber `==` und `!=` vor.
  - Bedingungsausdrücke werden immer gezwungen der `ToBoolean` Methode ausgewertet zu werden. Diese folgt den folgenden einfachen Grundregeln:

    + **Objekte** werden als **true** gewertet
    + **Undefined** wird als **false** gewertet
    + **Null** wird als **false** gewertet
    + **Booleans** werden als **der Wert des Booleans** gewertet
    + **Zahlen** werden als **false** gewertet sofern **+0, -0, or NaN**, ansonsten als **true**
    + **Zeichenketten** werden als **false** gewertet, sofern sie leer ist `''`, ansonsten als **true**

    ```javascript
    if ([0]) {
      // true
      // Arrays sind Objekte und Objekte werden als true ausgewertet
    }
    ```

  - Benutze `shortcuts`

    ```javascript
    // schlecht
    if (name !== '') {
      // ...stuff...
    }

    // gut
    if (name) {
      // ...stuff...
    }

    // schlecht
    if (collection.length > 0) {
      // ...stuff...
    }

    // gut
    if (collection.length) {
      // ...stuff...
    }
    ```

  - Für weitere Informationen siehe hier: [Truth Equality and JavaScript](http://javascriptweblog.wordpress.com/2011/02/07/truth-equality-and-javascript/#more-2108) by Angus Croll

    **[[⬆]](#TOC)**


## <a name='blocks'>Blöcke</a>

  - Benutze geschweifte Klammern für alle mehrzeiligen Blöcke.

    ```javascript
    // schlecht
    if (test)
      return false;

    // gut
    if (test) return false;

    // gut
    if (test) {
      return false;
    }

    // schlecht
    function() { return false; }

    // gut
    function() {
      return false;
    }
    ```

    **[[⬆]](#TOC)**


## <a name='comments'>Kommentare</a>

  - Benutze `/** ... */` für mehrzeilige Kommentare. Daran kann eine Beschreibung, eine Typendefinition und Werte für alle Parameter und den Rückgabewert angegeben werden.

    ```javascript
    // schlecht
    // make() returns a new element
    // based on the passed in tag name
    //
    // @param <String> tag
    // @return <Element> element
    function make(tag) {

      // ...stuff...

      return element;
    }

    // gut
    /**
     * make() returns a new element
     * based on the passed in tag name
     *
     * @param <String> tag
     * @return <Element> element
     */
    function make(tag) {

      // ...stuff...

      return element;
    }
    ```

  - Benutze `//` für einzeilige Kommentare. Platziere den Kommentar auf einer separaten Zeile oberhalb der beschriebenen Zeile. Vor den Kommentar kommt eine Leerzeile.

    ```javascript
    // schlecht
    var active = true;  // is current tab

    // gut
    // is current tab
    var active = true;

    // schlecht
    function getType() {
      console.log('fetching type...');
      // set the default type to 'no type'
      var type = this._type || 'no type';

      return type;
    }

    // gut
    function getType() {
      console.log('fetching type...');

      // set the default type to 'no type'
      var type = this._type || 'no type';

      return type;
    }
    ```
  - Benutze wenn möglich die Prefixe `FIXME` oder `TODO` für die Kommentare. Sie erleichtert die Arbeit für andere Entwickler und sich selbst. So kann man Codestellen, die eine Verbesserung brauchen oder noch nicht implementiert sind, ohne grosse Mühe auffinden.
  - Benutze `FIXME` um Probleme zu markieren
    
    ```javascript
    function Calculator() {
      
      // FIXME: brauche eine globale Variable
      total = 0;

      return this;
    }
    ```
  
  - Benutze `TODO` um Hinweise für mögliche Lösungen für ein bestimmtes Problem zu geben, welches noch behoben werden muss.
    
    ```javascript
    function Calculator() {      

      // FIXME: dieses Member sollte über einen Parameter konfigurierbar sein
      this.total = 0;

      return this;
    }
    ```

    **[[⬆]](#TOC)**


## <a name='whitespace'>Whitespace</a>

  - Benutze weiche Tabulatoren (`soft tabs`) mit 2 Leerzeichen.

    ```javascript
    // schlecht
    function() {
    ∙∙∙∙var name;
    }

    // schlecht
    function() {
    ∙var name;
    }

    // gut
    function() {
    ∙∙var name;
    }
    ```
  - Platziere ein Leerzeichen vor einer öffnenden Klammer.

    ```javascript
    // schlecht
    function test(){
      console.log('test');
    }

    // gut
    function test() {
      console.log('test');
    }

    // schlecht
    dog.set('attr',{
      age: '1 year',
      breed: 'Bernese Mountain Dog'
    });

    // gut
    dog.set('attr', {
      age: '1 year',
      breed: 'Bernese Mountain Dog'
    });
    ```
  - Platziere eine Leerzeile an das Ende der Datei.

    ```javascript
    // schlecht
    (function(global) {
      // ...stuff...
    })(this);
    ```

    ```javascript
    // gut
    (function(global) {
      // ...stuff...
    })(this);

    ```

  - Rücke bei langen Methodenverkettungen ein.

    ```javascript
    // schlecht
    $('#items').find('.selected').highlight().end().find('.open').updateCount();

    // gut
    $('#items')
      .find('.selected')
        .highlight()
        .end()
      .find('.open')
        .updateCount();

    // schlecht
    var leds = stage.selectAll('.led').data(data).enter().append("svg:svg").class('led', true)
        .attr('width',  (radius + margin) * 2).append("svg:g")
        .attr("transform", "translate(" + (radius + margin) + "," + (radius + margin) + ")")
        .call(tron.led);

    // gut
    var leds = stage.selectAll('.led')
        .data(data)
      .enter().append("svg:svg")
        .class('led', true)
        .attr('width',  (radius + margin) * 2)
      .append("svg:g")
        .attr("transform", "translate(" + (radius + margin) + "," + (radius + margin) + ")")
        .call(tron.led);
    ```

    **[[⬆]](#TOC)**


## <a name='leading-commas'>Führende Kommas</a>

  - Führende Kommas: **Nein.**

    ```javascript
    // schlecht
    var once
      , upon
      , aTime;

    // gut
    var once,
        upon,
        aTime;

    // schlecht
    var hero = {
        firstName: 'Bob'
      , lastName: 'Parr'
      , heroName: 'Mr. Incredible'
      , superPower: 'strength'
    };

    // gut
    var hero = {
      firstName: 'Bob',
      lastName: 'Parr',
      heroName: 'Mr. Incredible',
      superPower: 'strength'
    };
    ```
    
  - Zusätzliche Kommas am Ende einer Aufzählung: **Nein**. Denn dies kann zu Problemen mit IE6/7 und IE9 führen. Auch kann es in einigen Implementation on ES3 dazu führen, dass die Länge des Arrays um eins zu gross wird. Was in ES5 beschrieben wurde: [source](http://es5.github.io/#D)
    > Edition 5 clarifies the fact that a trailing comma at the end of an ArrayInitialiser does not add to the length of the array. This is not a semantic change from Edition 3 but some implementations may have previously misinterpreted this.

    ```javascript
    // schlecht
    var hero = {
      firstName: 'Kevin',
      lastName: 'Flynn',
    };

    var heroes = [
      'Batman',
      'Superman',
    ];

    // gut
    var hero = {
      firstName: 'Kevin',
      lastName: 'Flynn'
    };

    var heroes = [
      'Batman',
      'Superman'
    ];
    ```

    **[[⬆]](#TOC)**


## <a name='semicolons'>Semikolons</a>

  - **Ja.**

    ```javascript
    // schlecht
    (function() {
      var name = 'Skywalker'
      return name
    })()

    // gut
    (function() {
      var name = 'Skywalker';
      return name;
    })();

    // gut
    ;(function() {
      var name = 'Skywalker';
      return name;
    })();
    ```

    **[[⬆]](#TOC)**


## <a name='type-coercion'>Typumwandlung</a>

  - Benutze `type coercion` am Anfang eines Statements.
  - Bei Zeichenketten:

    ```javascript
    //  => this.reviewScore = 9;

    // schlecht
    var totalScore = this.reviewScore + '';

    // gut
    var totalScore = '' + this.reviewScore;

    // schlecht
    var totalScore = '' + this.reviewScore + ' total score';

    // gut
    var totalScore = this.reviewScore + ' total score';
    ```

  - Benutze immer `parseInt` für Zahlen und gebe immer eine Basis für die Typumwandlung an.
  - Wenn man aus [Performancegründen](http://jsperf.com/coercion-vs-casting/3) kein `parseInt` verwenden will und ein `Bitshifting` benutzt, sollte man einen Kommentar hinterlassen, wieso dies gemacht wurde.

    ```javascript
    var inputValue = '4';

    // schlecht
    var val = new Number(inputValue);

    // schlecht
    var val = +inputValue;

    // schlecht
    var val = inputValue >> 0;

    // schlecht
    var val = parseInt(inputValue);

    // gut
    var val = Number(inputValue);

    // gut
    var val = parseInt(inputValue, 10);

    // gut
    /**
     * parseInt was the reason my code was slow.
     * Bitshifting the String to coerce it to a
     * Number made it a lot faster.
     */
    var val = inputValue >> 0;
    ```

  - Bei Booleans:

    ```javascript
    var age = 0;

    // schlecht
    var hasAge = new Boolean(age);

    // gut
    var hasAge = Boolean(age);

    // gut
    var hasAge = !!age;
    ```

    **[[⬆]](#TOC)**


## <a name='naming-conventions'>Namenskonventionen</a>

  - Benutze keine `einzeichigen` Namen. Die Namen sollten beschreibend sein.

    ```javascript
    // schlecht
    function q() {
      // ...stuff...
    }

    // gut
    function query() {
      // ..stuff..
    }
    ```

  - Benutze `camelCase`, um Objekte, Funktionen und Instanzen zu benennen.

    ```javascript
    // schlecht
    var OBJEcttsssss = {};
    var this_is_my_object = {};
    var this-is-my-object = {};
    function c() {};
    var u = new user({
      name: 'Bob Parr'
    });

    // gut
    var thisIsMyObject = {};
    function thisIsMyFunction() {};
    var user = new User({
      name: 'Bob Parr'
    });
    ```

  - Benutze `PascalCase`, um Klassen und Konstrukturen zu benennen.

    ```javascript
    // schlecht
    function user(options) {
      this.name = options.name;
    }

    var bad = new user({
      name: 'nope'
    });

    // gut
    function User(options) {
      this.name = options.name;
    }

    var good = new User({
      name: 'yup'
    });
    ```

  - Benutze führende Untenstriche `_`, um private Eigenschaften zu benennen.

    ```javascript
    // schlecht
    this.__firstName__ = 'Panda';
    this.firstName_ = 'Panda';

    // gut
    this._firstName = 'Panda';
    ```

  - Um eine Referenz an `this` zuzuweisen, benutze `_this`.

    ```javascript
    // schlecht
    function() {
      var self = this;
      return function() {
        console.log(self);
      };
    }

    // schlecht
    function() {
      var that = this;
      return function() {
        console.log(that);
      };
    }

    // gut
    function() {
      var _this = this;
      return function() {
        console.log(_this);
      };
    }
    ```

  - Gib deinen Funktionen einen Namen. Dies ist hilfreich für den `stack trace`.

    ```javascript
    // schlecht
    var log = function(msg) {
      console.log(msg);
    };

    // gut
    var log = function log(msg) {
      console.log(msg);
    };
    ```

    **[[⬆]](#TOC)**


## <a name='accessors'>Zugriffsmethoden</a>

  - Zugriffsmethoden für Objekteigenschaften sind nicht von Nöten.
  - Macht man dennoch Zugriffsmethoden, benutze `getVal()` und `setVal('hello')`.

    ```javascript
    // schlecht
    dragon.age();

    // gut
    dragon.getAge();

    // schlecht
    dragon.age(25);

    // gut
    dragon.setAge(25);
    ```

  - Wenn die Eigenschaft ein Boolean ist, benutze `isVal()` oder `hasVal()`.

    ```javascript
    // schlecht
    if (!dragon.age()) {
      return false;
    }

    // gut
    if (!dragon.hasAge()) {
      return false;
    }
    ```

  - Es ist in Ordnung `get()`- und `set()`-Methoden zu erstellen, aber sei konsistent.

    ```javascript
    function Jedi(options) {
      options || (options = {});
      var lightsaber = options.lightsaber || 'blue';
      this.set('lightsaber', lightsaber);
    }

    Jedi.prototype.set = function(key, val) {
      this[key] = val;
    };

    Jedi.prototype.get = function(key) {
      return this[key];
    };
    ```

    **[[⬆]](#TOC)**


## <a name='constructors'>Konstruktoren</a>

  - Weise die Methoden dem `prototype` des Objektes zu, anstelle den `prototype` mit einem neuen Objekt zu überschreiben. Wenn man den `prototype` überschreibt wird eine Vererbung unmöglich, denn damit wird die Basis überschrieben!

    ```javascript
    function Jedi() {
      console.log('new jedi');
    }

    // schlecht
    Jedi.prototype = {
      fight: function fight() {
        console.log('fighting');
      },

      block: function block() {
        console.log('blocking');
      }
    };

    // gut
    Jedi.prototype.fight = function fight() {
      console.log('fighting');
    };

    Jedi.prototype.block = function block() {
      console.log('blocking');
    };
    ```

  - Methoden können `this` zurückgeben, um eine Methodenverkettung zu ermöglichen.

    ```javascript
    // schlecht
    Jedi.prototype.jump = function() {
      this.jumping = true;
      return true;
    };

    Jedi.prototype.setHeight = function(height) {
      this.height = height;
    };

    var luke = new Jedi();
    luke.jump(); // => true
    luke.setHeight(20) // => undefined

    // gut
    Jedi.prototype.jump = function() {
      this.jumping = true;
      return this;
    };

    Jedi.prototype.setHeight = function(height) {
      this.height = height;
      return this;
    };

    var luke = new Jedi();

    luke.jump()
      .setHeight(20);
    ```


  - Es ist in Ordnung eine eigene `toString()`-Methode zu schreiben, aber man sollte sicherstellen, dass diese korrekt funktioniert und keine Nebeneffekte hat.

    ```javascript
    function Jedi(options) {
      options || (options = {});
      this.name = options.name || 'no name';
    }

    Jedi.prototype.getName = function getName() {
      return this.name;
    };

    Jedi.prototype.toString = function toString() {
      return 'Jedi - ' + this.getName();
    };
    ```

    **[[⬆]](#TOC)**
    
    
## <a name='events'>Events</a>

  - Wenn man Daten zu einem Event hinzufügen möchte, dann soll man einen `hash` einem `raw value` vorziehen. Denn es lässt einen einfach weitere Parameter hinzuzufügen ohne den Eventhandler für den existieren Parameter zu bearbeiten.
    
    ```javascript
    // schlecht
    $(this).trigger('listingUpdated', listing.id);

    ...

    $(this).on('listingUpdated', function(e, listingId) {
      // do something with listingId
    });
    ```
    
    Bevorzuge:
    
    ```javascript
    // gut
    $(this).trigger('listingUpdated', { listingId : listing.id });

    ...
    
    $(this).on('listingUpdated', function(e, data) {
      // do something with data.listingId
    });
    ```
    
    **[[⬆]](#TOC)**
    

## <a name='modules'>Module</a>

  - Ein Modul sollte mit einem `!` beginnen. Dies stellt sicher, dass wenn in einem Modul das abschliessende Semikolon vergessen wurde, keine Fehler entstehen, wenn die Scripte zusammengeschnitten werden.
  - Eine Datei sollte in `camelCase` benannt sein, in einem Ordner mit dem selben Namen liegen und dem Namen entsprechen mit dem es exportiert wird.
  - Benutze eine Methode `noConflict()`, welche das exportierte Modul auf die vorhergehende Version setzt und diese zurück gibt.
  - Deklariere immer `'use strict';` am Anfang des Moduls.

    ```javascript
    // fancyInput/fancyInput.js

    !function(global) {
      'use strict';

      var previousFancyInput = global.FancyInput;

      function FancyInput(options) {
        this.options = options || {};
      }

      FancyInput.noConflict = function noConflict() {
        global.FancyInput = previousFancyInput;
        return FancyInput;
      };

      global.FancyInput = FancyInput;
    }(this);
    ```

    **[[⬆]](#TOC)**


## <a name='jquery'>jQuery</a>

  - Stelle allen jQuery-Objektvariablen ein `$` voran.

    ```javascript
    // schlecht
    var sidebar = $('.sidebar');

    // gut
    var $sidebar = $('.sidebar');
    ```

  - Speichere `jQuery lookups`, sofern sie mehrmals gebraucht werden.

    ```javascript
    // schlecht
    function setSidebar() {
      $('.sidebar').hide();

      // ...stuff...

      $('.sidebar').css({
        'background-color': 'pink'
      });
    }

    // gut
    function setSidebar() {
      var $sidebar = $('.sidebar');
      $sidebar.hide();

      // ...stuff...

      $sidebar.css({
        'background-color': 'pink'
      });
    }
    ```

  - Für DOM-Abfragen benutze `Cascading`: `$('.sidebar ul')` oder parent > child `$('.sidebar > .ul')`. [jsPerf](http://jsperf.com/jquery-find-vs-context-sel/16)
  - Benutze `find` mit `scoped jQuery object queries`

    ```javascript
    // schlecht
    $('.sidebar', 'ul').hide();

    // schlecht
    $('.sidebar').find('ul').hide();

    // gut
    $('.sidebar ul').hide();

    // gut
    $('.sidebar > ul').hide();

    // gut (langsamer)
    $sidebar.find('ul');

    // gut (schneller)
    $($sidebar[0]).find('ul');
    ```

    **[[⬆]](#TOC)**


## <a name='es5'>ECMAScript 5 Kompatibilität</a>

  - Verweis auf [Kangax](https://twitter.com/kangax/)'s ES5 [Kompatibilitätstabelle](http://kangax.github.com/es5-compat-table/)

  **[[⬆]](#TOC)**


## <a name='testing'>Testing</a>

  - **Ja.**

    ```javascript
    function() {
      return true;
    }
    ```

    **[[⬆]](#TOC)**


## <a name='performance'>Performance</a>

  - [On Layout & Web Performance](http://kellegous.com/j/2013/01/26/layout-performance/)
  - [String vs Array Concat](http://jsperf.com/string-vs-array-concat/2)
  - [Try/Catch Cost In a Loop](http://jsperf.com/try-catch-in-loop-cost)
  - [Bang Function](http://jsperf.com/bang-function)
  - [jQuery Find vs Context, Selector](http://jsperf.com/jquery-find-vs-context-sel/13)
  - [innerHTML vs textContent for script text](http://jsperf.com/innerhtml-vs-textcontent-for-script-text)
  - [Long String Concatenation](http://jsperf.com/ya-string-concat)
  - Loading...

  **[[⬆]](#TOC)**


## <a name='resources'>Ressourcen</a>


**Lese dieses**

  - [Annotated ECMAScript 5.1](http://es5.github.com/)

**Andere Styleguides**

  - [Google JavaScript Style Guide](http://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml)
  - [jQuery Core Style Guidelines](http://docs.jquery.com/JQuery_Core_Style_Guidelines)
  - [Principles of Writing Consistent, Idiomatic JavaScript](https://github.com/rwldrn/idiomatic.js/)

**Andere Styles**

  - [Naming this in nested functions](https://gist.github.com/4135065) - Christian Johansen
  - [Conditional Callbacks](https://github.com/airbnb/javascript/issues/52)
  - [Popular JavaScript Coding Conventions on Github](http://sideeffect.kr/popularconvention/#javascript)

**Bücher**

  - [JavaScript: The Good Parts](http://www.amazon.com/JavaScript-Good-Parts-Douglas-Crockford/dp/0596517742) - Douglas Crockford
  - [JavaScript Patterns](http://www.amazon.com/JavaScript-Patterns-Stoyan-Stefanov/dp/0596806752) - Stoyan Stefanov
  - [Pro JavaScript Design Patterns](http://www.amazon.com/JavaScript-Design-Patterns-Recipes-Problem-Solution/dp/159059908X)  - Ross Harmes and Dustin Diaz
  - [High Performance Web Sites: Essential Knowledge for Front-End Engineers](http://www.amazon.com/High-Performance-Web-Sites-Essential/dp/0596529309) - Steve Souders
  - [Maintainable JavaScript](http://www.amazon.com/Maintainable-JavaScript-Nicholas-C-Zakas/dp/1449327680) - Nicholas C. Zakas
  - [JavaScript Web Applications](http://www.amazon.com/JavaScript-Web-Applications-Alex-MacCaw/dp/144930351X) - Alex MacCaw
  - [Pro JavaScript Techniques](http://www.amazon.com/Pro-JavaScript-Techniques-John-Resig/dp/1590597273) - John Resig
  - [Smashing Node.js: JavaScript Everywhere](http://www.amazon.com/Smashing-Node-js-JavaScript-Everywhere-Magazine/dp/1119962595) - Guillermo Rauch
  - [Secrets of the JavaScript Ninja](http://www.amazon.com/Secrets-JavaScript-Ninja-John-Resig/dp/193398869X) - John Resig and Bear Bibeault
  - [Human JavaScript](http://humanjavascript.com/) - Henrik Joreteg
  - [Superhero.js](http://superherojs.com/) - Kim Joar Bekkelund, Mads Mobæk, & Olav Bjorkoy
  - [JSBooks](http://jsbooks.revolunet.com/)

**Blogs**

  - [DailyJS](http://dailyjs.com/)
  - [JavaScript Weekly](http://javascriptweekly.com/)
  - [JavaScript, JavaScript...](http://javascriptweblog.wordpress.com/)
  - [Bocoup Weblog](http://weblog.bocoup.com/)
  - [Adequately Good](http://www.adequatelygood.com/)
  - [NCZOnline](http://www.nczonline.net/)
  - [Perfection Kills](http://perfectionkills.com/)
  - [Ben Alman](http://benalman.com/)
  - [Dmitry Baranovskiy](http://dmitry.baranovskiy.com/)
  - [Dustin Diaz](http://dustindiaz.com/)
  - [nettuts](http://net.tutsplus.com/?s=javascript)

  **[[⬆]](#TOC)**

## <a name='in-the-wild'>In the Wild</a>

  Dies ist eine Liste von Organisationen, welche diesen Style Guide benutzen. Sende uns einen `Pull request` oder öffne einen `issue` und wir werden dich der Liste hinzufügen.

  - **Aan Zee**: [AanZee/javascript](https://github.com/AanZee/javascript)
  - **Airbnb**: [airbnb/javascript](https://github.com/airbnb/javascript)
  - **American Insitutes for Research**: [AIRAST/javascript](https://github.com/AIRAST/javascript)
  - **Compass Learning**: [compasslearning/javascript-style-guide](https://github.com/compasslearning/javascript-style-guide)
  - **ExactTarget**: [ExactTarget/javascript](https://github.com/ExactTarget/javascript)
  - **Gawker Media**: [gawkermedia/javascript](https://github.com/gawkermedia/javascript)
  - **GeneralElectric**: [GeneralElectric/javascript](https://github.com/GeneralElectric/javascript)
  - **GoodData**: [gooddata/gdc-js-style](https://github.com/gooddata/gdc-js-style)
  - **Grooveshark**: [grooveshark/javascript](https://github.com/grooveshark/javascript)
  - **How About We**: [howaboutwe/javascript](https://github.com/howaboutwe/javascript)
  - **Mighty Spring**: [mightyspring/javascript](https://github.com/mightyspring/javascript)
  - **MinnPost**: [MinnPost/javascript](https://github.com/MinnPost/javascript)
  - **ModCloth**: [modcloth/javascript](https://github.com/modcloth/javascript)
  - **National Geographic**: [natgeo/javascript](https://github.com/natgeo/javascript)
  - **National Park Service**: [nationalparkservice/javascript](https://github.com/nationalparkservice/javascript)
  - **Razorfish**: [razorfish/javascript-style-guide](https://github.com/razorfish/javascript-style-guide)
  - **Shutterfly**: [shutterfly/javascript](https://github.com/shutterfly/javascript)
  - **Userify**: [userify/javascript](https://github.com/userify/javascript)
  - **Zillow**: [zillow/javascript](https://github.com/zillow/javascript)
  - **ZocDoc**: [ZocDoc/javascript](https://github.com/ZocDoc/javascript)

  **[[⬆]](#TOC)**

## <a name='translation'>Übersetzungen</a>

  Dieser Styleguide ist in den folgenden Sprachen erhältlich:

  - :en: **Englisch**: [airbnb/javascript](https://github.com/airbnb/javascript)
  - :jp: **Japanisch**: [mitsuruog/javacript-style-guide](https://github.com/mitsuruog/javacript-style-guide)
  - :br: **Portugisisch**: [armoucar/javascript-style-guide](https://github.com/armoucar/javascript-style-guide)
  - :cn: **Chinesisch**: [adamlu/javascript-style-guide](https://github.com/adamlu/javascript-style-guide)
  - :es: **Spanisch**: [paolocarrasco/javascript-style-guide](https://github.com/paolocarrasco/javascript-style-guide)
  - :kr: **Koreanisch**: [tipjs/javascript-style-guide](https://github.com/tipjs/javascript-style-guide)
  - :fr: **Französisch**: [nmussy/javascript-style-guide](https://github.com/nmussy/javascript-style-guide)


  **[[⬆]](#TOC)**

## <a name='guide-guide'>The JavaScript Style Guide Guide</a>

  - [Reference](//github.com/airbnb/javascript/wiki/The-JavaScript-Style-Guide-Guide)

  **[[⬆]](#TOC)**

## <a name='authors'>Contributors</a>

  - [View Contributors](https://github.com/airbnb/javascript/graphs/contributors)

  **[[⬆]](#TOC)**


## <a name='license'>Lizenz</a>

(The MIT License)

Copyright (c) 2012 Airbnb

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

**[[⬆]](#TOC)**

# };
