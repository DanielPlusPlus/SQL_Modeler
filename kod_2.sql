CREATE TABLE "student" (
    "id" NUMBER,
    "name" VARCHAR2(20),
    CONSTRAINT "pk_student" PRIMARY KEY ("id")
);

CREATE TABLE "course" (
    "id" NUMBER,
    "name" VARCHAR2(20),
    CONSTRAINT "pk_course" PRIMARY KEY ("id")
);

CREATE TABLE "student_course" (
    "student_id" NUMBER NOT NULL,
    "course_id" NUMBER NOT NULL,
    CONSTRAINT "pk_student_course" PRIMARY KEY ("student_id","course_id"),
    CONSTRAINT "fk_student_course_student" FOREIGN KEY ("student_id") REFERENCES "student"("id"),
    CONSTRAINT "fk_student_course_course" FOREIGN KEY ("course_id") REFERENCES "course"("id")
);