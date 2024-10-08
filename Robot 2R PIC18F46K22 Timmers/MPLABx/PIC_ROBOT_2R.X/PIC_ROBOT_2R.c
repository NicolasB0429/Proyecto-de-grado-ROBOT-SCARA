/*
 * File:   PIC_ROBOT_2R.c
 * Author: tetri
 *
 * Created on 12 de julio de 2022, 09:18 PM
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

void deg2time1(float degrees);
void deg2time2(float degrees);

//LCD
void SettingsLCD(unsigned char word);
void WriteLCD(unsigned char word);
void LCD(unsigned char data);
void DataLCD(void);

void ClearLCD(void);
//UART
void DataUART(void);

unsigned int th1, tl1, th2, tl2, flag = 1, i, incremento=0, confir = 0, confir1 = 0;
float degrees1, degrees2, time_high, time_low, a = 0.0, b = 0, c = 0;
char text[20], servo;

void main(void) {
    settings();
   
    while (1) {
        
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
    PEIE = 1; //Perfericas
    //Interrupciones Recepción Serial
    RC1IE = 1; //HABILITAR UART 1
    RC1IF = 0; //bandera
    
    //TIMER 1
    TMR1IE = 1; // Registro PIE1 (interrupt overflow)
    TMR1IF = 0;  
    //TIMER 3
    TMR3IE = 1; // Registro PIE2 (interrupt overflow)
    TMR3IF = 0;  
    
    //Configuracion de TIMER1
    T1CON = 0x12; //Prescaler en 2 y 16 bits en una operación timer 1 y 3
    T3CON = 0x12;
    deg2time1(0.0); // Funcion Calculo de tiempos
    TMR1 = 0; // COMIENZA DESDE 0
    deg2time2(0.0);
    TMR3 = 0;
    LATD6 = 1;
    LATD7 = 1;      
    TMR1ON = 1;
    TMR3ON = 1;
}

void __interrupt() TMR1_ISR(void) {
    unsigned char d;

    if (TMR1IF) {
        if (confir == 1){
            if (LATD6 == 1) {
                TMR1 = th1;                
                LATD6 = 0;
                
            } else if (LATD6 == 0) {
                TMR1 = tl1;
                LATD6 = 1;
            }        
        TMR1IF = 0;
        }
    }
    
    if (TMR3IF) {
        if (confir == 1){
            if (LATD7 == 1) {
                TMR3 = th2;                
                LATD7 = 0;
                
            } else if (LATD7 == 0) {
                TMR3 = tl2;
                LATD7 = 1;
            }        
        TMR3IF = 0;
        }
    }    
    
    if (RC1IF) {
        d = RCREG1;
                
        if (d == 'A' || d == 'B'){
            servo = d;  
            confir = 0;
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
            //SettingsLCD(CD);
            if (servo == 'A'){
                b = a;
            }
            else if(servo == 'B'){
                c = a;
            }            
            flag = 1;
            a = 0.0;   
        }
        //Confirmacio Total
        else if (d == 'K'){
            deg2time1((float)b);
            deg2time2((float)c);
            // Servo 1
            SettingsLCD(CD);
            //deg2time1((float)b);
            SettingsLCD(RAW1);
            sprintf(text,"Servo 1:%.2f",b); //Angulo
            DataLCD(); //Escribe LCD
            
            //__delay_us(5);
            // Servo 2
            //deg2time2((float)c);
            SettingsLCD(RAW2);
            sprintf(text,"Servo 2:%.2f",c); //Angulo
            DataLCD();               
                 
        
            confir = 1;
            
        }
        
    }
   
}

//TIMER 1 Servo 1
void deg2time1(float degrees1) {
    //time_high = (((degrees * (0.5 / 90.0)) + 1.0))*0.001;
    time_high = (((degrees1 * (1.9 / 180.0)) + 0.6))*0.001;
    th1 = 65535.0 - (time_high / (0.00000025 * 2.0));
    time_low = 0.02 - time_high;
    tl1 = 65535.0 - (time_low / (0.00000025 * 2.0));
    
}

//TIMER 3 Servo 2
void deg2time2(float degrees2) {
    //time_high = (((degrees * (0.5 / 90.0)) + 1.0))*0.001;
    time_high = (((degrees2 * (1.9 / 180.0)) + 0.6))*0.001;
    th2 = 65535.0 - (time_high / (0.00000025 * 2.0));
    time_low = 0.02 - time_high;
    tl2 = 65535.0 - (time_low / (0.00000025 * 2.0));
}


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
