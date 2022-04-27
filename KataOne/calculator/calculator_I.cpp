#include <iostream>
#include <string>

using namespace std;


int main()
{
    int x, y, op;

    cout << "Dime el primer numero " << endl;
    cin >> x;
    cout << "Dime el segundo numero " << endl;
    cin >> y;

    cout << "Seleccione la operacion que desee realizar: " << endl;
    cout << "1. Sumar " <<endl;
    cout << "2. Restar " <<endl;
    cout << "3. Multiplicar " <<endl;
    cout << "4. Dividir " <<endl;
    cin >> op;

    switch (op)
    {
    case 1: cout << "El resultado de la suma es: " << x + y<< endl; 
        break;
    case 2: cout << "El resultado de la resta es: "<< x - y << endl; 
        break;    
    case 3: cout << "El resultado de la multiplacion es: "<< x * y << endl; 
        break;
    case 4: cout << "El resultado de la divicion es: "<< x / y << endl; 
        break;        

    }	
    return 0;
}