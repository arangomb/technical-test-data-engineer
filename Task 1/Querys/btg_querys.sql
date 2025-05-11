-- 1. Listar los clientes que han visitado más de 3 sucursales.
WITH multisucursal AS (
    SELECT idCliente
    FROM visitan
    GROUP BY idCliente
    HAVING COUNT(DISTINCT idSucursal) > 3
)
SELECT c.id, c.nombre, c.apellidos
FROM cliente c
JOIN multisucursal ms ON c.id = ms.idCliente;

-- 2. Obtener los productos que están disponibles en todas las sucursales
SELECT p.id, p.nombre
FROM producto p
WHERE NOT EXISTS(
    SELECT 1
    FROM sucursal s
    WHERE NOT EXISTS (
        SELECT 1
        FROM disponibilidad d
        WHERE d.idProducto = p.id AND d.idSucursal = s.id
    )
);

-- 3. Listar las fechas de visita en que un cliente visitó una sucursal que no es de su ciudad
SELECT v.fechaVisita
FROM visitan v
JOIN cliente c ON v.idCliente = c.id
JOIN sucusal s ON v.idSucursal = s.id
WHERE s.ciudad <> c.ciudad

-- 4.  Obtener los nombres de los clientes los cuales tienen inscrito algún producto disponible 
--     sólo en las sucursales que visitan.
SELECT c.id, c.nombre, c.apellidos
FROM cliente c
WHERE EXISTS (
    SELECT 1
    FROM inscripcion i
    WHERE i.idCliente = c.id
        AND NOT EXISTS(
            SELECT 1
            FROM disponibilidad d
            WHERE d.idProducto = i.idProducto
                AND d.idSucursal NOT IN (
                    SELECT v.idSucursal
                    FROM visitan v
                    WHERE v.idCliente = c.id
                )
        )
)

-- 5. ¿Qué recomendaciones podrías hacer al modelo para mejorarlo?

/*
    1. Crear una tabla de "Ciudad", ya que este campo se utiliza tanto en la tabla de clientes 
    como en la de sucursales. La creación de una tabla independiente permitiría mantener la 
    consistencia de los datos y facilitar el mantenimiento, ya que, en caso de un cambio en el 
    nombre de una ciudad, solo sería necesario actualizarlo en un único lugar.

    2. Incluir campos de auditoría para garantizar la integridad y trazabilidad de la información.
    Se deben incorporar campos como el usuario, la fecha de creación y/o actualización. Esto permitirá 
    realizar un seguimiento detallado de las actividades en la base de datos, asegurando así un control 
    más riguroso y transparente de los procesos.

    3. Mejorar la nomenclatura de las tablas y columnas del modelo, aplicando convenciones de nombramiento 
    más claras y consistentes. Entre las sugerencias esta el uso del prefijo "tbl" para identificar 
    de manera más rápida y sencilla las tablas dentro del esquema, esto facilitará la distinción de los 
    objetos a consultar. Además, otra de las sugerencias es que los identificadores (id) de cada tabla sean 
    nombrados de forma que incluyan el nombre de la tabla, ya sea como prefijo o sufijo, para evitar posibles 
    conflictos, ya que "Id" es una palabra reservada en SQL Server.
*/