#include "hogwarts.h"

bool isPrime(int n){
	if(n<2){
		return false;
	}
	for(int d=2;d*d<=n;d++){
		if(n%d==0)
			return false;
	}
	return true;
}	




