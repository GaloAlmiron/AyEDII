:: Compilo c+odigo objeto
g++ -Wall -std=c++11 -c .\src\calculator.cpp 
g++ -Wall -std=c++11 -c main.cpp 

:: Compilo el Binario
g++ calculator.o main.o -o calculator.exe

:: Limpio los códigos objeto
DEL .\*.o