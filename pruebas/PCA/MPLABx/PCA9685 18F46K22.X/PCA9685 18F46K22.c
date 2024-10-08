#include <xc.h>
#include <string.h>
#include <stdio.h>

#pragma config FOSC = INTIO67 //OSCILADOR  INTERNO Y PINES 6 Y 7 COMO ENTRADAS Y SALIDAS
#pragma config WDTEN = OFF //PERRO GUARDIAN 
#pragma config LVP = OFF // PROGRAMACION DE BAJO VOLTAJE ;

#define _XTAL_FREQ 16000000
#define time 100

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
//LCD
/*
#define CD 0x01
#define RH 0x02
#define EMS 0x06
#define DC 0x0F
#define DSr 0x1C
#define DS1 0x18
#define FS 0x38
#define RAW1 0x80
#define RAW2 0xC0
#define E LATE0
#define RS LATE1
#define button PORTBbits.RB2*/

void settings(void);
void writeI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes); //*=puntero(direccion de memoria)
void writeI2C1(unsigned char Address, unsigned char Register, unsigned char Data); //*=puntero(direccion de memoria)
void startI2C(void); //empieza la comunicaci�n
void readyI2C(void); //evita colicion de datos
void sendI2C(unsigned char data);
void stopI2C(void);
void readI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes);
void readI2C1(unsigned char Address, unsigned char Register, unsigned char Data, int bytes);
void repeatedStart(void);
unsigned char receiveI2C(char flag);
//LCD
/*void settingsLCD(unsigned char word);
void WriteLCD(unsigned char word);
void LCD(unsigned char data);
void data(void);*/
//PCA9685
int map(int x, int In_Min, int In_Max, int Out_Min, int Out_Max);
void setPWMFreq(float freq);
int i, pos, DriverPin = 0, led = 0;
unsigned char data1, data2[4];

/*unsigned char name[16]={"UNIVERSIDAD ECCI"};
int i;
unsigned char dataSaved[16];*/

void main(void) {
    settings();
    while (1) {
        /*writeI2C(SlaveAddress1,0xB5,name,16);//0xB5=ubicacion del registro
        writeI2C(SlaveAddress1,0xFF,&name[5],1);//envia solo un dato del puntero o vector(&)
        readI2C(SlaveAddress1,0xB5,dataSaved,16);*/
        data2[0] = 0;
        data2[1] = 0;
        for (int j = 0; j < 4; j++) { //Pines o canales PWM de la placa
            if(led == 0){
                LATDbits.LATD0 = 1;
                led = 1;
            }
            else{
                LATDbits.LATD0 = 0;
                led = 0;
            }
            DriverPin = j;
            pos = map(180, 0, 180, SERVOMIN, SERVOMAX);
            data2[2] = pos;
            data2[3] = pos >> 8;
            //void_write2(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + 4 * DriverPin, 0, pos);
            writeI2C(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + (4 * DriverPin), data2, 4);
            __delay_ms(1000);
            pos = map(0, 0, 180, SERVOMIN, SERVOMAX);
            data2[2] = pos;
            data2[3] = pos >> 8;
            //void_write2(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + 4 * DriverPin, 0, pos);
            writeI2C(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + (4 * DriverPin), data2, 4);
            __delay_ms(1000);
            pos = map(90.58, 0, 180, SERVOMIN, SERVOMAX);
            data2[2] = pos;
            data2[3] = pos >> 8;
            //void_write2(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + 4 * DriverPin, 0, pos);
            writeI2C(I2C_ADDRESS_PCA9685, PCA9685_LED0_ON_L + (4 * DriverPin), data2, 4);
            __delay_ms(1000);
            
        }
    }
}

void settings(void) {

    //OSCCON = 0x70; //Para 8MHz
    OSCCON = 0x72;
    ANSELC = 0x00;
    ANSELD = 0x00;

    TRISCbits.RC3 = 1;
    TRISCbits.RC4 = 1;
    TRISE = 0x00; //LCD
    LATE = 0x00; //LCD
    TRISD = 0x00; //LCD
    LATD = 0x00; //LCD

    //LCD
    /*settingsLCD(EMS);
    settingsLCD(DC);
    settingsLCD(FS);*/
    //Configurar pines de comunicacion I2C
    SSP1STAT = 0x80;
    SSP1CON1 = 0x28;
    SSP1CON2 = 0x00;
    SSP1CON3 = 0x00;
    SSP1ADD = 0x27;

    //PCA9685
    writeI2C1(I2C_ADDRESS_PCA9685, PCA9685_MODE1, MODE1_RESTART);
    __delay_ms(10);
    //// set a default frequency
    setPWMFreq(PWM_Frequencia);
    //// set a servo frequency
    setPWMFreq(Frequencia);
    __delay_ms(300);
}

void writeI2C(unsigned char Address, unsigned char Register, unsigned char *Data, int bytes) {
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    for (i = 0; i < bytes; i++) {
        sendI2C(*Data);
        Data++;
    }
    stopI2C();
    __delay_ms(time);
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

/*void settingsLCD(unsigned char word){
    RS = 0;
    LCD(word);
}

void WriteLCD(unsigned char word){
    RS = 1;
    LCD(word);
}

void LCD(unsigned char data){
    E = 1;
    __delay_ms(time);
    LATD = data;
    __delay_ms(time);
    E = 0;
    __delay_ms(time);
}*/

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
    __delay_ms(time);
}

void writeI2C1(unsigned char Address, unsigned char Register, unsigned char Data) {
    startI2C();
    sendI2C(Address);
    sendI2C(Register);
    sendI2C(Data);
    stopI2C();
    __delay_ms(time);
}

int map(int x, int In_Min, int In_Max, int Out_Min, int Out_Max) {
    return ((x - In_Min) * ((Out_Max - Out_Min) / (In_Max - In_Min))) +Out_Min;
}

/*void void_write(unsigned char Address, unsigned char Register, unsigned char Data){
  Wire.beginTransmission(Address); //Inicia comunica��o com o endere�o I2C do sensor   
  Wire.write(Register); //Define o endere�o inicial
  Wire.write(Data); //Escreve o dado a configurar
  Wire.endTransmission(); //Deixa aberta a comunica��o com o endere�o I2C do sensor
}

void void_write2(uint8_t Address, uint8_t Register, uint16_t on, uint16_t off){
  Wire.beginTransmission(Address); //Inicia comunica��o com o endere�o I2C do sensor   
  Wire.write(Register); //Define o endere�o inicial
  Wire.write(on); //Escreve o dado a configurar
  Wire.write(on >> 8); //Escreve o dado a configurar
  Wire.write(off); //Escreve o dado a configurar
  Wire.write(off >> 8); //Escreve o dado a configurar
  Wire.endTransmission(); //Deixa aberta a comunica��o com o endere�o I2C do sensor
}*/
