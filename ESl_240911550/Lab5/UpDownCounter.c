#include<LPC17xx.h>
main()
{	
	SystemInit();
	SystemCoreClockUpdate();
	unsigned char count=0;
	int j;
	LPC_PINCON->PINSEL0=0; // Sets P0.0 to P0.15 as GPIO
	LPC_PINCON->PINSEL4=0; // Sets P2.0 to P2.15 as GPIO
	
	// 1. Shift direction mask so P0.4 to P0.11 are OUTPUTS
	LPC_GPIO0->FIODIR=0xFF<<4;
	LPC_GPIO2->FIODIR=0;
	while(1)
	{
		LPC_GPIO0->FIOCLR=0xFF<<4; // 2. Clear ONLY the 8 LED pins (P0.4 to P0.11)
		LPC_GPIO0->FIOSET=count<<4; // 3. Write count starting from P0.4
		if(!(LPC_GPIO2->FIOPIN & (1<<12))) // Check switch on P2.12 (Active Low) 
		{
			count++;
		}
		else
		{
			count--;
		}
		for(j=0;j<500000;j++); //Delay
	}
}