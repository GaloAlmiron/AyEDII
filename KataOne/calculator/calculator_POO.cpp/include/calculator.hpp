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
    int suma();
    int rest();
    int mult();
    int div();
};




#endif