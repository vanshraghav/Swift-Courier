#include <iostream>
using namespace std;
int main(){
	int n;
	cout<<"Enter the number of processes"<<endl;
	cin>>n;
	int quantum;
	cout<<"Enter time Quantum"<<endl;
	cin>>quantum;
	int rem_bt[n];
	int bt[n];
	
	for(int i=0;i<n;i++){
		cout<<"Burst Time for P["<<i+1<<"] : ";
		cin>>bt[i];
		rem_bt[i]=bt[i];
	}
	int t=0;
	int wt[n];
	bool done =false;
	while(!done){
		done=true;
		for(int i=0;i<n;i++){
			if(rem_bt[i]>0){
				done=false;
				if(rem_bt[i]>quantum){
					t=t+quantum;
					rem_bt[i]=rem_bt[i]-quantum;
					
				}
				else{
					t=t+rem_bt[i];
					wt[i]=t-bt[i];
					rem_bt[i]=0;
				}
			}
		}
	}
	int total_tat=0,total_wt=0;
	int tat[n];
	for(int i=0;i<n;i++){
		tat[i]=wt[i]+bt[i];
	}
	cout<<"		Process Id		Burst Time		Waiting Time		TAT"<<endl;
	for(int i=0;i<n;i++){
		cout<<"\t\t"<<"P["<<i+1<<"]";
		cout<<"\t\t\t"<<bt[i];
		cout<<"\t\t\t"<<wt[i];
		cout<<"\t\t\t"<<tat[i];
		cout<<endl;
	}
	for(int i =0;i<n;i++){
		total_tat +=tat[i];
		total_wt+=wt[i];
		
	}
	cout<<"Average TAT : "<<total_tat/n<<endl;
	cout<<"Average WT : "<<total_wt/n<<endl;	
	
}
