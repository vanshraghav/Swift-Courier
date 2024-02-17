#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter the number of processes: " << endl;
    cin >> n;

    if (n <= 0) {
        cout << "Invalid number of processes. Please enter a positive integer." << endl;
        return 1;
    }

    int bt[n];
    int pid[n];
    int priority[n];

    cout << "Enter Burst Time and Priority" << endl;
    for (int i = 0; i < n; i++) {
        cout << "Enter Burst Time for P[" << i + 1 << "]: ";
        cin >> bt[i];
        cout << "Enter Priority for P[" << i + 1 << "]: ";
        cin >> priority[i];
        pid[i] = i + 1;
    }

    int temp;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (priority[j] > priority[i]) {
                temp = bt[i];
                bt[i] = bt[j];
                bt[j] = temp;
                temp = priority[i];
                priority[i] = priority[j];
                priority[j] = temp;
                temp = pid[i];
                pid[i] = pid[j];
                pid[j] = temp;
            }
        }
    }

    int wt[n];
    wt[0] = 0;
    for (int i = 1; i < n; i++) {
        wt[i] = wt[i - 1] + bt[i - 1];
    }

    float totalwt = 0.0;
    for (int i = 0; i < n; i++) {
        totalwt += wt[i];
    }

    int tat[n];
    for (int i = 0; i < n; i++) {
        tat[i] = bt[i] + wt[i];
    }

    float totaltat = 0.0;
    for (int i = 0; i < n; i++) {
        totaltat += tat[i];
    }

    cout << "Process Id\tBurst Time\tWaiting Time\tTAT" << endl;
    for (int i = 0; i < n; i++) {
        cout << "\t\t" << pid[i];
        cout << "\t\t\t" << bt[i];
        cout << "\t\t\t" << wt[i];
        cout << "\t\t\t" << tat[i];
        cout << endl;
    }

    cout << "Average Waiting Time = " << totalwt / n << endl;
    cout << "Average TAT = " << totaltat / n << endl;

    return 0;
}

