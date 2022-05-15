import time

dic_function_time = {}


def store_time(function):
    """Décorateur qui stocke le nombre de secondes écoulées
     entre le début et la fin de l'exécution de la fonction.

     Un décorateur est une fonction qui prend une autre fonction (ou classe) en paramètre
     pour modifier son comportement lors de son exécution."""

    def modified_function(*args, **kwargs):
        """On est dans la fonction modifiée qui a pour but de
         calculer et stocker le temps d'exécution de 'function' dans le dictionnaire.
         'function' est bien accessible dans ce bloc étant
         dans la définition de 'store_time'.

        :param args: tuple des paramètres non nommés (arguments).
        :param kwargs: dictionnaire des paramètres nommés (key word arguments).
        """

        t1 = time.time()
        value_returned = function(*args, **kwargs)
        t2 = time.time()
        elapsed_time = t2 - t1

        if function not in dic_function_time:
            dic_function_time[function] = [elapsed_time]
        else:
            dic_function_time[function].append(elapsed_time)

        # On retourne dans 'modified' la valeur retournée de 'function' (2)
        return value_returned

    # On retourne dans 'store_time' la fonction 'modified_function' (1)
    return modified_function


"""
NUMEROS = ORDRE EXECUTION 

Les décorateurs ne sont pas magiques, dans notre cas, considérons le cas suivant :

@store_time
def function(a, b, c):
    return a, b, c

Le décorateur ne fait rien d'autre que ça : modified_function = store_time(function)
(Vu que store_time retourne 'modified_function') 

function est en fait remplacée par modified_function et puisqu'on a défini plus haut
'def modified_function(*args, **kwargs)' on peut lui passer les paramètres a b et c comme si c'était 'function'.

Donc dans ce cas à chaque fois qu'on fait function(1, 2, 3) on exécute en fait store_time(function)(1, 2, 3)
c'est à dire modified_function(1, 2, 3) (Vu que store_time retourne 'modified_function') 

On calcule le temps d'exécution de 'function' en pensant bien à récupérer la sortie (value_returned) de 'function'
et afin de ne pas altérer son fonctionnement on retourne value, c'est à dire ce qu'aurait dû retourner 'function' 
à la fin de son exécution.

Donc à la fin on a juste ajouté une fonctionnalité à notre fonction avec notre fonction 'store_time'.

==> C'est le but d'un décorateur 

Si on veut ajouter des paramètres à store_time il faut rajouter une couche de fonction :
"""


def store_time2(min_time):
    def decorator(function):

        def modified_function(*args_function, **kwargs_function):
            t1 = time.time()
            value_returned = function(*args_function, **kwargs_function)
            t2 = time.time()
            elapsed_time = t2 - t1

            if elapsed_time >= min_time:
                if function not in dic_function_time:
                    dic_function_time[function] = [elapsed_time]
                else:
                    dic_function_time[function].append(elapsed_time)

            # On retourne dans 'modified'_function la valeur retournée de 'function'(3)
            return value_returned

        # On retourne dans 'decorator' la fonction 'modified_function' pour s'en servir (2)
        return modified_function

    # On retourne dans 'store_time2' notre fonction decorateur (1)
    return decorator


"""
Cela revient alors au même que de faire modified_function = store_time2(1)(function)
(Uniquement les durées de chaque exécution >= 1 seront stockées)

Puis si on exécute store_time2(1)(function)(1, 2, 3) c'est à dire : decorator(function)(1, 2, 3),
(en gardant à l'esprit qu'on a accès à min_time puisqu'on est toujours dans la définition de 'store_time2')
c'est à a dire modified_function(1, 2, 3).


"""
