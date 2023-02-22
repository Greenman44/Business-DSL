# Business-DSL
### Características generales del lenguaje:
 Nuestro trabajo es un lenguaje de dominio específico para la asignatura de Compilación. Tiene como objetivo facilitar la administración y contabilidad de un negocio, ofreciendo herramientas para calcular la sostenibilidad de un negocio y la manipulación y el almacenamiento de sus datos.  
 ### Sintaxis del lenguaje: 
 Es un lenguaje de tipado estático y no orientado a objetos.  
 
 #### Palabras reservadas:
        - business    
        - employed  
        - product  
        - collection  
        - num  
        - bill  
        - void  
        - action  
        - sale  
        - invest  
        - net_sales  
        - gross_margin  
        - gross_profit  
        - expenses  
        - earnings  
        - print  
        - load  
        - save  
        - amount  
        - get  
        - add  
        - del  
        - load  
        - today  
        - last_week  
        - last_month  
        - last_year  
        - price  
        - cost  
        - if    
        - else  
        - foreach   
        - while  
        - from  
        - in  
        - not  
        - and  
        - or
        - dismiss  
        - staff 
        - while  
        - catalog  
        - salary  
 #### Declaración y uso de variables:
 En este lenguaje existen 5 tipos built-in: Business, Collection, Employed, Product, Num. A continuación se muestran ejemplos de su declaración y asignación:
 ```
   num a = 5;
   employed e = {"Jose", salary : 666};
   collection c1 = [e,{"Juan",salary: 300}];
   product p = {"Aceite_no_hay", amount: 15};
   collection c2 = [p, {"Leche_no_hay", amount: 12}];
   businnes = {"laCuevita", c1, c2}; 
```

#### Condicionales:
```python
  num x = 5;
  if( x > 1){

  print : x;

  };

```

#### Bucles:
```python
   num a = 1;
   num b = 2;
   num i = 1;
   
   while(i < 6){
   
      print : a;
      
      i = i + 1;
   };
   
   collection c = [ a , b , i ];
   
   foreach number in c {
   
     print : number;
   
   };
```

#### Funciones built-in:
```python
    business b = load "laCuevita";
   
    product p = { "Azúcar_no_hay"};
   
    b action sale  p price : 40  amount : 5;
   
    b action invest p cost : 10 amount : 5;
   
    num earnings = b get earnings today;
   
    print : earnings;
   
    save b; 
    
```

### Reglas de la Gramática:

Grammar

Rule 0     S' -> Program  
Rule 1     Program -> ListInst  
Rule 2     ListInst -> Instruction END ListInst  
Rule 3     ListInst -> Instruction END  
Rule 4     Instruction -> instance  
Rule 5     Instruction -> SAVE ID  
Rule 6     Instruction -> loop_statements  
Rule 7     Instruction -> IfStatement  
Rule 8     Instruction -> IfStatement ELSE OBRACE ListInst CBRACE  
Rule 9     Instruction -> ID ACTION SALE ID PRICE DPOINT NUMBER AMOUNT DPOINT NUMBER  
Rule 10    Instruction -> ID ACTION SALE ID PRICE DPOINT ID AMOUNT DPOINT ID  
Rule 11    Instruction -> ID ACTION SALE ID PRICE DPOINT operation AMOUNT DPOINT operation  
Rule 12    Instruction -> ID ACTION INVESTS ID COST DPOINT NUMBER AMOUNT DPOINT NUMBER  
Rule 13    Instruction -> ID ACTION INVESTS ID COST DPOINT ID AMOUNT DPOINT ID  
Rule 14    Instruction -> ID ACTION INVESTS ID COST DPOINT operation AMOUNT DPOINT operation  
Rule 15    Instruction -> ID ADD ID  
Rule 16    Instruction -> ID ADD BILL OBRACE NUMBER COMMA DESCRIP CBRACE  
Rule 17    Instruction -> ID ADD BILL OBRACE NUMBER COMMA NAME CBRACE  
Rule 18    Instruction -> ID ADD BILL OBRACE operation COMMA DESCRIP CBRACE  
Rule 19    Instruction -> ID ADD BILL OBRACE operation COMMA NAME CBRACE  
Rule 20    Instruction -> ID ADD BILL OBRACE ID COMMA DESCRIP CBRACE  
Rule 21    Instruction -> ID ADD BILL OBRACE ID COMMA NAME CBRACE  
Rule 22    Instruction -> ID ADD subType  
Rule 23    Instruction -> ID DEL NAME  
Rule 24    Instruction -> ID DEL ID  
Rule 25    Instruction -> ID DISMISS NAME  
Rule 26    Instruction -> ID DISMISS ID  
Rule 27    Instruction -> PRINT DPOINT ID  
Rule 28    Instruction -> funct_call  
Rule 29    Instruction -> DEF TYPE ID OPAREN Params CPAREN OBRACE ListInst CBRACE  
Rule 30    Instruction -> DEF VOID ID OPAREN Params CPAREN OBRACE ListInst CBRACE  
Rule 31    Params -> TYPE ID COMMA Params  
Rule 32    Params -> TYPE ID  
Rule 33    Params -> empty  
Rule 34    loop_statements -> FOREACH ID IN ID OBRACE ListInst CBRACE  
Rule 35    loop_statements -> WHILE OPAREN condition CPAREN OBRACE ListInst CBRACE  
Rule 36    IfStatement -> IF OPAREN condition CPAREN OBRACE ListInst CBRACE  
Rule 37    condition -> bool_expression  
Rule 38    bool_expression -> NOT bool_expression  
Rule 39    bool_expression -> bool_expression AND bool_expression  
Rule 40    bool_expression -> bool_expression OR bool_expression  
Rule 41    bool_expression -> ID EQUAL ID  
Rule 42    bool_expression -> ID LEQ ID  
Rule 43    bool_expression -> ID GEQ ID  
Rule 44    bool_expression -> ID GREATER ID  
Rule 45    bool_expression -> ID LESS ID  
Rule 46    bool_expression -> OPAREN bool_expression CPAREN  
Rule 47    bool_expression -> ID IN ID  
Rule 48    instance -> TYPE ID  
Rule 49    instance -> TYPE ID ASSIGN Assignable  
Rule 50    instance -> ID ASSIGN Assignable  
Rule 51    operation -> operation PLUS operation  
Rule 52    operation -> operation MINUS operation  
Rule 53    operation -> operation DIV operation  
Rule 54    operation -> operation MULT operation  
Rule 55    operation -> ID  
Rule 56    operation -> NUMBER  
Rule 57    operation -> OPAREN operation CPAREN  
Rule 58    Assignable -> subType  
Rule 59    Assignable -> collection  
Rule 60    Assignable -> GET NAME FROM ID  
Rule 61    Assignable -> ID GET METRICS DATE  
Rule 62    Assignable -> LOAD NAME  
Rule 63    Assignable -> operation  
Rule 64    Assignable -> funct_call  
Rule 65    funct_call -> ID OPAREN Argument CPAREN  
Rule 66    Argument -> Assignable COMMA Argument  
Rule 67    Argument -> Assignable  
Rule 68    funct_call -> empty  
Rule 69    Assignable -> GET STAFF FROM ID  
Rule 70    Assignable -> GET CATALOG FROM ID  
Rule 71    Assignable -> GET AMOUNT FROM ID  
Rule 72    Assignable -> ID  
Rule 73    subType -> OBRACE bus CBRACE  
Rule 74    subType -> OBRACE emp CBRACE  
Rule 75    subType -> OBRACE prod CBRACE  
Rule 76    collection -> OBR collection_body CBR  
Rule 77    collection_body -> subType COMMA collection_body  
Rule 78    collection_body -> subType  
Rule 79    collection_body -> empty  
Rule 80    collection_body -> ID COMMA collection_body  
Rule 81    collection_body -> ID  
Rule 82    bus -> NAME COMMA collection COMMA collection  
Rule 83    bus -> NAME COMMA ID COMMA ID  
Rule 84    emp -> NAME COMMA SALARY DPOINT NUMBER  
Rule 85    emp -> NAME COMMA SALARY DPOINT ID  
Rule 86    emp -> NAME COMMA SALARY DPOINT operation  
Rule 87    prod -> NAME COMMA AMOUNT DPOINT NUMBER  
Rule 88    prod -> NAME  
Rule 89    prod -> NAME COMMA AMOUNT DPOINT ID  
Rule 90    prod -> NAME COMMA AMOUNT DPOINT operation  
Rule 91    empty -> < empty >

### Arquitectura del compilador:
Nos auxiliamos de la biblioteca ply.

#### Análisis léxico:
Se encuentra implementada en el archivo "lexer_rules.py".

#### Análisis sintáctico:
Se lleva a cabo en el archivo "parser_rules.py", a partir del cual se construye un AST. Los nodos se encuentran en el archivo "ast_nodes.py" de la carpeta Language.

#### Análisis semántico:
A continuación algunas reglas semánticas del lenguaje:

* Dos variables no pueden tener el mismo nombre.
* La asignación o llamado a una variable solo puede hacerse sobre variables previamemte definidas.
* La condición de una instrucción if o while debe ser una expresión booleana.
* Las operaciones de comparación >, <, >=, <= están definidas para nuestros tipos built-in excepto business y collection.
* La operación == está definida para operandos del mismo tipo.
* Las operaciones +, − están definidaspara nuestros tipos built-in excepto business y collection.
* Los elementos de una colección deben ser del mismo tipo.
* Las funciones built-in: `add`, `del` y `get` se pueden hacer sobre instancias de tipo business y collection.
* Las funciones built-in: `action`, `metrics`,`dismiss` y `add bill` solo se pueden realizar sobre negocios.
* El ciclo foreach se realiza sobre una instancia de tipo collection.  
La implementación se encuentra en el archivo "semanic_checker.py" de la carpeta Language y se utiliza el patrón visitor visto en clase práctica.

#### Ejecución:
Para la ejecución se implementó el patrón visitor en la clase Evaluator en el archivo "evaluator.py" de la carpeta Language.

#### Para correr la aplicación:
Ejecutar "test.py" y como se indica en la consola introducir el nombre del archivo de expresión .bus de la carpeta test que se desea ejecutar. Para ejecutar un archivo creado por usted debe ponerle la extensión .bus y ponerlo en la carpeta test. Luego seguir las instrucciones anteriores.
