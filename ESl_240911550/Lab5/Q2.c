//Write an embedded C program to turn ON the LED when the switch connected 
//to P2.12 is pressed and turn OFF the LED when the switch is released. 
#include<LPC17xx.h>
main()
{
	int x;
	SystemInit();
	SystemCoreClockUpdate();
	LPC_PINCON->PINSEL0=0;
	LPC_PINCON->PINSEL4=0;
	LPC_GPIO0->FIODIR=1<<4;
	LPC_GPIO2->FIODIR=0;
	while(1)
	{
		x=LPC_GPIO2->FIOPIN;
		if(!(x&(1<<12)))
			LPC_GPIO0->FIOSET=1<<4;
		else
			LPC_GPIO0->FIOCLR=1<<4;
	}
}
	
	