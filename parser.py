# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 14:04:36 2021

@author: tsfeith
"""

import numpy as np

def parser(expr, params, indep):
    """
    Parameters
    ----------
    expr : string
        Expressão dada pelo utilizador
    params : string
        Variáveis dadas pelo utilizador
    indep : string
        Nome da variável independente dada pelo utilizador

    Returns
    -------
    cleanExpr : string
        Clean expression, ready to be interpreted
    """
    np.seterr(all='raise')    
    functions = ['sin',
                 'cos',
                 'tan',
                 'exp',
                 'log']
    
    # Fazer limpeza dos params
    # Assumindo que estão separados por virgulas ou espaços
    first_split = params.split(' ')
    clean_split = []
    for val in first_split:
        for param in val.split(','):
            if param:
                clean_split.append(param)
    
    # Verificar se nenhum dos nomes das variáveis não são funções
    for val in clean_split:
        if val in functions:
            return 'O nome \''+str(val)+'\' já está associado a uma função. Dê um nome diferente.'
    
    # Aproveitar e verificar se a variável independente não é uma função
    if indep in functions:
        return 'O nome \''+str(indep)+'\' já está associado a uma função. Dê um nome diferente.'
    
    # E já agora verificar se não está nos parâmetros
    if indep in clean_split:
        return 'O nome \''+str(indep)+'\' foi dado à variável independente e a um parâmetro. Altere um deles.'
    
    # Substituir as funções pelo equivalente numpy
    # Primeira substituição temporária para não haver erros de conversão
    for function in enumerate(functions):
        expr = expr.split(function[1])
        expr = ('['+str(len(clean_split)+function[0])+']').join(expr)
    
    # Substituir os nomes dos parâmetros
    for pair in enumerate(clean_split):
        expr = expr.split(pair[1])
        expr = ('B['+str(pair[0])+']').join(expr)
    
    # Substituir a variável independente
    expr = expr.split(indep)
    expr = 'x'.join(expr)
    
    # Voltar a substituir os elementos pelas funções
    for function in enumerate(functions):
        expr = expr.split('['+str(function[0]+len(clean_split))+']')
        expr = ('np.'+str(function[1])).join(expr)

    # Vamos finalmente testar se a função funciona
    B = []
    for val in clean_split:
        B.append(np.pi/2)
    x=-1
    try:
        eval(expr)
    except NameError as error:
        return 'A função \''+str(error).split('\'')[1]+'\' não foi reconhecida.'
    except FloatingPointError:
        return expr
    except SyntaxError:
        return 'Não foi possível compilar a sua expressão. Verifique se todos os parâmetros estão definidos e a expressão está escrita corretamente.'

    return expr
    
if __name__=='__main__':
    print(parser('a+b*sin(c*t+d)+e*cos(f*t+g)+h*tan(i*t+j)', 'a, b, c, d, e, f, g, h, i, j','t'))
    