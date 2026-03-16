"""
=============================================================================
COMPLETE OOP CONCEPTS IN PYTHON — Detailed Reference
=============================================================================
"""


# =============================================================================
# 1. PYTHON OOP INTRO — Classes & Objects
# =============================================================================
#
# WHAT IS OOP?
#   A programming paradigm where you organize code around "objects" — bundles
#   of related data (attributes) and behavior (methods).
#
# WITHOUT OOP (procedural):
#   player1_name = "Alice"
#   player1_symbol = "X"
#   player2_name = "Bob"
#   player2_symbol = "O"
#   → messy, no grouping, easy to mix up variables
#
# WITH OOP:
#   player1 = Player("Alice", Symbol.X)
#   player2 = Player("Bob", Symbol.O)
#   → clean, grouped, self-documenting
#
# CORE TERMINOLOGY:
#   Class    → Blueprint/template (the recipe)
#   Object   → Instance created from a class (the actual cake)
#   self     → Reference to the current object instance
#   __init__ → Constructor, runs automatically when object is created

class Car:
    # __init__ is the CONSTRUCTOR
    # Called automatically when you do Car("Toyota", 2020)
    # 'self' is the object being created — Python passes it automatically
    def __init__(self, make: str, year: int):
        self.make = make      # instance attribute — unique per object
        self.year = year      # each Car object has its own make and year

    def describe(self) -> str:
        return f"{self.year} {self.make}"

# Creating objects (instantiation)
car1 = Car("Toyota", 2020)
car2 = Car("Honda", 2022)

# Each object is independent
print(car1.describe())  # "2020 Toyota"
print(car2.describe())  # "2022 Honda"

# HOW 'self' WORKS:
#   When you call car1.describe(), Python translates it to:
#   Car.describe(car1)
#   So 'self' inside describe() refers to car1
#
#   car2.describe() → Car.describe(car2) → self is car2
#
# WHY 'self' IS EXPLICIT IN PYTHON:
#   Java/C++ use 'this' implicitly. Python makes it explicit for clarity.
#   You MUST include self as the first parameter in instance methods.
#   You DON'T pass it when calling — Python handles that.


# =============================================================================
# 2. CLASS VARIABLES vs INSTANCE VARIABLES
# =============================================================================
#
# Instance Variable: Unique to each object. Defined in __init__ with self.
# Class Variable:    Shared across ALL objects of the class. Defined at
#                    class level (outside __init__).
#
# WHEN TO USE WHICH:
#   Class variable    → shared data, counters, constants, defaults
#   Instance variable → data unique to each object

class Student:
    # CLASS VARIABLE — shared by ALL Student objects
    # There's only ONE copy of this, stored on the class itself
    school_name = "Springfield High"
    student_count = 0

    def __init__(self, name: str, grade: int):
        # INSTANCE VARIABLES — unique to each Student object
        self.name = name
        self.grade = grade

        # Modifying class variable through the CLASS (not self)
        Student.student_count += 1

    def info(self) -> str:
        return f"{self.name}, Grade {self.grade}, {self.school_name}"

s1 = Student("Alice", 10)
s2 = Student("Bob", 11)

print(Student.student_count)   # 2 — shared across all instances
print(s1.school_name)          # "Springfield High" — accessed via instance
print(s2.school_name)          # "Springfield High" — same value

# IMPORTANT GOTCHA — Shadowing:
# If you do self.school_name = "New School" on s1,
# it creates a NEW instance variable on s1, it does NOT change the class variable.
# s2.school_name would still be "Springfield High"

s1.school_name = "New School"     # creates instance var on s1 only!
print(s1.school_name)             # "New School" (instance var shadows class var)
print(s2.school_name)             # "Springfield High" (still reads class var)
print(Student.school_name)        # "Springfield High" (class var unchanged)

# TO ACTUALLY CHANGE THE CLASS VARIABLE FOR EVERYONE:
Student.school_name = "Updated High"
print(s2.school_name)             # "Updated High"
# s1 still has its own instance variable shadowing it:
print(s1.school_name)             # "New School"

# LOOKUP ORDER:
#   When you access self.x, Python looks:
#   1. Instance's __dict__ (instance variables)
#   2. Class's __dict__ (class variables)
#   3. Parent class's __dict__ (inheritance chain)
#   First match wins. That's why instance vars "shadow" class vars.


# =============================================================================
# 3. INHERITANCE
# =============================================================================
#
# WHAT: A child class inherits ALL attributes and methods from a parent class.
# WHY:  Code reuse + "is-a" relationship.
#       Dog IS-A Animal. RowWinningStrategy IS-A WinningStrategy.
#
# The child can:
#   - Use parent's methods as-is (inherit)
#   - Override parent's methods (replace)
#   - Extend parent's methods (override + call super())
#   - Add new methods/attributes

class Animal:
    def __init__(self, name: str, speed: int):
        self.name = name
        self.speed = speed

    def move(self) -> str:
        return f"{self.name} moves at {self.speed} mph"

    def speak(self) -> str:
        return "..."

class Dog(Animal):    # Dog inherits from Animal
    def __init__(self, name: str, speed: int, breed: str):
        super().__init__()(name, speed)   # call parent's __init__
        self.breed = breed              # add Dog-specific attribute

    # OVERRIDE — replace parent's speak()
    def speak(self) -> str:
        return "Woof!"

    # NEW METHOD — only Dog has this
    def fetch(self) -> str:
        return f"{self.name} fetches the ball!"

dog = Dog("Rex", 30, "Labrador")
print(dog.move())    # "Rex moves at 30 mph" — INHERITED from Animal
print(dog.speak())   # "Woof!" — OVERRIDDEN
print(dog.fetch())   # "Rex fetches the ball!" — NEW in Dog
print(dog.breed)     # "Labrador" — Dog-specific attribute

# isinstance checks
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True  — Dog IS-A Animal

# WHAT GETS INHERITED:
#   ✅ All methods (move, speak)
#   ✅ All attributes set in parent's __init__ (name, speed)
#   ✅ Class variables from parent
#   ❌ Nothing is "private" in Python — even _private attrs are inherited
#
# METHOD RESOLUTION ORDER (MRO):
#   When you call dog.move(), Python searches:
#   Dog → Animal → object (built-in base)
#   First class that has the method wins.
#   dog.speak() → found in Dog → uses Dog's version
#   dog.move()  → not in Dog → found in Animal → uses Animal's version


# =============================================================================
# 4. MULTIPLE INHERITANCE
# =============================================================================
#
# WHAT: A class inherits from MORE THAN ONE parent class.
# WHY:  Combine behaviors from multiple sources.
#       Python supports this. Java does NOT (uses interfaces instead).
#
# DANGER: The "Diamond Problem" — what if two parents define the same method?
#         Python solves this with MRO (Method Resolution Order) using C3 linearization.

class Flyer:
    def fly(self) -> str:
        return "I can fly!"

    def move(self) -> str:
        return "Flying through the air"

class Swimmer:
    def swim(self) -> str:
        return "I can swim!"

    def move(self) -> str:
        return "Swimming through water"

# Duck inherits from BOTH Flyer and Swimmer
class Duck(Flyer, Swimmer):
    def quack(self) -> str:
        return "Quack!"

duck = Duck()
print(duck.fly())    # "I can fly!" — from Flyer
print(duck.swim())   # "I can swim!" — from Swimmer
print(duck.quack())  # "Quack!" — Duck's own

# THE DIAMOND PROBLEM:
# Both Flyer and Swimmer have move(). Which one does Duck use?
print(duck.move())   # "Flying through the air" — Flyer wins!

# WHY? Method Resolution Order (MRO):
print(Duck.__mro__)
# (Duck, Flyer, Swimmer, object)
# Python searches left to right: Duck → Flyer → Swimmer → object
# Flyer is listed FIRST in class Duck(Flyer, Swimmer), so Flyer's move() wins

# TO SEE MRO:
#   ClassName.__mro__  or  ClassName.mro()

# REAL WORLD USE IN OUR PROJECT:
#   Game(GameSubject)  — single inheritance
#   But multiple inheritance is useful when a class needs to be both
#   a Subject AND implement another interface.
#
# BEST PRACTICE:
#   - Keep inheritance trees shallow
#   - Prefer composition over multiple inheritance when possible
#   - If using multiple inheritance, use it for "mixin" classes
#     (small classes that add a single behavior)


# =============================================================================
# 5. ABSTRACT CLASSES (ABC)
# =============================================================================
#
# WHAT: A class that CANNOT be instantiated. It defines a CONTRACT —
#       "any subclass MUST implement these methods."
# WHY:  Enforces interface consistency. All WinningStrategies MUST have
#       check_winner(). If you forget, Python raises TypeError immediately.
#
# HOW:  Inherit from ABC, decorate methods with @abstractmethod
#
# ANALOGY: An abstract class is like a form template.
#          It has blank fields (abstract methods) that you MUST fill in.
#          You can't submit an empty form (can't instantiate ABC).

from abc import ABC, abstractmethod

class Shape(ABC):
    # ABSTRACT METHOD — subclasses MUST implement this
    # No default behavior — just a contract
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    # CONCRETE METHOD — has implementation, inherited as-is
    # Subclasses CAN override this, but don't have to
    def description(self) -> str:
        return f"I am a shape with area {self.area():.2f}"

# shape = Shape()  # TypeError: Can't instantiate abstract class Shape
#                   # with abstract methods area, perimeter

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:            # MUST implement
        return self.width * self.height

    def perimeter(self) -> float:       # MUST implement
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

rect = Rectangle(5, 3)
circ = Circle(7)

print(rect.area())          # 15
print(rect.description())   # "I am a shape with area 15.00" — inherited concrete method
print(circ.perimeter())     # 43.98

# WHAT HAPPENS IF YOU FORGET TO IMPLEMENT:
# class BadShape(Shape):
#     def area(self): return 0
#     # forgot perimeter()!
#
# BadShape()  # TypeError: Can't instantiate abstract class BadShape
#             # with abstract method perimeter

# ABC vs REGULAR CLASS:
#   Regular class → can be instantiated, no enforcement
#   ABC           → cannot be instantiated, enforces method implementation
#
# IN OUR PROJECT:
#   WinningStrategy(ABC)  → forces check_winner() on all strategies
#   GameState(ABC)        → forces handle_move() on all states
#   GameObserver(ABC)     → forces update() on all observers


# =============================================================================
# 6. super()
# =============================================================================
#
# WHAT: Returns a proxy object that delegates method calls to the parent class.
# WHY:  Call parent's methods without hardcoding the parent class name.
#       Essential for proper initialization in inheritance chains.
#
# WHEN TO USE:
#   1. In __init__ to call parent's constructor
#   2. When overriding a method but still wanting parent's behavior too

class Vehicle:
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

    def start(self) -> str:
        return "Vehicle started"

class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, battery_kwh: int):
        # super().__init__()() calls Vehicle.__init__()
        # This sets self.make and self.model
        super().__init__()(make, model)
        # Then we add ElectricCar-specific attribute
        self.battery_kwh = battery_kwh

    def start(self) -> str:
        # Call parent's start() AND add our own behavior
        parent_msg = super().start()
        return f"{parent_msg} silently (Battery: {self.battery_kwh}kWh)"

ev = ElectricCar("Tesla", "Model 3", 75)
print(ev.make)       # "Tesla" — set by Vehicle.__init__ via super()
print(ev.start())    # "Vehicle started silently (Battery: 75kWh)"

# WITHOUT super() — what goes wrong:
# class BadElectricCar(Vehicle):
#     def __init__(self, make, model, battery_kwh):
#         # FORGOT to call super().__init__()()!
#         self.battery_kwh = battery_kwh
#
# bad = BadElectricCar("Tesla", "Model 3", 75)
# print(bad.make)  # AttributeError: 'BadElectricCar' has no attribute 'make'
# Because Vehicle.__init__ was never called, self.make was never set!

# super() WITH MULTIPLE INHERITANCE:
# super() follows the MRO, not just "the parent"

class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return f"Hello from B, then {super().greet()}"

class C(A):
    def greet(self):
        return f"Hello from C, then {super().greet()}"

class D(B, C):
    def greet(self):
        return f"Hello from D, then {super().greet()}"

d = D()
print(d.greet())
# "Hello from D, then Hello from B, then Hello from C, then Hello from A"
# MRO: D → B → C → A
# super() in B goes to C (not A!), because MRO says C comes after B

print(D.__mro__)  # (D, B, C, A, object)

# KEY INSIGHT:
#   super() doesn't mean "call my parent."
#   It means "call the NEXT class in the MRO."
#   In simple single inheritance, next in MRO IS the parent.
#   In multiple inheritance, it might not be!


# =============================================================================
# 7. POLYMORPHISM
# =============================================================================
#
# WHAT: "Many forms" — the same method name behaves differently depending
#       on the actual object type at runtime.
# WHY:  Write code that works with a general type, and it automatically
#       does the right thing for each specific type.
#       The Game doesn't care which WinningStrategy it's calling.
#
# TWO KINDS:
#   1. Method Overriding — child class replaces parent's method (runtime)
#   2. Operator Overloading — redefine what +, ==, etc. do (magic methods)

# --- METHOD OVERRIDING (most common) ---

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"EMAIL: {message}"

class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS: {message}"

class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"PUSH: {message}"

# POLYMORPHISM IN ACTION:
# This function doesn't know or care which notification type it gets.
# It calls send() and the RIGHT version runs based on the actual object.
def notify_user(notifier: Notification, msg: str):
    print(notifier.send(msg))

notify_user(EmailNotification(), "Hello")   # "EMAIL: Hello"
notify_user(SMSNotification(), "Hello")     # "SMS: Hello"
notify_user(PushNotification(), "Hello")    # "PUSH: Hello"

# With a list — process mixed types uniformly:
notifiers: list[Notification] = [
    EmailNotification(),
    SMSNotification(),
    PushNotification()
]
for n in notifiers:
    print(n.send("Welcome!"))
# Each calls its OWN send() — that's polymorphism

# IN OUR PROJECT:
#   winning_strategies = [RowWinningStrategy(), ColumnWinningStrategy(), DiagonalWinningStrategy()]
#   for strategy in winning_strategies:
#       if strategy.check_winner(board, player):  # polymorphism!
#           return True
#   Game doesn't know which strategy. Each does its own check.

# --- OPERATOR OVERLOADING (via magic methods) ---

class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):      # what + does
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):       # what == does
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2         # calls v1.__add__(v2)
print(v3)             # "(4, 6)"
print(v1 == v2)       # False
print(v1 == Vector(1, 2))  # True


# =============================================================================
# 8. DUCK TYPING
# =============================================================================
#
# WHAT: "If it walks like a duck and quacks like a duck, it's a duck."
#       Python doesn't check the TYPE of an object — it checks if the
#       object has the required METHOD. No need for inheritance or interfaces.
#
# WHY:  Maximum flexibility. Any object that has the right methods works.
#       This is why Python is "dynamically typed."
#
# HOW:  Just call the method. If the object has it, it works.
#       If not, you get an AttributeError at runtime.

class RealDuck:
    def quack(self):
        return "Quack quack!"

    def walk(self):
        return "Waddle waddle"

class Person:
    def quack(self):
        return "I'm quacking like a duck!"

    def walk(self):
        return "Walking on two legs"

class RubberDuck:
    def quack(self):
        return "Squeak!"

    def walk(self):
        return "Doesn't walk, it floats"

# This function doesn't care about the type.
# It only cares: does the object have quack() and walk()?
def duck_test(thing):
    print(thing.quack())
    print(thing.walk())

duck_test(RealDuck())     # works — has quack() and walk()
duck_test(Person())       # works — has quack() and walk()
duck_test(RubberDuck())   # works — has quack() and walk()
# duck_test(42)           # AttributeError — int has no quack()

# DUCK TYPING vs ABC:
#   Duck typing:  No contract enforcement. Runtime errors if method missing.
#   ABC:          Compile-time-ish enforcement. TypeError at instantiation.
#
#   For our LLD project, we use ABCs because:
#   - We want GUARANTEED interface compliance
#   - We want errors EARLY (at class definition, not deep in game logic)
#   - It's a design-pattern-heavy project where contracts matter
#
#   Duck typing is great for:
#   - Quick scripts
#   - When you want maximum flexibility
#   - When the interface is obvious (like __iter__, __len__)

# PYTHON'S BUILT-IN DUCK TYPING EXAMPLES:
#   for x in something:       → calls something.__iter__()
#   len(something)            → calls something.__len__()
#   str(something)            → calls something.__str__()
#   something[0]              → calls something.__getitem__(0)
# Python doesn't check "is this a list?" — it checks "does it have __iter__?"


# =============================================================================
# 9. AGGREGATION (HAS-A, weak ownership)
# =============================================================================
#
# WHAT: A class USES objects that exist INDEPENDENTLY of it.
#       The contained objects can survive without the container.
#       "Has-a" relationship with WEAK ownership.
#
# ANALOGY: A Library has Books, but Books exist independently.
#          If the Library closes, the Books still exist.
#
# HOW:    Objects are created OUTSIDE the class and PASSED IN.

class Professor:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class Department:
    def __init__(self, name: str):
        self.name = name
        self.professors: list[Professor] = []  # aggregation

    def add_professor(self, professor: Professor):
        # Professor is created OUTSIDE and passed in
        # Department doesn't own the Professor's lifecycle
        self.professors.append(professor)

    def show(self):
        names = [str(p) for p in self.professors]
        print(f"{self.name}: {', '.join(names)}")

# Professors exist independently
prof1 = Professor("Dr. Smith")
prof2 = Professor("Dr. Jones")

# Department uses them but doesn't own them
cs_dept = Department("Computer Science")
cs_dept.add_professor(prof1)
cs_dept.add_professor(prof2)
cs_dept.show()  # "Computer Science: Dr. Smith, Dr. Jones"

# If department is deleted, professors still exist
del cs_dept
print(prof1.name)  # "Dr. Smith" — still alive!

# IN OUR PROJECT:
#   Game receives Player objects — Players exist independently of Game.
#   Game receives WinningStrategy objects — strategies exist independently.
#   If Game is destroyed, Players and Strategies still exist.
#   → This is aggregation.


# =============================================================================
# 10. COMPOSITION (HAS-A, strong ownership)
# =============================================================================
#
# WHAT: A class OWNS objects that are created INSIDE it.
#       The contained objects CANNOT exist without the container.
#       "Has-a" relationship with STRONG ownership.
#
# ANALOGY: A House has Rooms. If the House is demolished, Rooms are gone.
#          Rooms don't exist independently outside a House.
#
# HOW:    Objects are created INSIDE the class constructor.
#
# KEY DIFFERENCE FROM AGGREGATION:
#   Aggregation:  objects passed IN from outside (weak ownership)
#   Composition:  objects created INSIDE the class (strong ownership)

class CPU:
    def __init__(self, cores: int):
        self.cores = cores

    def process(self) -> str:
        return f"Processing on {self.cores} cores"

class RAM:
    def __init__(self, gb: int):
        self.gb = gb

class Computer:
    def __init__(self, cpu_cores: int, ram_gb: int):
        # COMPOSITION — CPU and RAM are created INSIDE Computer
        # They don't exist outside this Computer
        # When Computer is deleted, CPU and RAM are also deleted
        self.cpu = CPU(cpu_cores)
        self.ram = RAM(ram_gb)

    def run(self) -> str:
        return f"{self.cpu.process()} with {self.ram.gb}GB RAM"

pc = Computer(8, 16)
print(pc.run())  # "Processing on 8 cores with 16GB RAM"
# pc.cpu and pc.ram were created by Computer, owned by Computer

# IN OUR PROJECT:
#   Board creates Cell objects inside initialize_board()
#   → Board OWNS the Cells. Cells don't exist without the Board.
#   → This is composition.

# COMPARISON TABLE:
#   | Aspect       | Aggregation          | Composition            |
#   |------------- |----------------------|------------------------|
#   | Ownership    | Weak (borrows)       | Strong (owns)          |
#   | Creation     | Outside, passed in   | Inside the class       |
#   | Lifecycle    | Independent          | Tied to container      |
#   | Example      | Game has Players     | Board has Cells        |
#   | Deletion     | Parts survive        | Parts destroyed too    |


# =============================================================================
# 11. NESTED CLASSES
# =============================================================================
#
# WHAT: A class defined INSIDE another class.
# WHY:  When the inner class is tightly coupled to the outer class and
#       has no meaning outside of it. Keeps it organized and private.
#
# WHEN TO USE:
#   - The inner class is only used by the outer class
#   - You want to logically group classes
#   - Builder pattern, Node in LinkedList, etc.
#
# WHEN NOT TO USE:
#   - If the inner class is useful elsewhere, make it top-level

class LinkedList:
    # Node is NESTED — it only makes sense inside LinkedList
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

        def __str__(self):
            return str(self.data)

    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = LinkedList.Node(data)  # use OuterClass.InnerClass
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        parts = []
        current = self.head
        while current:
            parts.append(str(current.data))
            current = current.next
        print(" -> ".join(parts))

ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.display()  # "1 -> 2 -> 3"

# Accessing nested class from outside (possible but usually not needed):
# node = LinkedList.Node(42)

# ANOTHER EXAMPLE — Iterator pattern:

class Playlist:
    class Song:
        def __init__(self, title: str, artist: str):
            self.title = title
            self.artist = artist

        def __str__(self):
            return f"{self.title} by {self.artist}"

    def __init__(self, name: str):
        self.name = name
        self.songs: list[Playlist.Song] = []

    def add(self, title: str, artist: str):
        self.songs.append(Playlist.Song(title, artist))

    def show(self):
        print(f"Playlist: {self.name}")
        for i, song in enumerate(self.songs, 1):
            print(f"  {i}. {song}")

playlist = Playlist("Road Trip")
playlist.add("Bohemian Rhapsody", "Queen")
playlist.add("Hotel California", "Eagles")
playlist.show()

# IN OUR PROJECT:
#   We don't use nested classes — all our classes are top-level because
#   Cell, Player, Board, etc. are all independently meaningful.
#   But it's good to know for other LLD problems (e.g., LinkedList.Node).


# =============================================================================
# 12. STATIC METHODS (@staticmethod)
# =============================================================================
#
# WHAT: A method that belongs to the class but does NOT access instance (self)
#       or class (cls) data. It's just a regular function that lives inside
#       a class for organizational purposes.
#
# WHY:  Group utility functions with the class they relate to.
#       Makes it clear the function is conceptually part of that class.
#
# WHEN TO USE:
#   - Utility/helper functions related to the class
#   - Functions that don't need self or cls
#   - Factory-like methods that don't need class state

class MathUtils:
    @staticmethod
    def add(a: int, b: int) -> int:
        # No self, no cls — pure function
        return a + b

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

# Called on the class directly — no instance needed
print(MathUtils.add(3, 5))       # 8
print(MathUtils.is_even(4))      # True

# Can also be called on an instance (but why?)
m = MathUtils()
print(m.add(3, 5))               # 8 (works but unusual)

class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c: float) -> float:
        return (c * 9 / 5) + 32

    @staticmethod
    def fahrenheit_to_celsius(f: float) -> float:
        return (f - 32) * 5 / 9

print(TemperatureConverter.celsius_to_fahrenheit(100))  # 212.0
print(TemperatureConverter.fahrenheit_to_celsius(32))   # 0.0

# STATIC METHOD vs REGULAR METHOD vs CLASS METHOD:
#   Regular method: def method(self)      → accesses instance data
#   Class method:   def method(cls)       → accesses class data
#   Static method:  def method()          → accesses nothing, pure utility
#
# IF YOUR METHOD DOESN'T USE self OR cls, MAKE IT @staticmethod.
# This signals to readers: "this method is independent of any state."


# =============================================================================
# 13. CLASS METHODS (@classmethod)
# =============================================================================
#
# WHAT: A method that receives the CLASS (cls) as first argument instead
#       of the instance (self). Can access and modify class-level state.
#
# WHY:  - Alternative constructors (factory methods)
#       - Modify class variables
#       - Methods that logically belong to the class, not instances
#
# KEY DIFFERENCE FROM STATIC:
#   @staticmethod → no access to class or instance
#   @classmethod  → access to the CLASS (cls), but not a specific instance

class Employee:
    raise_percentage = 1.05    # class variable
    employee_count = 0

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
        Employee.employee_count += 1

    def apply_raise(self):
        self.salary *= self.raise_percentage

    # CLASS METHOD — receives cls (the class itself)
    @classmethod
    def set_raise_percentage(cls, percentage: float):
        # Modifies the CLASS variable, affects all instances
        cls.raise_percentage = percentage

    # ALTERNATIVE CONSTRUCTOR — common use case
    # Creates an Employee from a different data format
    @classmethod
    def from_string(cls, emp_string: str):
        name, salary = emp_string.split("-")
        return cls(name, float(salary))   # cls() is same as Employee()

    @classmethod
    def get_count(cls) -> int:
        return cls.employee_count

# Normal constructor
emp1 = Employee("Alice", 50000)

# Alternative constructor via @classmethod
emp2 = Employee.from_string("Bob-60000")
print(emp2.name)     # "Bob"
print(emp2.salary)   # 60000.0

# Modify class variable via @classmethod
Employee.set_raise_percentage(1.10)
emp1.apply_raise()
print(emp1.salary)   # 55000.0

print(Employee.get_count())  # 2

# WHY cls INSTEAD OF Employee?
#   If someone creates a subclass of Employee, cls will be the SUBCLASS,
#   not Employee. This makes classmethods work correctly with inheritance.

class Manager(Employee):
    pass

# Manager.from_string("Carol-80000") → cls is Manager, creates Manager object
mgr = Manager.from_string("Carol-80000")
print(type(mgr))     # <class 'Manager'> — NOT Employee!
# If we used Employee() instead of cls(), this would return an Employee

# SUMMARY:
#   @classmethod → alternative constructors, class variable manipulation
#   @staticmethod → pure utility functions grouped with the class
#   Regular method → operates on specific instance (self)


# =============================================================================
# 14. MAGIC METHODS (Dunder Methods)
# =============================================================================
#
# WHAT: Special methods surrounded by double underscores (__method__).
#       Python calls them automatically in certain situations.
#       "Dunder" = Double UNDERscore.
#
# WHY:  Define how your objects behave with built-in operations.
#       How they print, compare, add, iterate, etc.
#
# YOU'VE ALREADY SEEN:
#   __init__  → constructor
#   __str__   → string representation
#   __add__   → + operator

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # --- STRING REPRESENTATION ---
    def __str__(self) -> str:
        """Called by print() and str(). Human-readable."""
        return f"{self.name}: ${self.price:.2f}"

    def __repr__(self) -> str:
        """Called in debugger, REPL, and inside lists. Developer-readable."""
        return f"Product('{self.name}', {self.price})"

    # --- COMPARISON ---
    def __eq__(self, other) -> bool:
        """Called by =="""
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def __lt__(self, other) -> bool:
        """Called by <. Also enables sorting."""
        return self.price < other.price

    def __le__(self, other) -> bool:
        """Called by <="""
        return self.price <= other.price

    # --- ARITHMETIC ---
    def __add__(self, other):
        """Called by +. Returns combined product."""
        return Product(f"{self.name} + {other.name}", self.price + other.price)

    # --- CONTAINER-LIKE ---
    def __len__(self) -> int:
        """Called by len(). Return name length as example."""
        return len(self.name)

    def __bool__(self) -> bool:
        """Called by bool() and if statements. Product is truthy if price > 0."""
        return self.price > 0

p1 = Product("Laptop", 999.99)
p2 = Product("Mouse", 29.99)
p3 = Product("Laptop", 999.99)

# __str__
print(p1)                    # "Laptop: $999.99"

# __repr__
print(repr(p1))              # "Product('Laptop', 999.99)"
print([p1, p2])              # [Product('Laptop', 999.99), Product('Mouse', 29.99)]

# __eq__
print(p1 == p3)              # True (same name and price)
print(p1 == p2)              # False

# __lt__ (enables sorting!)
products = [p1, p2]
products.sort()              # uses __lt__
print(products)              # [Product('Mouse', 29.99), Product('Laptop', 999.99)]

# __add__
bundle = p1 + p2
print(bundle)                # "Laptop + Mouse: $1029.98"

# __len__
print(len(p1))               # 6 (length of "Laptop")

# __bool__
free = Product("Sample", 0)
print(bool(p1))              # True
print(bool(free))            # False
if p1:
    print("Product exists")  # prints — because __bool__ returns True

# COMMON MAGIC METHODS TABLE:
#
#   Method          | Trigger              | Example
#   --------------- |----------------------|------------------
#   __init__        | object creation      | Product("X", 10)
#   __str__         | print(), str()       | print(obj)
#   __repr__        | repr(), debugger     | repr(obj)
#   __eq__          | ==                   | obj1 == obj2
#   __ne__          | !=                   | obj1 != obj2
#   __lt__          | <                    | obj1 < obj2
#   __le__          | <=                   | obj1 <= obj2
#   __gt__          | >                    | obj1 > obj2
#   __ge__          | >=                   | obj1 >= obj2
#   __add__         | +                    | obj1 + obj2
#   __sub__         | -                    | obj1 - obj2
#   __mul__         | *                    | obj1 * obj2
#   __len__         | len()               | len(obj)
#   __bool__        | bool(), if           | if obj:
#   __getitem__     | indexing []          | obj[0]
#   __setitem__     | assignment []        | obj[0] = x
#   __contains__    | in                   | x in obj
#   __iter__        | for loop             | for x in obj:
#   __next__        | next()              | next(iter(obj))
#   __call__        | calling as function  | obj()
#   __hash__        | hash(), dict key     | {obj: "val"}
#   __del__         | deletion             | del obj


# =============================================================================
# 15. @property DECORATOR
# =============================================================================
#
# WHAT: Makes a method behave like an attribute.
#       Provides getter, setter, and deleter with controlled access.
#
# WHY:  - Encapsulation: validate data before setting
#       - Computed attributes: calculate value on access
#       - Clean syntax: obj.name instead of obj.get_name()
#       - You can add validation LATER without changing the interface
#
# THE EVOLUTION:
#   Step 1: Public attribute       → obj.age = -5 (no protection!)
#   Step 2: Getter/setter methods  → obj.get_age() (ugly, Java-style)
#   Step 3: @property              → obj.age (clean + protected)

class Person:
    def __init__(self, name: str, age: int):
        self._name = name     # underscore = "private by convention"
        self._age = age       # actual storage

    # --- GETTER ---
    # @property makes this method callable as an attribute
    @property
    def name(self) -> str:
        """Read-only property — no setter defined."""
        return self._name

    @property
    def age(self) -> int:
        return self._age

    # --- SETTER ---
    # @age.setter runs when you do: person.age = 25
    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

    # --- COMPUTED PROPERTY ---
    # No setter — it's calculated, not stored
    @property
    def is_adult(self) -> bool:
        return self._age >= 18

    # --- DELETER (rarely used) ---
    @age.deleter
    def age(self):
        print("Deleting age...")
        self._age = 0

person = Person("Alice", 25)

# GETTER — looks like attribute access, but calls the method
print(person.name)       # "Alice" — calls name getter
print(person.age)        # 25 — calls age getter
print(person.is_adult)   # True — computed property

# SETTER — looks like attribute assignment, but calls the method
person.age = 30          # calls age setter, validation passes
print(person.age)        # 30

# person.age = -5        # raises ValueError: Age must be between 0 and 150
# person.age = "old"     # raises TypeError: Age must be an integer
# person.name = "Bob"    # AttributeError: property 'name' has no setter
#                        # (read-only because we didn't define @name.setter)

# DELETER
del person.age           # prints "Deleting age...", sets _age to 0
print(person.age)        # 0

# REAL-WORLD USE CASE — Computed from other attributes:

class Rectangle2:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self) -> float:
        """Computed property — always up to date."""
        return self._width * self._height

    @property
    def perimeter2(self) -> float:
        return 2 * (self._width + self._height)

r = Rectangle2(5, 3)
print(r.area)        # 15.0
r.width = 10
print(r.area)        # 30.0 — automatically recalculated!

# IN OUR PROJECT:
#   Cell uses @property for symbol getter/setter
#   Board might use @property for computed values like is_full
#   This gives clean syntax: cell.symbol instead of cell.get_symbol()

# COMMON PATTERN — property with validation:
#
#   @property
#   def x(self):
#       return self._x
#
#   @x.setter
#   def x(self, value):
#       # validate here
#       self._x = value
#
#   Usage:
#       obj.x          → calls getter
#       obj.x = val    → calls setter (with validation)


# =============================================================================
# SUMMARY — WHEN TO USE WHAT
# =============================================================================
#
#   CONCEPT              | USE WHEN
#   ---------------------|--------------------------------------------
#   Enum                 | Fixed set of constants (Symbol.X, Status.DRAW)
#   Class Variable       | Data shared by all instances (count, default)
#   Instance Variable    | Data unique to each object (name, score)
#   Inheritance          | "is-a" relationship (Dog is-a Animal)
#   Multiple Inheritance | Combining behaviors (use sparingly)
#   ABC                  | Enforcing interface contracts
#   super()              | Calling parent methods, especially __init__
#   Polymorphism         | Same interface, different behavior
#   Duck Typing          | Flexible, no strict type checks needed
#   Aggregation          | Object uses others created outside (weak has-a)
#   Composition          | Object creates and owns others (strong has-a)
#   Nested Class         | Inner class only meaningful inside outer
#   @staticmethod        | Utility function, no self/cls needed
#   @classmethod         | Alternative constructor, modify class state
#   Magic Methods        | Custom behavior for operators/built-ins
#   @property            | Controlled attribute access with validation
# =============================================================================
