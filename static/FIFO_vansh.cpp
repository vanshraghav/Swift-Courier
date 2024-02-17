#include <iostream>
using namespace std;
int main(){
	int nf;
	cout<<"Enter the number of frames"<<endl;
	cin>>nf;
	int frames[nf];
	for(int i=0;i<nf;i++){
		frames[i]=-1;
	}
	int pl;
	cout<<"Enter the length of input string"<<endl;
	cin>>pl;
	int number[pl];
	cout<<"Enter the values of the input string"<<endl;
	for(int i=0;i<pl;i++){
		cin>>number[i];
	}
	int top=0;
	int hits=0;
	for(int i =0;i<pl;i++){
		int flag=0;
		for(int j=0;j<nf;j++){
			if(frames[j]==number[i]){
				flag=1;
				hits++;
				break;
			}
		}
		if(flag==0){
			frames[top]=number[i];
			top++;
			if(top>=nf){
				top=0;
			}
		}
	}
	cout<<"Number of hits are : - "<<hits<<endl;
	
}
