/*
 * File:   PIC18F46K22_PCA9685_ROBOR_2R
 * Author: Angie Mancipe y Nicolas Barrera
 *
 * Created on 31 de Octubre de 2022, 09:03 AM
 */

#include <xc.h>
#include <string.h>
#include <stdio.h>

#pragma config FOSC = INTIO67 //OSCILADOR  INTERNO Y PINES 6 Y 7 COMO ENTRADAS Y SALIDAS
#pragma config WDTEN = OFF //PERRO GUARDIAN 
#pragma config LVP = OFF // PROGRAMACION DE BAJO VOLTAJE ;

#define _XTAL_FREQ 16000000
#define time2 10 //LCD
#define time 100 //I2C

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

//PCA9685
#define SlaveAddress1 0xA0 //Direccion servo 1
#define SlaveAddress2 0xA2 //Direccion servo 2

#define Frequencia 50 // VALOR DA FREQUENCIA DO SERVO en Hz
#define I2C_ADDRESS_PCA9685 0x80 //Creo que es la direcion de la PCA
#define SERVOMIN 110 // VALOR PARA UM PULSO MAIOR QUE 1 mS
#define SERVOMAX 510 // VALOR PARA UM PULSO MENOR QUE 2 mS
#define PWM_Frequencia 1000
//Registros
#define PCA9685_MODE1 0x00 /**< Mode Register 1 */
#define PCA9685_PRESCALE 0xFE /**< Prescaler for PWM output frequency */
//Datos
#define FREQUENCY_CALIBRATED 26075000 /**< Oscillator frequency measured at 104.3% */
#define MODE1_AI 0x20 /**< Auto-Increment enabled */
#define PCA9685_PRESCALE_MIN 3 /**< minimum prescale value */
#define PCA9685_PRESCALE_MAX 255 /**< maximum prescale value */
#define MODE1_SLEEP 0x10 /**< Low power mode. Oscillator off */
#define MODE1_RESTART 0x80 /**< Restart enabled */

#define PCA9685_LED0_ON_L 0x06 /**< LED0 output and brightness control byte 0 */

void settings(void);
//Interrupción
void __interrupt() TMR1_ISR(void);

//LCD
void SettingsLCD(unsigned char word);
void WriteLCD(unsigned char word);
void LCD(unsigned char data);
void DataLCD(void);
void ClearLCD(void);

//UART
void DataUART(void);

//PCA9685
void writeI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes); //*=puntero(direccion de memoria)
void writeI2C1(unsigned char Address, unsigned char Register, unsigned char Data); //*=puntero(direccion de memoria)
void startI2C(void); //empieza la comunicación
void readyI2C(void); //evita colicion de datos
void sendI2C(unsigned char data);
void stopI2C(void);
void readI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes);
void readI2C1(unsigned char Address, unsigned char Register, unsigned char Data, int bytes);
void repeatedStart(void);
unsigned char receiveI2C(char flag);

unsigned int flag = 1, i, confir = 0;
float a = 0.0, b = 0, c = 0;
char text[20], servo;

//PCA9685 variables
int map(int x, int In_Min, int In_Max, int Out_Min, int Out_Max);
void setPWMFreq(float freq);
int pos, DriverPin1 = 0, DriverPin2 = 0, led = 0;
unsigned char data1, data2[4], data3[4];


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
    
    GIE = 1; // habilitacion de interrupciones
    PEIE = 1; //Perfericas
    
    //Interrupciones Recepción Serial
    RC1IE = 1; //HABILITAR UART 1
    RC1IF = 0; //bandera
    
    //PCA9685
    TRISCbits.RC3 = 1;
    TRISCbits.RC4 = 1;
    //Configurar pines de comunicacion I2C
    SSP1STAT = 0x80;
    SSP1CON1 = 0x28;
    SSP1CON2 = 0x00;
    SSP1CON3 = 0x00;
    SSP1ADD = 0x27;
    
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, MODE1_RESTART);
    __delay_ms(10);
    //// set a default frequency
    setPWMFreq(PWM_Frequencia);
    //// set a servo frequency
    setPWMFreq(Frequencia);
    __delay_ms(300);
    
    // PINES DE LOS SERVOS
    LATD6 = 1; 
    LATD7 = 1;      
}

void __interrupt() TMR1_ISR(void) {
    unsigned char d;

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
            // Servo 1
            SettingsLCD(CD);
            SettingsLCD(RAW1);
            sprintf(text,"Servo 1:%.2f",b); //Angulo
            DataLCD(); //Escribe LCD
            
            // Servo 2
            SettingsLCD(RAW2);
            sprintf(text,"Servo 2:%.2f",c); //Angulo
            DataLCD();  
            
            data2[0] = 0;
            data2[1] = 0;

            DriverPin1 = 0;
            pos = map(b, 0, 180, SERVOMIN, SERVOMAX);
            data2[2] = pos;
            data2[3] = pos >> 8;
            //void_write2(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + 4 * DriverPin, 0, pos);
           
            //__delay_ms(100);

            //Servo 2
            DriverPin2 = 1;
            pos = map(c, 0, 180, SERVOMIN, SERVOMAX);
            data3[2] = pos;
            data3[3] = pos >> 8;
            //void_write2(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + 4 * DriverPin, 0, pos);
            writeI2C(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + (4 * DriverPin1), data2, 4);//Servo1
            writeI2C(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + (4 * DriverPin2), data3, 4);//Servo2
            //__delay_ms(100);
        }
    }
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
    __delay_us(time2);
    LATDbits.LATD0 = (data & 0x01);
    __delay_us(time2);
    LATDbits.LATD1 = (data & 0x02) >> 1;
    __delay_us(time2);
    LATDbits.LATD2 = (data & 0x04) >> 2;
    __delay_us(time2);
    LATDbits.LATD3 = (data & 0x08) >> 3;
    __delay_us(time2);
    E = 0;
    __delay_us(time2);
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

//FUNCIONES I2C
void writeI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes) {
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    for (i = 0; i < bytes; i++) {
        sendI2C(*Data);
        Data++;
    }
    stopI2C();
    //__delay_ms(time);
}

void startI2C(void) {
    readyI2C();
    SSP1CON2bits.SEN = 1; //coloca en ILDE
}

void readyI2C(void) {
    while ((SSP1CON2 & 0x1F) || (SSP1STAT & 0x04)); //SSPSTAT = ESTA TRANSMITIENDO INFORMACION//SSPCON2 = ver datasheet 
}

void sendI2C(unsigned char data) {
    readyI2C();
    SSP1BUF = data;
}

void stopI2C(void) {
    readyI2C();
    SSP1CON2bits.PEN = 1;
}

/*void readI2C(unsigned char Address,unsigned char Register,unsigned char *Data,int bytes){
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    repeatedStart();
    sendI2C(Address|0x01);
    //settingsLCD(RAW1);
    for(i=0;i<bytes;i++){
        if(i+1 == bytes){
 *Data = receiveI2C(1);
        }
        else{
 *Data = receiveI2C(0);
        }
        //WriteLCD(*Data);
        Data++;
    }
    //settingsLCD(CD);
    stopI2C();
    __delay_ms(time);
}
 */
void repeatedStart(void) {
    readyI2C();
    SSP1CON2bits.RSEN = 1;
}

unsigned char receiveI2C(char flag) {
    unsigned char buffer;
    readyI2C();
    SSP1CON2bits.RCEN = 1;
    readyI2C();
    buffer = SSP1BUF;
    readyI2C();
    SSP1CON2bits.ACKDT = flag == 1 ? 1 : 0;
    SSP1CON2bits.ACKEN = 1;
    readyI2C();
    return buffer;
}
void setPWMFreq(float freq) {
    // Range output modulation frequency is dependant on oscillator
    if (freq < 1) freq = 1;
    if (freq > 3500) freq = 3500; // Datasheet limit is 3052=50MHz/(4*4096)
    /*
    freq *= 0.9; // Correct for overshoot in the frequency setting (see issue #11)
    float prescaleval = FREQUENCY_OSCILLATOR;
     */
    unsigned long prescaleval = FREQUENCY_CALIBRATED;
    prescaleval /= freq; // required output modulation frequency
    // rounding to nearest number is equal to adding 0,5 and floor to nearest number
    prescaleval += 2048;
    prescaleval /= 4096;
    prescaleval -= 1;
    if (prescaleval < PCA9685_PRESCALE_MIN) prescaleval = PCA9685_PRESCALE_MIN;
    if (prescaleval > PCA9685_PRESCALE_MAX) prescaleval = PCA9685_PRESCALE_MAX;
    unsigned char prescale = (unsigned char) prescaleval;
    readI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, data1, 1);
    //Serial.print("data");Serial.println(data[0],HEX);//arduino
    unsigned char newmode = (data1 & ~MODE1_RESTART) | MODE1_SLEEP; // sleep
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, newmode); // go to sleep
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_PRESCALE, prescale); // set the prescaler
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, data1);
    __delay_ms(5);
    // This sets the MODE1 register to turn on auto increment.
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, (data1 | MODE1_RESTART | MODE1_AI));
}

void readI2C1(unsigned char Address, unsigned char Register, unsigned char Data, int bytes) {
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    repeatedStart();
    sendI2C(Address | 0x01);
    //settingsLCD(RAW1);
    for (i = 0; i < bytes; i++) {
        if (i + 1 == bytes) {
            Data = receiveI2C(1);
        } else {
            Data = receiveI2C(0);
        }
        //WriteLCD(*Data);
        Data++;
    }
    //settingsLCD(CD);
    stopI2C();
    //__delay_ms(time);
}

void writeI2C1(unsigned char Address, unsigned char Register, unsigned char Data) {
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    sendI2C(Data);
    stopI2C();
    //__delay_ms(time);
}

int map(int x, int In_Min, int In_Max, int Out_Min, int Out_Max) {
    return ((x - In_Min) * ((Out_Max - Out_Min) / (In_Max - In_Min))) +Out_Min;
}

/*void void_write(unsigned char Address, unsigned char Register, unsigned char Data){
  Wire.beginTransmission(Address); //Inicia comunicação com o endereço I2C do sensor   
  Wire.write(Register); //Define o endereço inicial
  Wire.write(Data); //Escreve o dado a configurar
  Wire.endTransmission(); //Deixa aberta a comunicação com o endereço I2C do sensor
}

void void_write2(uint8_t Address, uint8_t Register, uint16_t on, uint16_t off){
  Wire.beginTransmission(Address); //Inicia comunicação com o endereço I2C do sensor   
  Wire.write(Register); //Define o endereço inicial
  Wire.write(on); //Escreve o dado a configurar
  Wire.write(on >> 8); //Escreve o dado a configurar
  Wire.write(off); //Escreve o dado a configurar
  Wire.write(off >> 8); //Escreve o dado a configurar
  Wire.endTransmission(); //Deixa aberta a comunicação com o endereço I2C do sensor
}*/