#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <ctime>
using namespace std;

// 单次随机验证算法
int singleRandomCheck(vector<int>& F, int n, int m, int z) {
    int x = rand() % n;
    int y = (z - x + n) % n;
    return (F[x] + F[y]) % m;
}

// 运行k次并投票
int computeWithVoting(vector<int>& F, int n, int m, int z, int k) {
    map<int, int> votes;
    
    for (int i = 0; i < k; i++) {
        int candidate = singleRandomCheck(F, n, m, z);
        votes[candidate]++;
    }
    
    int maxVotes = 0, result = F[z];
    for (auto& p : votes) {
        if (p.second > maxVotes) {
            maxVotes = p.second;
            result = p.first;
        }
    }
    return result;
}

// 测试算法的准确性
void testAccuracy(int trials, int k) {
    int n = 100, m = 100;
    int correct = 0;
    
    for (int trial = 0; trial < trials; trial++) {
        // 创建满足加法同态性质的函数 F(x) = (3*x) mod m
        // 验证: F((x+y) mod n) = F(x+y) = 3*(x+y) mod m = (3*x + 3*y) mod m = (F(x) + F(y)) mod m
        vector<int> originalF(n);
        for (int i = 0; i < n; i++) {
            originalF[i] = (3 * i) % m;
        }
        
        // 篡改20%的值（确保不重复）
        vector<int> corruptedF = originalF;
        int numCorrupted = n / 5;
        vector<bool> corrupted(n, false);
        int count = 0;
        while (count < numCorrupted) {
            int pos = rand() % n;
            if (!corrupted[pos]) {
                corrupted[pos] = true;
                // 篡改为一个不同的随机值
                int newVal;
                do {
                    newVal = rand() % m;
                } while (newVal == originalF[pos]);
                corruptedF[pos] = newVal;
                count++;
            }
        }
        
        // 随机选择一个位置测试
        int z = rand() % n;
        int estimated = computeWithVoting(corruptedF, n, m, z, k);
        
        if (estimated == originalF[z]) {
            correct++;
        }
    }
    
    double accuracy = (double)correct / trials;
    cout << "测试 " << trials << " 次，验证次数 k=" << k 
         << "，准确率: " << accuracy << endl;
}

int main() {
    srand(time(0));
    
    cout << "========== 算法准确性测试 ==========" << endl;
    cout << "理论分析：单次验证准确率应为 (4/5)^2 = 0.64" << endl;
    cout << "3次投票准确率应约为 0.70" << endl << endl;
    
    testAccuracy(1000, 1);   // k=1 单次验证
    testAccuracy(1000, 3);   // k=3 三次投票
    testAccuracy(1000, 5);   // k=5 五次投票
    testAccuracy(1000, 10);  // k=10 十次投票
    
    cout << "\n========== 具体示例 ==========" << endl;
    int n = 10, m = 10;
    
    // 创建函数 F(x) = (2*x) mod m
    vector<int> originalF(n);
    for (int i = 0; i < n; i++) {
        originalF[i] = (2 * i) % m;
    }
    
    cout << "原始函数值: ";
    for (int i = 0; i < n; i++) {
        cout << originalF[i] << " ";
    }
    cout << endl;
    
    // 篡改1/5的值
    vector<int> corruptedF = originalF;
    corruptedF[1] = 9;  // 真实值是2，篡改为9
    corruptedF[4] = 3;  // 真实值是8，篡改为3
    
    cout << "被篡改的函数值: ";
    for (int i = 0; i < n; i++) {
        cout << corruptedF[i] << " ";
    }
    cout << endl << endl;
    
    // 测试多个位置
    for (int z = 0; z < 5; z++) {
        cout << "计算 F(" << z << "):" << endl;
        cout << "  真实值: " << originalF[z] << endl;
        cout << "  数组值: " << corruptedF[z] << endl;
        cout << "  3次投票结果: " << computeWithVoting(corruptedF, n, m, z, 3) << endl;
        cout << "  10次投票结果: " << computeWithVoting(corruptedF, n, m, z, 10) << endl;
        cout << endl;
    }
    
    return 0;
}
