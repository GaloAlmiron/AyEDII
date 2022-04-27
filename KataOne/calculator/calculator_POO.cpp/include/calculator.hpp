#ifndef CALCULATOR_HPP
#define CALCULATOR_HPP

class Calculator
{
private:
    int x;
    int y;
public:
    Calculator();
    ~Calculator();
    void numbers(int _x, int _y);
    int add();
    int subtract();
    int multiply();
    int divide();
};




#endif