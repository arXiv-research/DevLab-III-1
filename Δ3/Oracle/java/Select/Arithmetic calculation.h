The arithmetic expressions can be performed in SQL statements, which consist addition, subtraction, multiplication, and division. Arithmetic expressions can be done on numbers or dates. The four arithmetic operators are shown in the following table:

Operator	Description
+	Addition
-	Subtraction
*	Multiplication
/	Division

SQL> SELECT 2 * 6 FROM dual;

       2*6
----------
        12

SQL>
multiplication and division are performed first, followed by addition and subtraction. If operators of the same precedence are used, they are performed from left to right.


SQL> SELECT 10 * 12 / 3 - 5 FROM dual;

 10*12/3-5
----------
        35

SQL>
You can use parentheses () to specify the order of execution for the operators:


SQL> SELECT 10 * (12 / 3 - 5)
  2  FROM dual;

10*(12/3-5)
-----------
        -10

SQL>
Arithmetic Operators in Order of Precedence

Name	Operator	Precedence
Parentheses	( )	1
Multiplication, Division	*, /	2
Addition, Subtraction	+, -	3
