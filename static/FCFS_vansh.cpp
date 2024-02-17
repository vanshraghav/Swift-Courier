#include <iostream>
using namespace std;
int main(){
	int n;
	cout<<"Enter the number of processes"<<endl;
	cin>>n;
	int pid[n];
	cout<<"Enter Process Id for all processes"<<endl;
	for(int i=0;i<n;i++){
		cin>>pid[i];
	}
	int bursttime[n];
	cout<<"Enter Burst Time of all processes"<<endl;
	for(int i=0;i<n;i++){
		cin>>bursttime[i];
	}
	int waitingtime[n];
	waitingtime[0]=0;
	for(int i = 1 ; i < n ;i++){
		waitingtime[i]=waitingtime[i-1]+bursttime[i-1];
	}
	float tat[n];
	tat[0]=waitingtime[0]+bursttime[0];
	for(int i =1 ; i <n ; i++){
		tat[i]=waitingtime[i]+bursttime[i];
	}
	cout<<" 		Process Id		Burst Time		Waiting Time		Turnaroundtime"<<endl;
	for(int i = 0 ; i<n;i++){
		cout<<"\t\t"<<pid[i];
		cout<<"\t\t\t"<<bursttime[i];
		cout<<"\t\t\t"<<waitingtime[i];
		cout<<"\t\t\t"<<tat[i];
		cout<<endl;
	}
	float totaltat=0.0;
	for(int i = 0 ; i < n ;i++){
		totaltat += tat[i];
	}
	cout<<"Average Turnaround Time  = "<<totaltat/n<<endl;
	float avgwt=0.0;
	for(int i = 0;i<n;i++){
		avgwt += waitingtime[i];
	}
	cout<<"Average Waiting Time  = "<<avgwt/n<<endl;
}


