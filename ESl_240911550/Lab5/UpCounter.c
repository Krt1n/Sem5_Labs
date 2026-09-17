#include<LPC17xx.h>
main()
{	
	int i;
	int j;
	SystemInit();
	SystemCoreClockUpdate();
	LPC_PINCON->PINSEL0=0;
	LPC_GPIO0->FIODIR=0xF<<4;
	while(1)
	{
		for(i=0;i<16;i++)
		{
			LPC_GPIO0->FIOPIN=i<<4;
			for(j=0;j<10000;j++);
		}
	}
}