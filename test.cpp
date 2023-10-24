#include<algorithm>
#include "hogwarts.h"


using namespace std;

void check(int& n);
void process(vector<int>& v);

	
int main(){
	vector<int> v;
	read(v);
	process(v);
	print(v);

	return 0;
}

void process(vector<int>& v){
	for_each(v.rbegin(),v.rend(),check);
}

void check(int& n){
	static bool locked = false;
	if(!locked and isPrime(n)){
		locked = true;
		n=0;
	}
}
