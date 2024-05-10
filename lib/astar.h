// astar.h

#ifndef ASTAR_H
#define ASTAR_H

#include <vector>
#include <unordered_map>
#include <queue>
#include <functional>

using namespace std;

struct Point {
    int x;
    int y;

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Point& other) const {
        return !(*this == other);
    }

    bool operator<(const Point& other) const {
        // Compare based on x, then y
        return x < other.x || (x == other.x && y < other.y);
    }

    bool operator>(const Point& other) const {
        // Compare based on x, then y
        return x > other.x || (x == other.x && y > other.y);
    }
};

class AStar {
public:
    AStar(const vector<vector<int>>& grid);
    int heuristic(const Point& a, const Point& b);
    vector<Point> find_path(const Point& start, const Point& end, const Point& npc_size);
private:
    const vector<vector<int>> grid;
    const int width;
    const int height;
};

#endif /* ASTAR_H */