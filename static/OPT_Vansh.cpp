#include <iostream>
using namespace std;

int main() {
    int nf;
    cout << "No. of frames: ";
    cin >> nf;

    int frames[nf];
    for (int i = 0; i < nf; i++) {
        frames[i] = -1;
    }

    int pl;
    cout << "Enter the length of the string: ";
    cin >> pl;

    int number[pl];
    for (int i = 0; i < pl; i++) {
        cout << "Input String: ";
        cin >> number[i];
    }

    int hits = 0;
    int faults = 0;

    for (int i = 0; i < pl; i++) {
        int flag = 0;

        for (int j = 0; j < nf; j++) {
            if (frames[j] == number[i]) {
                flag = 1;
                hits++;
                break;
            }
        }

        if (flag == 0){
            int pageToReplace = -1;
            int farthest = -1;

            for (int j = 0; j < nf; j++) {
                int nextOccurrence = pl;
                for (int k = i + 1; k < pl; k++) {
                    if (frames[j] == number[k]) {
                        nextOccurrence = k;
                        break;
                    }
                }
                if (nextOccurrence > farthest) {
                    farthest = nextOccurrence;
                    pageToReplace = j;
                }
            }

            frames[pageToReplace] = number[i];
            faults++;
        }
    }

    cout << "No. of Hits: " << hits << endl;
    cout << "No. of Faults: " << faults << endl;

    return 0;
}
