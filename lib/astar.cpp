#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <unordered_set>
#include <unordered_map>
#include <functional>
#include "astar.h"
using namespace std;

struct PointHash {
    size_t operator()(const Point &p) const {
        return hash<int>()(p.x) ^ (hash<int>()(p.y) << 1);
    }
};

AStar::AStar(const vector<vector<int>> &grid) : grid(grid), width(grid.size()), height(grid[0].size()) {}

int AStar::heuristic(const Point &a, const Point &b) {
    return abs(b.x - a.x) + abs(b.y - a.y);
}

vector<Point> AStar::find_path(const Point &start, const Point &end, const Point &npc_size) {
    if (grid[start.x][start.y] == 1 || grid[end.x][end.y] == 1) {
        return {};
    }

    priority_queue<pair<int, Point>, vector<pair<int, Point>>, greater<>> open_set;
    open_set.push({0, start});
    unordered_set<Point, PointHash> visited;
    unordered_map<Point, int, PointHash> g_cost;
    unordered_map<Point, Point, PointHash> parent;
    g_cost[start] = 0;

    while (!open_set.empty()) {
        auto [_, current] = open_set.top();
        open_set.pop();

        if (current == end) {
            vector<Point> path;
            while (current != start) {
                path.push_back(current);
                current = parent[current];
            }
            path.push_back(start);
            reverse(path.begin(), path.end());
            return path;
        }

        visited.insert(current);

        for (int dx = -npc_size.x + 1; dx < npc_size.x; ++dx) {
            for (int dy = -npc_size.y + 1; dy < npc_size.y; ++dy) {
                int x = current.x + dx;
                int y = current.y + dy;
                if (0 <= x && x < width && 0 <= y && y < height && grid[x][y] == 0 && visited.find({x, y}) == visited.end()) {
                    int new_g_cost = g_cost[current] + 1;
                    if (new_g_cost < g_cost[{x, y}] || g_cost.find({x, y}) == g_cost.end()) {
                        g_cost[{x, y}] = new_g_cost;
                        parent[{x, y}] = current;
                        open_set.push({new_g_cost + heuristic({x, y}, end), {x, y}});
                    }
                }
            }
        }
    }
    return {};
}

extern "C" {
    AStar *AStar_new(int *grid, int width, int height) {
        vector<vector<int>> grid_vec(width, vector<int>(height));
        for (int i = 0; i < width; ++i) {
            for (int j = 0; j < height; ++j) {
                grid_vec[i][j] = grid[i * height + j];
            }
        }
        return new AStar(grid_vec);
    }

    void AStar_delete(AStar *astar) {
        delete astar;
    }

    Point *AStar_find_path(AStar *astar, Point start, Point end, Point npc_size, int *path_length) {
        vector<Point> path = astar->find_path(start, end, npc_size);
        *path_length = path.size();
        Point *path_array = new Point[*path_length];
        copy(path.begin(), path.end(), path_array);
        return path_array;
    }

    void AStar_delete_path(Point *path) {
        delete[] path;
    }
}
