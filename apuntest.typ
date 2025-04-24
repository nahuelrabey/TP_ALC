#let ga = $alpha$
#import "@preview/physica:0.9.5": *

== Ejercicio 1
$
  &va(p) = (1-ga)C va(p) +  ga/N va(1)\
  &va(p)-(1-ga)C va(p) = ga/N va(1)\
  &(I-(1-ga)C)va(p) = ga/N va(1)\
  &N/ga (I-(1-ga)C)va(p) = va(1)\
$

Luego, nos queda la siguiente ecuación matricial.
$
&M=N/ga (I-(1-ga)C)\
&b=va(1)\
&M va(p) = va(1)
$

== Ejercicio 2
=== a) 
¿Qué condiciones se deben cumplir para que exista una solución única a la ecuación del punto anterior?

La matriz debe ser inversible. Por lo tanto queremos ver que $det(M)!=0$, es decir
$
&det(N/ga (I-(1-ga)C))!=0\
&(N/ga)^N det((I-(1-ga)C))!=0
$

Si $ga = 1$ tenemos que $1 - ga = 0$ y nuestra expresión se reduce a
$
&(N)^N det(I-(0)C)=(N)^N det((I))=(N)^N
$
Cómo $N in NN_(>=1)$, para cualquier cantidad de museos tenemos que $N^N != 0$, y por lo tanto \ $det(M)!=0$

Si $ga = 0$ no se cumple la ecuación anterior pues $N\/0$ es indefinido.
#pagebreak()
=== b) 

Caso $0 <ga < 1$, 

Supongamos que $I-(1-ga)C$ no es inversible, entonces existe $va(x) in RR^n: va(x)!=va(0)$ tal que 
$
  &(I-(1-ga)C)va(x) = 0\
  &va(x)-(1-ga)C va(x) = 0\
  &va(x) = (1-ga)C va(x)\
$
Aplico norma 1 a ambos lados
$
  &va(x) = (1-ga)C va(x)\
  &norm(va(x))_1 = norm((1-ga)C va(x))_1\
  &norm(va(x))_1 <= abs(1-ga)norm(C)_1 norm(va(x))_1\
$
Cómo $norm(C)_1 = 1$, pues C es estocástica, y además ($0<ga<1$)
$
  &norm(va(x))_1 <= (1-ga)norm(va(x))_1\
  &norm(va(x))_1 - (1-ga)norm(va(x))_1 <= 0\
  &ga norm(va(x))_1 <= 0\
$
Cómo $ga != 0$
$
  &norm(va(x))_1 <= 0\
$
Esto ocurre sí, y sólo sí, $va(x) = 0$, llegando a un absurdo.

Por lo tanto $(I-(1-ga)C)$ es inversible, entonces
$
  det(M) = det(N/ga (I-(1-ga)C)) = (N/ga)^N det(I-(1-ga)C)
$
con $(N/ga)^N!=0$ y $det(I-(1-ga)C)!=0$. Es decir
$
  det(M) != 0
$
Con lo cual la matriz $M$ es inversible y existe solución única para
$
  M va(p) = va(1)
$
=== Punto 4.

Si la matriz $C^k$ representa la probabilidad de que un visitante vaya a un determinado museo, entonces dados dos vectores $v,w$ tales que

$
  w = C v + v
$

Decimos que $v_i$ tiene la información de cuantos visitantes hay en el museo $i$, y $w_i$ tendrá la información de cuantos visitantes habrá en el siguiente. Luego

$
  w = C^2 v + C v + C^0 v
$

Ahora $w_i$ almacena la información de la cantidad de visitantes que tendrá cada museo en el tercer paso. (tomamos $C^0$ cómo el primero).

$
  w = C^(r-1)v + dots + v + C v + C^0 v
$
Ahora $w_i$ almacena la información de la cantidad de visitantes que tendrá cada museo en el $r-$paso.

Lo anterior es lo mismo que decir

$
  &w = sum_(k=0)^(r-1) C^k v\
  &w = (sum_(k=0)^(r-1) C^k) v\
$
Luego, si decimos que $B=sum_(k=0)^(r-1) C^k$ nos podemos quedar con la siguiente ecuación.
$
  &w = B v\
$

Finalmente la siguiente es una buena aproximación a la cantidad de visitantes que tuvo inicialmente cada museo.
$
  &v = B^(-1) v\
$

