#include <iostream>
using namespace std;

int main(){
	int n;
	cout<<"Enter the number of processes"<<endl;
	cin>>n;
	int bursttime[n];
	int pid[n];
	cout<<"Enter Burst Time"<<endl;
	for(int i=0;i<n;i++){
		cout<<"For P["<<i+1<<"]";
		cin>>bursttime[i];
		pid[i]=i+1;
	}
	int temp;
	for(int i =0;i<n;i++){
		for(int j =0 ;j<n;j++){
			if(bursttime[j]>bursttime[i]){
				temp = bursttime[i];
                bursttime[i] = bursttime[j];
                bursttime[j] = temp;
                temp = pid[i];
                pid[i]= pid[j];
                pid[j] = temp;
			}
		}
		
	}
	int wt[n];
	wt[0]=0;
	for(int i =1;i<n;i++){
		wt[i]=wt[i-1]+bursttime[i-1];
	}
	float totalwt=0;
	for(int i=0;i<n;i++){
		totalwt+=wt[i];
	}
	float avg_wt = totalwt/n;
	int tat[n];
	for(int i =0;i<n;i++){
		tat[i]=bursttime[i]+wt[i];
	}
	float totaltat = 0.0;
	for(int i =0 ;i<n;i++){
		totaltat+=tat[i];
	}
	cout<<"		Process Id		Burst Time		Waiting Time		TurnAround Time"<<endl;
	for(int i =0;i<n;i++){
		cout<<"\t\t"<<pid[i];
		cout<<"\t\t\t"<<bursttime[i];
		cout<<"\t\t\t"<<wt[i];
		cout<<"\t\t\t"<<tat[i];
		cout<<endl;
	}
	float avg_tat = totaltat/n;
	cout<<"Average TAT = "<<avg_tat<<endl;
	cout<<"Average WT = "<<avg_wt<<endl;
	
}
