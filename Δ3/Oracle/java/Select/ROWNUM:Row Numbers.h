CREATE TABLE EMP (EMPNO NUMBER(4) NOT NULL,
                      ENAME VARCHAR2(10),
                      HIREDATE DATE);

INSERT INTO EMP VALUES (1, 'SMITH', TO_DATE('17-DEC-1980', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (2, 'ALLEN', TO_DATE('20-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (3, 'WARD',  TO_DATE('22-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (4, 'JONES', TO_DATE('2-APR-1981',  'DD-MON-YYYY'));
INSERT INTO EMP VALUES (5, 'MARTIN',TO_DATE('28-SEP-1981', 'DD-MON-YYYY'));

SQL> SELECT ROWNUM, empno, ename FROM Emp;

    ROWNUM      EMPNO ENAME
---------- ---------- ----------
         1          1 SMITH
         2          2 ALLEN
         3          3 WARD
         4          4 JONES
         5          5 MARTIN

SQL>
ROWNUM and where clause:


SQL> SELECT ROWNUM, empno, ename FROM Emp
  2  WHERE empno = 3;

    ROWNUM      EMPNO ENAME
---------- ---------- ----------
         1          3 WARD

SQL>
