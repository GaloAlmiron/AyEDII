#include "../include/calculator.hpp"

Calculator::Calculator(){}


void Calculator::numbers(int _x, int _y)
{
    x = _x;
    y = _y;
}

int Calculator::suma()
{
    return x + y;
}

int Calculator::rest()
{
    return x - y;
}

int Calculator::mult()
{
   return x * y; 
}

int Calculator::div()
{
    return x / y;
}

Calculator::~Calculator(){}