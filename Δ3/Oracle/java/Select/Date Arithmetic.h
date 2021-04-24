You can use the addition and subtraction operators with dates. The following example adds two days to July 25, 2012:


SQL> SELECT TO_DATE('25-JUL-2012') + 2 FROM dual;

TO_DATE('
---------
27-JUL-12

SQL>
TO_DATE() is a function that converts a string to a date. Subtract three days from August 2, 2012:


SQL> SELECT TO_DATE('02-AUG-2012') - 3 FROM dual;

TO_DATE('
---------
30-JUL-12

SQL>
Subtract one date from another, return the number of days between the two dates.


SQL> SELECT TO_DATE('02-AUG-2007') - TO_DATE('25-JUL-2007') FROM dual;

TO_DATE('02-AUG-2007')-TO_DATE('25-JUL-2007')
---------------------------------------------
                                            8

SQL>
