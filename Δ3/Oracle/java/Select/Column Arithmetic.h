CREATE TABLE EMP (EMPNO NUMBER(4) NOT NULL,
                      ENAME VARCHAR2(10),
                      HIREDATE DATE);

INSERT INTO EMP VALUES (1, 'SMITH', TO_DATE('17-DEC-1980', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (2, 'ALLEN', TO_DATE('20-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (3, 'WARD',  TO_DATE('22-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (4, 'JONES', TO_DATE('2-APR-1981',  'DD-MON-YYYY'));
INSERT INTO EMP VALUES (5, 'MARTIN',TO_DATE('28-SEP-1981', 'DD-MON-YYYY'));

SQL> select ename, hiredate + 3 from emp;

ENAME      HIREDATE+
---------- ---------
SMITH      20-DEC-80
ALLEN      23-FEB-81
WARD       25-FEB-81
JONES      05-APR-81
MARTIN     01-OCT-81

SQL>
Combine more than one operator in an expression.


SQL> select ename, hiredate + 3 -1 from emp;

ENAME      HIREDATE+
---------- ---------
SMITH      19-DEC-80
ALLEN      22-FEB-81
WARD       24-FEB-81
JONES      04-APR-81
MARTIN     30-SEP-81

SQL>
