#include <iostream>
#include "./include/calculator.hpp"

#include <string>
#include <stdlib.h> 

using namespace std;

int main()
{
    
    Calculator* calculator = new Calculator();
    int a, b, op;
    
    cout << "Dime el primer numero: " << endl;
    cin >> a;
    cin.ignore();

    cout << "Dime el segundo numero: " << endl;
    cin >> b;
    cin.ignore();

    calculator->numbers(a, b);
    

    cout << "\nSeleccione la operacion que desee realizar: " << endl;
    cout << "1. Sumar " <<endl;
    cout << "2. Restar " <<endl;
    cout << "3. Multiplicar " <<endl;
    cout << "4. Dividir " <<endl;
    cin >> op;

    switch (op)
    {
    case 1: cout <<"Resultado: " << calculator->suma() << endl; 
        break;
    case 2: cout <<"Resultado: " << calculator->rest() << endl; 
        break; 
    case 3: cout <<"Resultado: " << calculator->mult() << endl; 
        break;
    case 4: cout <<"Resultado: " << calculator->div() << endl; 
        break;   

    }
      


    delete calculator;
    system("pause");
    return 0;
}