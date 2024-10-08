/*
 * File:   PruevaServosPic.c
 * Author: HP
 *
 * Created on 19 de febrero de 2023, 10:40 AM
 */


#include <xc.h>
#include <string.h>
#include <stdio.h>


#pragma config FOSC = INTIO67 //OSCILADOR  INTERNO Y PINES 6 Y 7 COMO ENTRADAS Y SALIDAS
#pragma config WDTEN = OFF //PERRO GUARDIAN 
#pragma config LVP = OFF // PROGRAMACION DE BAJO VOLTAJE ;


#define _XTAL_FREQ 16000000
#define time 10

//LCD
#define CD 0x01 //Clear Display
#define RH 0x02 //(0x03) Return Home
#define EMS 0x06 //Entry Mode Set
#define DC 0x0F //(0x0E) Display Control
#define DSr 0x1C //Display Shift Rigth
#define DSl 0x18 //Display Shift Left
#define FS 0x28 //(0x3C) Function Set
#define RAW1 0x80 //DDRAM display
#define RAW2 0xC0 //DDRAM display
#define button PORTBbits.RB2 //Button start
#define RS LATEbits.LATE1 //Register Selection
#define E LATEbits.LATE0 //Enable

void settings(void);
//Interrupción
void __interrupt() TMR1_ISR(void);
void deg2time(void);
//LCD
void SettingsLCD(unsigned char word);
void WriteLCD(unsigned char word);
void LCD(unsigned char data);
void DataLCD(void);
void ClearLCD(void);
//UART
void DataUART(void);

unsigned int th, tl, a = 0, b = 0, flag = 1, i, incremento=0;
float degrees, time_high , time_low;
char text[20], servo= 'A';

void main(void) {
    settings();
   
    while (1) {
        deg2time();
        SettingsLCD(RAW1);
        sprintf(text,"Servo 2:%.5f",time_high*1000); //Angulo
        //DataUART();
        DataLCD();
        __delay_ms(500);
        TMR1ON = 1;
    }
}

void settings(void) {
    OSCCON = 0x72;
    ANSELD = 0x00;
    ANSELE = 0x00;
    ANSELC = 0x00;
    //LCD
    TRISD = 0;
    TRISE = 0;
    LATD = 0;
    LATE = 0;
        
    SettingsLCD(0x02); //Iniciar la LCD con el método nibble (4 MSB y 4 LSB)
    SettingsLCD(EMS);
    SettingsLCD(DC);
    SettingsLCD(FS);
    SettingsLCD(CD);
    
    //UART
    TRISCbits.TRISC6 = 0;
    TRISCbits.TRISC7 = 1;
    SPBRG1 = 0x19;
    RCSTA1 = 0x90;
    TXSTA1 = 0x20;
    
    //Habilitação da interrupção do TIMER 1
    GIE = 1;
    PEIE = 1;
    //Interrupciones Recepción Serial
    RC1IE = 1; //El primero de perifericas
    RC1IF = 0; //bandera
    TMR1IE = 1;
    TMR1IF = 0;
    
       
    //Configuração do TIMER1
    T1CON = 0x12; //Prescaler en 2 y 16 bits en una operación
    //deg2time(0.0);
    TMR1 = 0;
    LATD6 = 1;
    LATD7 = 1;  
    //TMR1ON = 1;
}

void __interrupt() TMR1_ISR(void) {
    unsigned char d;
    if (TMR1IF) {
        if (servo == 'A'){
            LATD7 = 0;
            if (LATD6 == 1) {
                TMR1 = th;
                LATD6 = 0;
            } else if (LATD6 == 0) {
                TMR1 = tl;
                LATD6 = 1;
            }
        }
        if (servo == 'B'){
            LATD6 = 0;
            if (LATD7 == 1) {
                TMR1 = th;
                LATD7 = 0;
            } else if (LATD7 == 0) {
                TMR1 = tl;
                LATD7 = 1;
            }
        }
        //LATD0 = ~LATD0;
        TMR1IF = 0;
    }
    
    if (RC1IF) {
        d = RCREG1;
        if (d == 'A' || d == 'B'){
            servo = d;  
        }
        
        else if (d == '0' || d == '1' || d == '2' || d == '3' || d == '4' || d == '5' || d == '6' || d == '7' || d == '8' || d == '9') {
            if (flag == 1) {
                a = d - 48;
                flag = 2;
            } 
            else  if(flag == 2){
                a = (a * 10) + (d - 48);
            }
            //Decimales
            else  if(flag == 3){
                a = a + (d-48)*0.1;
                flag = 4;
            }
            else  if(flag == 4){
                a = a + (d-48)*0.01;
                flag = 5;
            }
            
        }
        else if(d == '.'){
            flag = 3;
        }
        
        else if (d == 'O') {
            b = a;
            flag = 1;
            a = 0;
            
            if(servo == 'A'){
            
                SettingsLCD(CD);
                //deg2time((float)b);
                SettingsLCD(RAW1);
                sprintf(text,"Servo 1:%d",b); //Angulo
                //DataUART();
                DataLCD();

                SettingsLCD(RAW2);
                sprintf(text,"DC:%.2f ms",time_high*1000);
                //DataUART();
                DataLCD();
                //__delay_ms(100);
            
            
            }
            else if (servo == 'B'){
                SettingsLCD(CD);
                //deg2time((float)b);
                SettingsLCD(RAW1);
                sprintf(text,"Servo 2:%d",b); //Angulo
                //DataUART();
                DataLCD();
                SettingsLCD(RAW2);
                sprintf(text,"DC:%.2f ms",time_high*1000);
                //DataUART();
                DataLCD();
                //__delay_ms(100);
            }
        }
        
        //Recepcion SIN DECIMALES
        /*
         if (RC1IF) {
        d = RCREG1;
        if (d == 'A' || d == 'B'){
            servo = d;
        }
        
        if (d == '0' || d == '1' || d == '2' || d == '3' || d == '4' || d == '5' || d == '6' || d == '7' || d == '8' || d == '9') {
            if (flag == 1) {
                a = d - 48;
                flag = 2;
            } else {
                a = (a * 10) + (d - 48);
            }
        } else if (d == 'O') {
            //SettingsLCD(CD);
            b = a;
            flag = 1;
            a = 0;
            
        }
    
         */
    }
}

void deg2time(void) {
    //time_high = (((degrees * (1.9 / 90.0)) + 0.6))*0.001;
    time_high = 0.79*0.001;
    th = 65535.0 - (time_high / (0.00000025 * 2.0));
    time_low = 0.02 - time_high;
    tl = 65535.0 - (time_low / (0.00000025 * 2.0));
}

//void deg2time1(float degrees1) {
//    //time_high = (((degrees * (0.5 / 90.0)) + 1.0))*0.001;
//    time_high = (((degrees1 * (1.9 / 180.0)) + 0.6))*0.001;
//    th = 65535.0 - (time_high / (0.00000025 * 2.0));
//    time_low = 0.02 - time_high;
//    tl = 65535.0 - (time_low / (0.00000025 * 2.0));
//    
//}

void SettingsLCD(unsigned char word) {
    RS = 0;
    LCD(word >> 4); // 4 MSB
    LCD(word & 0x0F); // 4 LSB
}

void WriteLCD(unsigned char word) {
    RS = 1;
    LCD(word >> 4);
    LCD(word & 0x0F);
}

void LCD(unsigned char data) { //Opción bits
    E = 1;
    __delay_us(time);
    LATDbits.LATD0 = (data & 0x01);
    __delay_us(time);
    LATDbits.LATD1 = (data & 0x02) >> 1;
    __delay_us(time);
    LATDbits.LATD2 = (data & 0x04) >> 2;
    __delay_us(time);
    LATDbits.LATD3 = (data & 0x08) >> 3;
    __delay_us(time);
    E = 0;
    __delay_us(time);
}

void DataLCD(void) {
    for (i = 0; i <= strlen(text)-1; i++) {
        WriteLCD(text[i]);
    }
}

void ClearLCD(void) { //No se esta usando
    for (i = 0; i <= strlen(text); i++) {
        WriteLCD(' ');
    }
}