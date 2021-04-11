Each row in an Oracle database has a unique row identifier, or ROWID. ROWID stores the physical location of the row. A ROWID is an 18-digit number that is represented as a base-64 number. ROWID is known as a pseudo column.


CREATE TABLE EMP (EMPNO NUMBER(4) NOT NULL,
                      ENAME VARCHAR2(10),
                      HIREDATE DATE);

INSERT INTO EMP VALUES (1, 'SMITH', TO_DATE('17-DEC-1980', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (2, 'ALLEN', TO_DATE('20-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (3, 'WARD',  TO_DATE('22-FEB-1981', 'DD-MON-YYYY'));
INSERT INTO EMP VALUES (4, 'JONES', TO_DATE('2-APR-1981',  'DD-MON-YYYY'));
INSERT INTO EMP VALUES (5, 'MARTIN',TO_DATE('28-SEP-1981', 'DD-MON-YYYY'));


SQL> SELECT ROWID, empno FROM emp;

ROWID                   EMPNO
------------------ ----------
AAADcFAABAAAKZCAAA          1
AAADcFAABAAAKZCAAB          2
AAADcFAABAAAKZCAAC          3
AAADcFAABAAAKZCAAD          4
AAADcFAABAAAKZCAAE          5

SQL>
