CREATE OR REPLACE TYPE "Person_T" AS OBJECT (
    "pesel" NUMBER,
    "birth_city" VARCHAR2(20)
) NOT FINAL;

CREATE OR REPLACE TYPE "Student_T" UNDER "Person_T" (
    "id" NUMBER,
    "name" VARCHAR2(20),
    "department_id" NUMBER
);

CREATE TABLE "Student" OF "Student_T" (
    "id" NOT NULL,
    "name" NOT NULL,
    CONSTRAINT "pk_Student" PRIMARY KEY ("id")
);

CREATE TABLE "Departments" (
    "id" NUMBER,
    "name" VARCHAR2(20),
    CONSTRAINT "pk_Departments" PRIMARY KEY ("id")
);

CREATE TABLE "Person" OF "Person_T" (
    "pesel" NOT NULL,
    UNIQUE ("pesel")
);

ALTER TABLE "Student" ADD CONSTRAINT "fk_Student_department_id" FOREIGN KEY ("department_id") REFERENCES "Departments"("id");