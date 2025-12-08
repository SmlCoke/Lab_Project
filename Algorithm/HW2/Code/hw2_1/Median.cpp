#include <iostream>
#include <vector>
#include <climits>  // for INT_MIN, INT_MAX
#include <algorithm>  // for max(), min()
using namespace std;

/**
 * 在两个有序数组中寻找中位数，时间复杂度 O(log(min(m, n))).
 * 原理：在较短的数组 A 上二分查找切分点 i。
 */
double findMedianSortedArrays(const vector<int>& A, const vector<int>& B) {
    int m = A.size();
    int n = B.size();

    // 确保 A 是较短的数组
    if (m > n) return findMedianSortedArrays(B, A);

    int left = 0, right = m;
    int totalLeft = (m + n + 1) / 2;  // 左半部分元素个数

    while (left <= right) {
        int i = (left + right) / 2;      // A 的切分点
        int j = totalLeft - i;           // B 的切分点（由总个数确定）

        // 边界情况处理
        int A_left  = (i == 0) ? INT_MIN : A[i - 1];
        int A_right = (i == m) ? INT_MAX : A[i];
        int B_left  = (j == 0) ? INT_MIN : B[j - 1];
        int B_right = (j == n) ? INT_MAX : B[j];

        // 检查是否找到合适的切分
        if (A_left <= B_right && B_left <= A_right) {
            // 总数为奇数时，取左半部分最大值
            if ((m + n) % 2 == 1)
                return max(A_left, B_left);
            else
                // 总数为偶数时，取左半部分最大与右半部分最小的平均
                return (max(A_left, B_left) + min(A_right, B_right)) / 2.0;
        }
        else if (A_left > B_right) {
            // A 的左边太大了，往左收缩
            right = i - 1;
        }
        else {
            // A 的左边太小了，往右扩张
            left = i + 1;
        }
    }

    // 正常情况不会执行到这里
    throw runtime_error("No median found (input not sorted?)");
}

int main() {
    // ------------------------------
    // 构造两个大规模升序数组
    // ------------------------------
    const int m = 5;  
    const int n = 6;  
    vector<int> A(m), B(n);

    // A = [0, 2, 4, 6, 8]
    for (int i = 0; i < m; ++i) {
        A[i] = i * 2;
    }

    // B = [1, 3, 5, 7, 9, 11]
    for (int i = 0; i < n; ++i) {
        B[i] = i * 2 + 1;
    }

    // ------------------------------
    // 计算中位数
    // ------------------------------
    double median = findMedianSortedArrays(A, B);

    cout << "Median = " << median << endl;

    return 0;
}
