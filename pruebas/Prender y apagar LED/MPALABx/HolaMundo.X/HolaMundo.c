/*
 * File:   main.c
 * Author: user
 *
 * Created on 18 de Fevereiro de 2020, 11:30
 */

#include <xc.h>
#include <stdio.h>
#include <string.h>
#pragma config FOSC = INTIO67 //OSCILADOR  INTERNO Y PINES 6 Y 7 COMO ENTRADAS Y SALIDAS
#pragma config WDTEN = OFF //PERRO GUARDIAN 
#pragma config LVP = OFF // PROGRAMACION DE BAJO VOLTAJE ;

#define _XTAL_FREQ 16000000  //CONSTANTE FRECUENCIA DE OSCILACION 
#define time 10

void main(void) {
    OSCCON = 0x72;
    ANSELB = 0x00;
    TRISB = 0x00;
    LATB = 0x00;
  
    while(1){
        //LATB = 0x03; //(outro exemplo: PORTA = 0b00000001 ou RA0 = 1;)
        LATBbits.LATB1 = 1;
        __delay_ms(1000);
        //LATA = 0x00; //(outro exemplo: PORTA = 0b00000000 ou RA0 = 0;)
        LATBbits.LATB1 = 0;
        __delay_ms(1000);
    }
}