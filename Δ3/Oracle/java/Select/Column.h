Column Aliases

CREATE TABLE EMP (EMPNO NUMBER(4) NOT NULL,
                  ENAME VARCHAR2(10),
                  JOB VARCHAR2(9),
                  SAL NUMBER(7, 2),
                  DEPTNO NUMBER(2));

INSERT INTO EMP VALUES (1, 'SMITH', 'CLERK',     800,    20);
INSERT INTO EMP VALUES (2, 'ALLEN', 'SALESMAN', 1600,    30);
INSERT INTO EMP VALUES (3, 'WARD',  'SALESMAN', 1250,    30);
INSERT INTO EMP VALUES (4, 'JONES', 'MANAGER',  2975,    20);
INSERT INTO EMP VALUES (5, 'MARTIN','SALESMAN', 1250,    30);
INSERT INTO EMP VALUES (6, 'BLAKE', 'MANAGER',  2850,    30);
INSERT INTO EMP VALUES (7, 'CLARK', 'MANAGER',  2850,    10);
INSERT INTO EMP VALUES (8, 'SCOTT', 'ANALYST',  3000,    20);
INSERT INTO EMP VALUES (9, 'KING',  'PRESIDENT',3000,    10);
INSERT INTO EMP VALUES (10,'TURNER','SALESMAN', 1500,    30);
INSERT INTO EMP VALUES (11,'ADAMS', 'CLERK',    1500,    20);
You can provide your own header using an alias.


SQL> SELECT sal * 2 DOUBLE_SALARY FROM emp;

DOUBLE_SALARY
-------------
         1600
         3200
         2500
         5950
         2500
         5700
         5700
         6000
         6000
         3000
         3000

11 rows selected.

SQL>
To use spaces and preserve the case of your alias text, place the text within double quotation marks (""):


SQL> SELECT sal * 2 "DOUBLE SALARY" FROM emp;

DOUBLE SALARY
-------------
         1600
         3200
         2500
         5950
         2500
         5700
         5700
         6000
         6000
         3000
         3000

11 rows selected.

SQL>
You can use the optional AS keyword before the alias:


SQL> SELECT sal * 2 AS "DOUBLE SALARY" FROM emp;

DOUBLE SALARY
-------------
         1600
         3200
         2500
         5950
         2500
         5700
         5700
         6000
         6000
         3000
         3000

11 rows selected.

SQL>
