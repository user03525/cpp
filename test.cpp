//488
//afisare

#include<algorithm>
#include "hogwarts.h"


using namespace std;

void process(vector<int>& v);
	
int main(){
	vector<int> v;
	read(v);
	process(v);

	return 0;
}

void process(vector<int>& v){
	for_each(v.begin(),v.end(),[v](int &n){int i=&n-&v[0];if(i%2!=0) cout<<n<<" ";});
	cout<<endl;
	for_each(v.rbegin(),v.rend(),[v](int &n){int i=&n-&v[0];if(i%2==0) cout<<n<<" ";});
}

