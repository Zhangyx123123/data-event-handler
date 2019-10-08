import json


def get_abstract(expr):
    abstract = []
    if validate_expression(expr):
        for operand in expr['operands']:
            op1 = operand['operand1']['path'].split('.')[-1]
            op = operand['op']
            op2 = operand['operand2']
            if op == 'rewrite':
                abstract.append('{}符合正则【{}】并重写'.format(op1, translate_op(op), op2))
            elif op == 'in' or op == 'nin':
                abstract.append('{}{}【{}】'.format(op1, translate_op(op), ', '.join(map(str, op2))))
            else:
                abstract.append('{}{}【{}】'.format(op1, translate_op(op), op2))
    return abstract


def translate_op(op):
    return {
        'gt': '大于',
        'gte': '不小于',
        'lt': '小于',
        'lte': '不大于',
        'eq': '等于',
        'neq': '不等于',
        'in': '包含于',
        'nin': '不包含于',
        'regex': '符合正则',
        'rewrite': '符合正则'
    }[op]


def validate_expression(expr):
    if expr['op'] != 'and':
        return False
    for operand in expr['operands']:
        if 'operand1' not in operand or 'operand2' not in operand:
            return False
        if not isinstance(operand['operand1'], dict) or isinstance(operand['operand2'], dict):
            return False
        if operand['operand1']['op'] != 'select':
            return False
    return True
