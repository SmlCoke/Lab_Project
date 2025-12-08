#include <bits/stdc++.h>
using namespace std;

struct Point {
    double x, y;
};

/// 计算两点间距离
double dist(const Point& a, const Point& b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

/// 在小规模区间（<=3）内直接暴力求最近点对
double bruteForce(const vector<Point>& pts, int l, int r) {
    double d = DBL_MAX;
    for (int i = l; i <= r; ++i) {
        for (int j = i + 1; j <= r; ++j) {
            d = min(d, dist(pts[i], pts[j]));
        }
    }
    return d;
}

/// 在跨越中线的strip区域求最近点对
double stripClosest(vector<Point>& strip, double d) {
    // strip 已按 y 坐标排序（在主函数中维持）
    sort(strip.begin(), strip.end(), [](const Point& a, const Point& b) {
        return a.y < b.y;
    });

    double minVal = d;

    // 对每个点，只需检查后续最多 6 个点（几何证明）
    for (int i = 0; i < (int)strip.size(); ++i) {
        for (int j = i + 1; j < (int)strip.size() && 
             (strip[j].y - strip[i].y) < minVal; ++j) {
            minVal = min(minVal, dist(strip[i], strip[j]));
        }
    }
    return minVal;
}

/// 核心分治算法：计算 pts[l..r] 的最近点对距离
double closestUtil(vector<Point>& pts, int l, int r) {
    // 点数小于等于 3 时，直接暴力求解
    if (r - l <= 3)
        return bruteForce(pts, l, r);

    int mid = (l + r) / 2;
    Point midPoint = pts[mid];

    // 分治求左右区间的最小距离
    double dl = closestUtil(pts, l, mid);
    double dr = closestUtil(pts, mid + 1, r);
    double d = min(dl, dr);

    // 构造 strip：取与中线 x 距离 < d 的点
    vector<Point> strip;
    strip.reserve(r - l + 1);

    for (int i = l; i <= r; ++i) {
        if (fabs(pts[i].x - midPoint.x) < d)
            strip.push_back(pts[i]);
    }

    // 处理跨越中线的最近对
    return min(d, stripClosest(strip, d));
}

/// 对外接口：输入点集（无序），返回最近点对距离
double closestPair(vector<Point> pts) {
    // 先按 x 坐标排序
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        return a.x < b.x;
    });
    return closestUtil(pts, 0, pts.size() - 1);
}

int main() {
    vector<Point> points = {
        {2.1, 3.0}, {12.0, 30.0}, {40.0, 50.0}, {5.0, 1.0},
        {12.0, 10.0}, {3.0, 4.0}
    };

    double result = closestPair(points);
    cout << "Closest distance = " << result << endl;
    return 0;
}
