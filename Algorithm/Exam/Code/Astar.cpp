#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <sstream>
#include <limits>

using namespace std;

struct Edge {
    int to;
    int weight;
};

struct NodeState {
    int node;
    int g;  // 当前实际代价
    int f;  // 估计总代价 = g + h
    bool operator<(const NodeState& other) const {
        return f > other.f; // 小根堆（优先 f 小的）
    }
};

// 启发函数（如无地理信息，可设为0，退化成 Dijkstra）
int heuristic(int node, int target) {
    return 0;
}

int main() {
    string filename;
    cout << "input data file: ";
    cin >> filename;

    ifstream fin(filename);
    if (!fin.is_open()) {
        cerr << "File cannot be opened!" << endl;
        return 1;
    }

    // 为了自动适应节点编号，我们需要统计最大节点编号
    vector<tuple<int,int,int>> edges_temp;
    int u, v, w;
    int maxNode = -1;

    while (fin >> u >> v >> w) {
        edges_temp.emplace_back(u, v, w);
        maxNode = max(maxNode, max(u, v));
    }
    fin.close();

    int n = maxNode + 1;
    cout << "Detected number of nodes: " << n << endl;

    // 建立邻接表
    vector<vector<Edge>> graph(n);
    for (auto &e : edges_temp) {
        int a, b, ww;
        tie(a, b, ww) = e;
        graph[a].push_back({b, ww});
    }

    int source;
    cout << "Input source node: ";
    cin >> source;

    if (source < 0 || source >= n) {
        cerr << "Invalid source node!" << endl;
        return 1;
    }

    // ----------- A* 算法求单源最短路径（到所有节点） -----------

    const int INF = numeric_limits<int>::max();
    vector<int> dist(n, INF);
    dist[source] = 0;

    priority_queue<NodeState> pq;
    pq.push({source, 0, heuristic(source, -1)});

    while (!pq.empty()) {
        auto cur = pq.top(); pq.pop();
        int u = cur.node;

        if (cur.g > dist[u]) continue; // 已经是次优状态

        for (auto &edge : graph[u]) {
            int v = edge.to;
            int w = edge.weight;

            int newG = dist[u] + w;
            if (newG < dist[v]) {
                dist[v] = newG;
                int h = heuristic(v, -1); // 这里暂时不用 target
                pq.push({v, newG, newG + h});
            }
        }
    }

    // ----------- 输出结果 -----------
    // cout << "\n从节点 " << source << " 出发的最短路径：\n";
    cout << "\nShortest paths from node " << source << ":\n";
    for (int i = 0; i < n; i++) {
        if (dist[i] == INF)
            cout << "Node " << i << " is unreachable\n";
        else
            cout << "Shortest distance to node " << i << " = " << dist[i] << "\n";
    }

    return 0;
}
