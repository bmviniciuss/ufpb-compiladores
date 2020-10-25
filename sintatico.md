# Gramatica

## Programa

> programa -> 

**program** id;

declarações_variáveis

declarações_de_subprogramas

comando_composto

.

## declarações_variáveis
>declarações_variáveis ->

**var** lista_declarações_variáveis
 | ε

## lista_declarações_variáveis
> lista_declarações_variáveis →

lista_declarações_variáveis lista_de_identificadores: tipo;

| lista_de_identificadores: tipo; 

**Remover recursão à esquerda:**

> lista_declarações_variáveis →

lista_de_identificadores: tipo; lista_declarações_variáveis_2

> lista_declarações_variáveis_2 →

lista_de_identificadores: tipo; lista_declarações_variáveis_2
| ε
