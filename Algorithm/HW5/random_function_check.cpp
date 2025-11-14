#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <map>
using namespace std;

// 随机算法：验证并恢复被篡改的函数值
// 参数：
//   F: 函数值数组（可能被篡改）
//   n: 定义域大小
//   m: 值域大小
//   z: 需要计算的函数值的自变量
//   k: 随机验证次数
// 返回值：F(z)的估计值
int computeFunctionValue(vector<int>& F, int n, int m, int z, int k) {
    // 随机选择k对(x, y)使得(x + y) mod n = z
    // 验证F(z)是否等于(F(x) + F(y)) mod m
    
    map<int, int> votes; // 存储每个可能值的投票数
    
    for (int i = 0; i < k; i++) {
        // 随机选择x，计算y = (z - x) mod n
        int x = rand() % n;
        int y = (z - x + n) % n;
        
        // 计算候选值: (F(x) + F(y)) mod m
        int candidate = (F[x] + F[y]) % m;
        votes[candidate]++;
    }
    
    // 返回获得最多票数的值（多数投票）
    int maxVotes = 0;
    int result = F[z];
    for (auto& p : votes) {
        if (p.second > maxVotes) {
            maxVotes = p.second;
            result = p.first;
        }
    }
    
    return result;
}

// 单次随机验证算法（Monte Carlo算法）
// 返回值：F(z)的一个候选值
int singleRandomCheck(vector<int>& F, int n, int m, int z) {
    // 随机选择x，计算y = (z - x) mod n
    int x = rand() % n;
    int y = (z - x + n) % n;
    
    // 返回候选值: (F(x) + F(y)) mod m
    return (F[x] + F[y]) % m;
}

// 运行算法3次，返回众数
int threeTimesAlgorithm(vector<int>& F, int n, int m, int z) {
    map<int, int> votes;
    
    // 运行3次
    for (int i = 0; i < 3; i++) {
        int result = singleRandomCheck(F, n, m, z);
        votes[result]++;
    }
    
    // 返回出现次数最多的值（majority voting）
    int maxVotes = 0;
    int result = F[z];
    for (auto& p : votes) {
        if (p.second > maxVotes) {
            maxVotes = p.second;
            result = p.first;
        }
    }
    
    return result;
}

int main() {
    srand(time(0));
    
    int n = 10; // 定义域大小
    int m = 10; // 值域大小
    
    // 示例：定义一个线性函数 F(x) = (2*x) mod m
    vector<int> originalF(n);
    for (int i = 0; i < n; i++) {
        originalF[i] = (2 * i) % m;
    }
    
    // 复制并篡改1/5的值
    vector<int> corruptedF = originalF;
    int numCorrupted = n / 5;
    for (int i = 0; i < numCorrupted; i++) {
        int pos = rand() % n;
        corruptedF[pos] = rand() % m; // 随机篡改
    }
    
    cout << "原始函数值: ";
    for (int i = 0; i < n; i++) {
        cout << originalF[i] << " ";
    }
    cout << endl;
    
    cout << "被篡改的函数值: ";
    for (int i = 0; i < n; i++) {
        cout << corruptedF[i] << " ";
    }
    cout << endl;
    
    // 测试算法
    int z = 5; // 要计算的位置
    cout << "\n计算 F(" << z << "):" << endl;
    cout << "真实值: " << originalF[z] << endl;
    cout << "数组中的值（可能被篡改）: " << corruptedF[z] << endl;
    
    // 使用k次随机验证
    int k = 10;
    int estimated = computeFunctionValue(corruptedF, n, m, z, k);
    cout << "使用" << k << "次随机验证的估计值: " << estimated << endl;
    
    // 使用3次算法
    int estimated3 = threeTimesAlgorithm(corruptedF, n, m, z);
    cout << "运行3次算法的结果: " << estimated3 << endl;
    
    return 0;
}
