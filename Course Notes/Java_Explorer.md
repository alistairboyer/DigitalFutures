# Java Explorer

_Alistair Boyer_

Notes on the <a href="https://learn.oracle.com/ols/learning-path/java-explorer/88323/79726">Oracle Java Explorer Course</a>

## Java
> Write once: run anywhere

> Runs on billions of devices

- `code` compiled __once__ into `bytecode`
- `bytecode` executed in `JVM` - emulates __all types__ of underlying hardware  
- platform independant
- __strongly__ typed: need to define type when variable first used
- object-oriented

## Object-Oriented Programming (OOP)


### Origins of Programming
- Punch cards
- Languages: Pascal, FORTRAN for engineering
- Code written at once and all in one block


### Object Oriented Programming History
- __Smalltalk__, the first _OOP_ language [[https://en.wikipedia.org/wiki/Smalltalk](https://en.wikipedia.org/wiki/Smalltalk)]
- Created by __Alan Kay__ at Xerox as reaction to monolithic computing as a "concept" of individual computing
- Package code into cells, __mimic biology__
- Self contained, easy to distribute, easy to extend
- Focus on simple __communication__ between code "cells" as design principle
- Simple syntax - fits on a punch card, tested at school  
- Inspired by generalising Simula [[https://en.wikipedia.org/wiki/Simula](https://en.wikipedia.org/wiki/Simula)]
- Conceived a "dynabook" concept, precursor to todays tablets
- Free open source version: __Squeak__ [[https://squeak.org/](https://squeak.org/)]


### Practical Considerations
- Benefits
  - Easy to maintain
  - Easy to extend
  - Minimise side effects
  - Conceptually straightforward, logically group common features with objects
- Drawbacks
  - Originally harder to implement originally
  - More verbose
  - More overhead
  - More complexity for garbage collection

- Most of the drawbacks are not relevant in the context of mature OOP and fast modern processors.


### OOP Features
- __encapsulation__: validate and protect data by restricting the scope of variable access; reduces dependency and side effects
- __extend__: elaborate on features in higher level parent classes
- __inheritance__: create more specific classes that inherit base features from their parent classes
- __polymorphism__: different objects with personalised implementations of methods with the same name
- __abstraction__: specify overall design requirements without the details of implementation
- __interface__: define expected common behaviours (e.g. `print()`) as outward facing information; can not be instantiated

## Definitions
- __late binding__, or dynamic binding: looking up arguments at run time for e.g. polymorphism (instead of compile time)
- __enum__: enumeration
- __generics__: type info for compilers










## Java Editions
- __Card__: secure, for smart cards
- __ME__: Micro Edition
- __SE__: Standard Edition
- __MP__: Microprofile, microservices
- __EE__: Enterprise Edition, servlets, webservices, websites


## Java in Enterprise
- Webservices expose code on web
- JAX-WS for SOAP
- JAX-RS for REST
- EE applications run on server - weblogic, tomcat
- Oracle cloud - supports most languages, databases and tools
- Handle security, etc..

# Code

## A Java Program
- Set of instructions that can be converted into machine code
- Machine code selects operations built in the CPU
<br /><br />
- `.java` files contain text program code
- `.class` files contain compiled bytecode for the JVM
<br /><br />
- `javac x.java` runs the java compiler
- `java x` runs the compiled bytecode on the JVM
<br /><br />
- classes are stored in __files__
- packages are stored in __folders__
<br /><br />
- entry point is `public static void main(String[] args) {}`
- `args` are command line arguments



## Project Design

### Design Phases
- __abstraction__: _analysis phase_
- __polymorphism__: _design phase_
- __interface__: _design phase_
- __inheritence__: _design phase_
- __encapsulation__: _coding phase_


### Unified Modelling Language (UML)
- Design focussed on use case
- Class diagram, behaviours, attributes and relations
  - Rounded rectangle
  - Top section: class name
  - Middle section: variables [ name : String ]
  - Bottom section: methods [ getSize() : int ]
- Activity: flow of control
- Seauence: passing of data, invocations
- State: state info
- Deployment

## Java Standard Classes
- Array: indexing multiple of the same type
- Collection: sets, lists, queues, etc..
- Concurrency: multithreaded applications
- IO: files
- JDBC: connect to database for e.g. SQL, JPA links Java objects to db data
- Stream: apply lambda, map, filter, foreach, etc. to collection of objects
- String: text

## Variables
- strong typed - declare type upon creation
- preference for `camelCase`
- use descriptive names


- `constant`: can not be changed
- `static`: class variables
- `final`: can not be changed in subclass
- `public`: can be accessed by anything
- `private`: can only be accessed by the object
- `protected`: can only be accessed by the object and its subclasses
- `abstract`: can not be instantiated only extended


Variable Location
- Stack
  - Primitive variables
  - Object references
  - Array references
- Heap
  - Objects
  - Arrays


### Primitive Types
```java
// integer primatives, default 0
byte i8 = -17;  // 8 bit: -128 to 127
short i16 = 1;  // 16 bit
int i32 = 1;  // 32 bit
long i64 = 98_645_673;  // 64 bit

// float primatives, default 0.0
float f32 = 0.0005; // 32 bit
double d64 = -5.6;  // 64 bit

// char primative, default \u0000
char c16 = '@'; // 16 bit unicode

// boolean primative, default false
boolean b1 = true;  // 1 bit


// declare final to make read only
final int MOON_LANDING_YEAR = 1969;
```

Operators
- order of operation : `()` > `++` `--` > `*` `/` > `+` `-`

```java
ints     +  -  *  /(floordiv)  +=  ++ ...
floats   +  -  *  /(truediv)   +=  ++ ...
```


### String
```java
// String object, defaults to null
String s = "this is a string!";

// can't use comparison operators, need to use methods
boolean eq = str1.equals(str2);
boolean eqIC = str1.equalsIgnoreCase(str2);
String str1str2 = str1.concat(str2);
String str1str2 = str1 + str1; // alternative to concat
String str1trim = str1.trim()
String str1LC = str1.toLowerCase();
int idx = str1.indexOf("c");
int len = str1.length();

// automated String type conversion
String s5 = s1 + (99) + s2;
```

### Array
```java
// initialise to null objects then assign elements
int[] arr = new int[3];
arr[0] = 0;
arr[1] = 1;
arr[2] = 2;

// initialise to defined objects
String[] items = {"zeroth", "first", "second"};

// array length
int len = arr.length;
```

## OOP Structure

- Module - high level code aggregation _that can contain_:
  - Package - intermediate code aggregation _that can contain_:
    - Class - definition of an object, its behatiour and attributes; each class is a single file
    - Enum - collection of enumerated labels

### Packages and Classes
```java
package animals.domestic; // represents a folder

// class full reference is animals.domestic.Dog
public class Dog {

    // overloading - different code executed for different signatures
    // signatures - combination of function or class name and order and count of parameter types
    Dog() {}
    Dog(String name) {name=name;}
    Dog(String name, String breed) {name=name; breed=breed;}
    
    // class variable
    public static const String animal = "Dog";

    // instance variables
    String name;
    String breed;
    
    // functions
    @ Override // note for compiler
    public void bark() {

        // command line output
        System.out.println("woof");
        
    }
    
    // lambda expressions
    e -> e.doFunction();

}


public class Labrador extends Dog {

    public static const String breed = "Labrador";

    public void bark() {
        System.out.println("woof");
        super.back();  // woof woof
    }

}
```

interfaces
```java
public inteface Printable {
    abstract void print(Printer printer);
}

public class PDF implements Printable {
    public class print(Printer printer) {
        printer.print(this.content);
    }
}

public static main(String[] args) {
    Printable[] print_queue[3];
    print_queue[0] = new PDF;
    print_queue[1] = new WordDocument;
    print_queue[2] = new Photograph;
    for (Printable p: print_queue) {
        p.print();
    }
}

```

objects - create a new instance of a class
```java
Dog rover = new Dog();
```


## Flow Control

### Conditionals
```java
// logic
true || false;  // OR
true && false;  // AND
!true;          // NOT

// if
if (condition1 || condition2) {
    // run if condition1 or condition2
} else {
    // run if not condition1 and no condition2
}

// ternary operator
int x = (condition) ? 1 : 2;

// switch
switch (condition) {
    case 1:
        // run if condition is 1
        break;
    case 2:
        // run if condition is 2
        break;
    default:
        // run if no other match
        break;
}
```

### Loops
```java
for (int i=0; i<arr.length; i++) {
    obj = arr[i];
    // loop
}

for (Obj obj: arr_of_Obj) {
    // loop
}

while (condition) {
    // loop
}

do {
    // loop at least once
} while (condition)

break;  // break out of loop
continue;  // skip rest of code in current loop and continue
```

### Exceptions
```java
try {
    // code
} catch (Exception e) {
    // code run on error
}

throw new Exception("Exception information");
// code must catch Exception OR include declaraion that it throws Exception
```

## Overview and Environment Setup for Java Explorer
- Java Explorer Leads to Java SE 11 Complete Course
- Course environment: OCI VM Compute Instance
  - JDK 11
  - Netbeans
  - Free trial account
- JShell
  - Read-Evauate-Print-Loop [REPL] command line tool

# Java Explorer Badge
<img src="JavaExplorer.jpeg" alt="Java Explorer Badge" />

