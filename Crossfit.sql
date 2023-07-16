create table dieta (
dieta_id serial primary key,
nombre varchar(50),
descripcion varchar(150),
forma_dieta varchar(500),
calorias_total varchar(15));


create table rutina(
rutina_id serial primary key,
nombre varchar(30),
descripcion varchar(150),
series int,
repeticion varchar(100),
tiempo_descanso varchar(50));


create table instructor(
instructor_id serial primary key,
nombre varchar(50),
apellido varchar(50),
correo varchar(50),
edad int,
Genero varchar(50),
telefono varchar(10),
rutina_id  serial constraint instructor_rutina_id_fk references rutina (rutina_id) 
   ON DELETE RESTRICT ON UPDATE CASCADE,
dieta_id serial constraint instructor_dieta_id_fk references dieta (dieta_id) 
   ON DELETE RESTRICT ON UPDATE CASCADE);


create table cliente(
cliente_id serial primary key,
nombre varchar(50),
apellido varchar(50),
correo varchar(50),
edad int,
genero varchar(10),
telefono varchar(10),
rutina_id serial constraint cliente_rutina_id_fk references rutina (rutina_id) 
	ON DELETE RESTRICT ON UPDATE CASCADE,
dieta_id serial constraint cliente_dieta_id_fk references dieta (dieta_id)
	ON DELETE RESTRICT ON UPDATE CASCADE);
	
create table registro_cliente(
resgistro_cliente_id serial primary key,
usuario varchar(40),
contrasena varchar(20),
cliente_id serial constraint registro_cliente_id_fk references cliente (cliente_id)
   ON DELETE RESTRICT ON UPDATE CASCADE);
   
   
create table registro_instructor(
resgistro_instructor_id serial primary key,
usuario varchar(40),
contrasena varchar(20),
instructor_id serial constraint registro_instructor_id_fk references instructor (instructor_id)
   ON DELETE RESTRICT ON UPDATE CASCADE);

create table crossfit(
crossfit_id serial primary key,
nombre varchar(50),
direccion varchar(50),
telefono varchar(10),
instructor_id serial constraint crossfit_instructor_id_fk references instructor (instructor_id)
     ON DELETE RESTRICT ON UPDATE CASCADE,
usuario_id serial constraint crossfit_cliente_id_fk references cliente (cliente_id)
	ON DELETE RESTRICT ON UPDATE CASCADE);


insert into rutina (nombre,descripcion,series,repeticion,tiempo_descanso) values('Fran','Combinación de thrusters (sentadillas frontales seguidas de una prensa de hombros) y pull-ups (dominadas)','3',
	'1-15-9 (21 thrusters, 21 pull-ups, 15 thrusters, 15 pull-ups, 9 thrusters, 9 pull-ups)','3-5 minutos entre series');
insert into rutina (nombre,descripcion,series,repeticion,tiempo_descanso) values('Cindy','AMRAP (tantas rondas como sea posible) de 20 minutos de pull-ups, push-ups (flexiones) y air squats (sentadillas sin peso)',
	'5','5 pull-ups, 10 push-ups, 15 air squats','Descanso mínimo entre rondas');
insert into rutina (nombre,descripcion,series,repeticion,tiempo_descanso) values('Grace','Levantamiento de peso olímpico - Clean and Jerk (arranque y envión) a alta intensidad',
	'1','30 Clean and Jerks','Descanso mínimo necesario entre repeticiones');	

	
insert into dieta (nombre,descripcion,forma_dieta,calorias_total) values('Energía explosiva','Dieta diseñada para atletas de CrossFit que buscan aumentar la energía explosiva y la resistencia',
	' Esta dieta se basa en una combinación de proteínas magras, carbohidratos complejos, grasas saludables y verduras. Se recomienda consumir porciones adecuadas de cada grupo de alimentos para mantener un equilibrio nutricional. Por ejemplo, una comida puede consistir en pechuga de pollo a la parrilla con una porción de arroz integral, brócoli al vapor y aguacate en rodajas. Las nueces y las batatas también se pueden consumir como meriendas o acompañamientos adicionales',
	'2500 kcal');
insert into dieta (nombre,descripcion,forma_dieta,calorias_total) values('Recuperación y reparación','Dieta enfocada en la recuperación muscular y la reparación del tejido después de los entrenamientos intensos de CrossFit',
	'Esta dieta se centra en alimentos que apoyan la recuperación muscular y la reparación del tejido. Se recomienda consumir fuentes de proteínas magras como el salmón, carbohidratos complejos como la quinoa, verduras de hoja verde como las espinacas y frutas variadas para obtener antioxidantes. Los batidos de proteínas y el yogur griego pueden ser una opción conveniente para obtener proteínas después de los entrenamientos',
	'2000 kcal');
insert into dieta (nombre,descripcion,forma_dieta,calorias_total) values('Rendimiento óptimo','Dieta diseñada para maximizar el rendimiento en los entrenamientos de CrossFit, proporcionando los nutrientes necesarios para la fuerza y resistencia',
	'Esta dieta se basa en una combinación de proteínas magras, carbohidratos de calidad y grasas saludables. Se recomienda consumir carnes magras como el filete, patatas al horno, zanahorias, huevos, nueces, aguacate y plátanos para obtener energía y nutrientes esenciales. Se pueden hacer comidas equilibradas con porciones adecuadas de cada alimento para satisfacer las necesidades energéticas y de rendimiento',
	'3000 kcal');


insert into instructor (nombre,apellido,correo,edad,genero,telefono) values('Diego','Cedeño','DiegoCed@gmail.com','28','Masculino','0997856428');
insert into instructor  (nombre,apellido,correo,edad,genero,telefono) values('Maria','Zambrano','ZambranoM25@gmail.com','25','Femenino','0968375427');


insert into cliente (nombre,apellido,correo,edad,genero,telefono) values ('Deivy','Cedeño','deivy14@gmail.com','21','Masculino','0998542376');


insert into registro_cliente (usuario,contrasena) values ('deivy','1234');


insert into registro_instructor (usuario,contrasena) values ('diego','1234');
insert into registro_instructor (usuario,contrasena) values ('maria','1234');

insert into crossfit (nombre, direccion, telefono) values('crossfit','Calle 8 Avenida 10','0968574217');

