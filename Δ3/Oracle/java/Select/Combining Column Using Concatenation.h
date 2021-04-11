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

SQL> SELECT ename || '''s employee number is ' || empno AS "ID/Name"
  2  FROM emp;

ID/Name
------------------------------------------------------------------------
SMITH's employee number is 1
ALLEN's employee number is 2
WARD's employee number is 3
JONES's employee number is 4
MARTIN's employee number is 5
BLAKE's employee number is 6
CLARK's employee number is 7
SCOTT's employee number is 8
KING's employee number is 9
TURNER's employee number is 10
ADAMS's employee number is 11

11 rows selected.

SQL>
