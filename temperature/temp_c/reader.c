#include<stdio.h>
#include<stdlib.h>
#define COMMAND "cat /sys/bus/w1/devices/28*/w1_slave > tmp.txt"
//#define COMMAND "cat file.txt > tmp.txt"

// le a temperatura de uma forma roubada
float temp_reader(){

  int c;
  int cp = 0;
  char number[10];
  int flag = 0;
  int i = 0;
  float temp;



  system(COMMAND);//ROUBADA, como nao sei o caminho exato, leio e redireciono para um tmp
  FILE *fp;
  fp = fopen("tmp.txt","r");

  while((c = fgetc(fp)) != EOF){
    if (c =='\n') flag = 0; //evita fim de linha
    
    
    if (flag){
      number[i] = c;
      i++;
    }
 
    if ((cp=='t') && (c=='=')) flag = 1; // procura pelo sinal 't=' 
     
     cp = c;//armazena char anterior
  }
  fclose(fp);
  //system("rm tmp.txt") //removendo o tmp, se quiser
  temp =  atoi(number)/1000.;
  //printf("Text: %f ## \n", myvar/1000.);
  return temp;
  }

//a hard-written delay
void delay(){
unsigned int i;
for (i=0;i<100000000;i++) {}

}

//THE RUN
int main(){
  int i = 10;
  while(i--){
    printf("Temperatura: %.3f \n", temp_reader());
    delay();
  }


  return 0;
}


