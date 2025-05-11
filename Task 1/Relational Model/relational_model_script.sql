CREATE DATABASE IF NOT EXISTS BTG;

USE BTG;

CREATE TABLE "cliente"(
    "id" INT PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "apellidos" VARCHAR(100) NOT NULL,
    "ciudad" VARCHAR(100) NOT NULL
);

CREATE TABLE "producto"(
    "id" INT PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "tipoProducto" VARCHAR(100) NOT NULL
);

CREATE TABLE "inscripcion"(
    "idProducto" INT,
    "idCliente" INT,
    PRIMARY KEY ("idProducto", "idCliente"),
    FOREIGN KEY ("idProducto") REFERENCES "producto"("id"),
    FOREIGN KEY ("idCliente") REFERENCES "cliente"("id"),
);

CREATE TABLE "sucursal"(
    "id" INT PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "ciudad" VARCHAR(100) NOT NULL
);

CREATE TABLE "disponibilidad"(
    "idSucursal" INT,
    "idProducto" INT,
    PRIMARY KEY ("idSucursal", "idProducto"),
    FOREIGN KEY ("idSucursal") REFERENCES "sucursal"("id"),
    FOREIGN KEY ("idProducto") REFERENCES "producto"("id"),
);

CREATE TABLE "visitan"(
    "idSucursal" INT,
    "idCliente" INT,
    "fechaVisita" DATE NOT NULL,
    PRIMARY KEY ("idSucursal", "idCliente"),
    FOREIGN KEY ("idSucursal") REFERENCES "sucursal"("id"),
    FOREIGN KEY ("idCliente") REFERENCES "cliente"("id"),
);