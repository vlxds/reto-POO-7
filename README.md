# reto-POO-7
## Implementación de decoradores en el reto 5 de la clase de programación orientado a objetos.

Este proyecto contiene las modificaciones solicitadas del reto 7 teniendo como base el trabajo realizado en el reto 5, estas modificaciones son las siguietnes:

* Utilización del decorador @property en los metodos creados en el modulo shape.py en el programa Shape 2 con el objetivo de tener un codigo mas simple, limpio y con mejores practicras de programación.

* Utilización del decorador @classmethod en el modulo shape.py para que resiviera las clases derivas de Rectangle, Triangle y Square, esto para poder cambiar el tipo de figura.

* Creación de decorador personalizado @timeit que tiene el objetivo de medir el tiempo que se demora en ejecutar el metodo compute_area() del modulo triangle.py para luego imprimir un mensaje mostrando el resultado.

Ahora se va explicar que se hizo exactamente.

## Modulo shape.py
El primer cambio que se realizó fue proteger todos los atributos de la clase Shape para que solamente puedan ser leidos con el decorador @property, esto se realiza para tener las ventajas de impedir que se modifiquen los atributos, tener una interfaz más limpia y exponer la información interna sin afectar el encapsulamiento.

```python
@property
def vertices(self):
    return self._vertices
```

Cada metodo simplemente muestra el atributo restringido para que luego, estos datos internos, sean empleados por las clases derivadas de la clase Shape.

El segundo cambio que se realizó fue la implementación del decorador @classmethod que permite definir y cambiar el tipo de figura desde el modulo shape.py donde se encuentra la clase Shape que es la clase base.

```python
@classmethod
def set_shape_type(cls, new_type):
    cls.shape_type = new_type
```

## Modulo triangle.py
En este modulo se creo un decorador personalizado llamado @timeit, el cual es el siguiente:

```python
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end - start:.6f} segundos")
        return result
    return wrapper
```

Este decorador funciona de la siguiente manera:
1.  Recibe el metodo (función) compute_area() como parametro.
2. Luego se crea una función interna que puede recibir una cantidad indefinida de argumentos.
3. A continuación, en la variables start, se guarda el tiempo en el que inicio la ejeción del metodo.
4. Despues, ejecuta la función que se ingreso como parametro en el decorador y lo guarda en la variable resultados.
5. Luego, en la variable end, guarda el tiempo en el que finaliza el metodo compute_area().
6. Lo siguente que sucede es que se imprime un mensaje indicando el tiempo que se demoró la ejecución del metodo.
7. para finalizar retorna el la variable resultado y el decorador retorna el metodo modificado
