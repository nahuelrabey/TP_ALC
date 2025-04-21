#let ga = $alpha$
#import "@preview/physica:0.9.5": *

== Ejercicio 1
$
  &va(p) = (1-ga)C va(p) +  ga/N va(1)\
  &va(p)-(1-ga)C va(p) = ga/N va(1)\
  &(I-(1-ga)C)va(p) = ga/N va(1)\
  &N/ga (I-(1-ga)C)va(p) = va(1)\
$

Luego, nuestra matriz nos queda 
$
&M=N/ga (I-(1-ga)C)\
&b=va(1)
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
=== b) 
¿Se cumplen estas condiciones para la matriz M tal cómo fue construida para los Museos cuando \ $0<ga<1$? Demuestre que se cumplen o de un contraejemplo.

Buscamos que $M$ sea inversible entre $0<ga<1$, es decir $0<(1-ga)<1$. Para que esto ocurra, al menos, $det((I-(1-ga)C)) != 0$. Para estudiar este problema, llamaremos $W$ a la matriz $(I-(1-ga)C)$

Cómo $C$ es estocástica, y su diagonal son ceros, entonces $0 <= (1-ga)C_(i j) < 1" " forall i,j$ pues $C_(i j) <= 1$. Además también se cumple que $sum_(i=1)^(n)(C_(i j)) = 1 " " forall j$. Por lo tanto $sum_(i=1)^(n)((ga-1)C_(i j)) <= 1$

Luego, $W=(I-(1-ga)C)$ cumple las siguientes propiedades: 
- $w_(i j) = - (1-ga)C_(i j) < 0 " " forall i!=j$
- $abs(w_(i j)) = (1-ga)C_(i j) " " forall i!=j$.
- $W_(i i) = 1 " " forall i$. 

Por lo tnato $sum_(1<=i, i!=j)^(n) abs(W_(i j)) <= 1 = W_(i j)$, tenemos una matriz diagonalmente fuerte, es decir inversible en $0 <(1-ga)< 1$

Veamos que ocurre en los extremos.\
Si $alpha -> 0$ entonces $N/ga -> +infinity$. Además, tenemos que $det(I-(1-ga)C)!=0$ por la demostración anterior. Luego
$
&(N/ga)^N det((I-C))->_(ga->infinity) infinity
$
Entonces, no importa que tanto $ga$ se acerque al 0, siempre será inversible.

Si $ga -> 1$ podemos reemplazar fácilmente:
$
  lim_(ga -> 1)(N/ga)^N det((I-(1-ga)C)) = N^N det(I) = N^N != 0
$

Por lo tanto, se cumplen las condiciones cuando $0 < ga < 1$

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

