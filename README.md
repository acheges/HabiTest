# HabiTest

## ReadMe

En el presente proyecto se hace una versión minimalista de un servicio de consulta para API de Habi. 
Para tal efecto se inicia explorando las tablas que contiene la base de datos. 

Encontramos como relevantes tres tablas de las cuales se alimentará la API de consulta. 
Nos valdremos unicamente de un método GET para el código funcional de la misma. 

En vista de que es un proyecto pequeño dejamos al usuario la posibilidad de omitir entornos virtuales si así lo considera, sin embargo se le exhorta a considerarlo para cualquier fin de escalarlo. 

Estamos prescindiendo de un modelo ORM, el cual se recomendaría de forma mas ortodoxa para mapear los objetos de python en relación con la base de Datos SQL. Aprovechamos para mencionar que un modelo ORM como SQLAlchemy tiene la ventaja de ofrecer “sanitización” de las queries enviadas a la DB. 
Sin embargo parte del código presentado lleva como fin exponer las consultas efectuadas a la base de datos. 

Para el fin de ganar familiaridad con las tablas se deja expuestas en diversas rutas el contenido del mismo, en formato JSON con el fin de que el usuario las explore y conozca los campos que las componen.

Las tablas de las que se vale el proyecto son :
    • property 		Tabla de las propiedades
    • status_history		Historial de cada propiedad
    • status			Etiquetas de los estatus empleados

Basicamente se trata de hacer una triple join de las tres tablas. A considerar unicamente que la tabla status_history debe de contemplar la última actualización de cada propiedad. Es por ello que para esta tabla hacemos una self join, obteniendo así: primero los valores “maximos” del timestamp de cada propiedad y luego obteniendo los valores acompañantes por medio de dicha self join.
- - -
El resto de los argumentos del método Get se obtienen de los parámetros de la URL.
Vale la pena destacar que esta prueba fue realizada en FLASK.
Se observó que algunas cualidades de fitros no son muy eficientes en MySQL para el despliegue de datos, por lo que se unificaron campos nulos y vacíos manipulando la salida del la respuesta. previo a "Jsonificarlo"

http://127.0.0.1:3000/api/v1/updatedproperties
Ejemplos
http://127.0.0.1:3000/api/v1/updatedproperties?year=2000&status_id=3
http://127.0.0.1:3000/api/v1/updatedproperties?ymin=2000&ymax=2002
http://127.0.0.1:3000/api/v1/updatedproperties?city=bogota

+ status_id
+ property_id
+ city
+ year (Busca por año preciso)

+ ymin (Cota inferior de año)
+ ymax (Cota superior de año)
+ pmin (Cota inferior de precio)
+ pmax (Cota superior de precio)
- - -
### UnitTests
Los UnitTests unicamente corroboran algunas de las principales cualidades de este EndPoint.


- - -
## Extendiendo el modelo para sistema de Me gusta
- - -
El presente modelo puede admitir una sección de “Me gusta”. 

Para ello deberíamos hacer un update (Rest PUT) de la misma tabla ingresando un nuevo campo. 
En dicho campo se puede agregar el id de la tabla property, aunque en vista de que aparentemente se busca recopilar esta información con principal énfasis en las propiedades (inducimos esto, a partir de que se recopila esta información tanto de usuarios logueados como no logueados), parece ideal la creación de una nueva tabla cuyas clave foráneas permitan relacionarla con los usuarios y con la propiedades, además de contar con un TimeStamp.
Sería similar a status_history en el sentido de que sería una colección de TimeStamps y Usuario activos y no logueados
Así, en caso de que el usuario no esté logueado se podrá asignar una bandera (Usuario Nulo, o vacío por ejemplo) Uno de los aspectos a considerar bajo esta premisa es que el usuario se encuentre logueado adecuadamente para poder asignar el id de usuario. 
Estos aspectos se pueden resolver fácilmente con diversos middlewares de Django.

Presento la relación de las principales tablas que alimentaría esta hipotética tabla. 



    ------------------                ----------------                  -----------------
        auth_user                         property                       liked_table
    ------------------                ----------------                  -----------------
    id(foreign key, ref liked_table)   id(foreign key)  ----------->>    property_id (foreign key, ref property(id)
              !---------------------------------------------------->>    user_id(foreign key, ref aut_user(id))
                                                                         TimeStamp
                                                                         