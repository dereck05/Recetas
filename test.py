"""
from pyexpert import *


def n():
    prolog = prolog_default_env()

    reglas="comidita(X,A,B):-comida(X,A,B)."

    hechos="comida(arroz,hola,adios)."


    prolog_driver(prolog,reglas,[narrate_predicates])
    prolog_driver(prolog,hechos,[narrate_predicates])


    ret, vars = prolog_driver(prolog,'? comidita(arroz,A,B).')
    print(vars)

n()


# Imports

def fn():
    # Initialise environment
    env = prolog_default_env()

    # Execute query
    ret,vars = prolog_driver(env, '? append(A, B, [x,y]).')
    print(vars)

fn()


from prologterms import TermGenerator, PrologRenderer, Program, Var, SExpressionRenderer

P = TermGenerator()
X = Var('X')
Y = Var('Y')
Z = Var('Z')
R = PrologRenderer()
S = SExpressionRenderer()
def t():
    p = Program(
        P.ancestor(X,Y) <= (P.parent(X,Z), P.ancestor(Z,Y)),
        P.ancestor(X,Y) <= P.parent(X,Z),
        P.parent('a','b'),
        P.parent('b','c'),
        P.parent('c','d')
        )
    print('PROG:\n')
    print(R.render(p))
    assert R.render(p) == "ancestor(X,b)"
    print(R.render(p))
t()
"""
from zamiaprolog.parser  import PrologParser

prolog = parser = PrologParser()
assertz