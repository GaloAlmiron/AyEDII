#include "../include/calculator.hpp"

Calculator::Calculator(){}


void Calculator::numbers(int _x, int _y)
{
    x = _x;
    y = _y;
}

int Calculator::add()
{
    return x + y;
}

int Calculator::subtract()
{
    return x - y;
}

int Calculator::multiply()
{
   return x * y; 
}

int Calculator::divide()
{
    return x / y;
}

Calculator::~Calculator(){}