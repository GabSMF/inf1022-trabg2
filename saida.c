#include <stdio.h>

int main(){
int X = 0;
int Y = 0;
int B = 0;
int Z = 0;
printf("Z = %d",Z);
X = 5;

Y = 2;

B = 0;

for (int i = X; i > Y; i--)
{
if (B)
{
Z = Z + 2;
printf("Z = %d",Z);
}
else
{
Z = Z + 1;
printf("Z = %d",Z);
}
}

return 0;
}