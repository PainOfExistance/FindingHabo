#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Define Point struct
typedef struct {
    int x;
    int y;
} Point;

// Define Node struct for priority queue
typedef struct {
    int priority;
    Point point;
} Node;

// Define AStar struct
typedef struct {
    int** grid;
    int width;
    int height;
} AStar;

// Function prototypes
AStar* AStar_new(int* grid, int width, int height);
void AStar_delete(AStar* astar);
Point* AStar_find_path(AStar* astar, Point start, Point end, Point npc_size, int* path_length);
void AStar_delete_path(Point* path);

// Calculate Manhattan distance heuristic
int heuristic(Point a, Point b) {
    return abs(b.x - a.x) + abs(b.y - a.y);
}

// Function to initialize AStar object
AStar* AStar_new(int* grid, int width, int height) {
    AStar* astar = (AStar*)malloc(sizeof(AStar));
    astar->width = width;
    astar->height = height;
    
    // Allocate memory for grid
    astar->grid = (int**)malloc(width * sizeof(int*));
    for (int i = 0; i < width; i++) {
        astar->grid[i] = (int*)malloc(height * sizeof(int));
        for (int j = 0; j < height; j++) {
            astar->grid[i][j] = grid[i * height + j];
        }
    }
    
    return astar;
}

// Function to free memory allocated for AStar object
void AStar_delete(AStar* astar) {
    for (int i = 0; i < astar->width; i++) {
        free(astar->grid[i]);
    }
    free(astar->grid);
    free(astar);
}

// Function to find path using A* algorithm
Point* AStar_find_path(AStar* astar, Point start, Point end, Point npc_size, int* path_length) {
    if (astar->grid[start.x][start.y] == 1 || astar->grid[end.x][end.y] == 1) {
        *path_length = 0;
        return NULL;
    }

    // Priority queue implementation using an array
    Node* open_set = (Node*)malloc(astar->width * astar->height * sizeof(Node));
    int open_set_size = 0;
    
    // Visited set implementation using a 2D array
    int** visited = (int**)malloc(astar->width * sizeof(int*));
    for (int i = 0; i < astar->width; i++) {
        visited[i] = (int*)calloc(astar->height, sizeof(int));
    }

    // G-cost and parent arrays
    int** g_cost = (int**)malloc(astar->width * sizeof(int*));
    Point** parent = (Point**)malloc(astar->width * sizeof(Point*));
    for (int i = 0; i < astar->width; i++) {
        g_cost[i] = (int*)malloc(astar->height * sizeof(int));
        parent[i] = (Point*)malloc(astar->height * sizeof(Point));
        for (int j = 0; j < astar->height; j++) {
            g_cost[i][j] = -1; // Initialize to -1 (infinity)
        }
    }
    
    // Add start node to open set
    open_set[open_set_size++] = (Node){0, start};
    g_cost[start.x][start.y] = 0;

    while (open_set_size > 0) {
        // Find node with minimum priority
        int min_index = 0;
        for (int i = 1; i < open_set_size; i++) {
            if (open_set[i].priority < open_set[min_index].priority) {
                min_index = i;
            }
        }
        Node current = open_set[min_index];
        
        // Pop node from open set
        for (int i = min_index; i < open_set_size - 1; i++) {
            open_set[i] = open_set[i + 1];
        }
        open_set_size--;

        if (current.point.x == end.x && current.point.y == end.y) {
            // Reconstruct path
            Point* path = (Point*)malloc(astar->width * astar->height * sizeof(Point));
            int path_index = 0;
            Point current_point = end;
            while (current_point.x != start.x || current_point.y != start.y) {
                path[path_index++] = current_point;
                current_point = parent[current_point.x][current_point.y];
            }
            path[path_index++] = start;
            
            // Reverse path
            *path_length = path_index;
            Point* reversed_path = (Point*)malloc(path_index * sizeof(Point));
            for (int i = 0; i < path_index; i++) {
                reversed_path[i] = path[path_index - i - 1];
            }
            
            // Free memory
            free(open_set);
            for (int i = 0; i < astar->width; i++) {
                free(visited[i]);
                free(g_cost[i]);
                free(parent[i]);
            }
            free(visited);
            free(g_cost);
            free(parent);
            free(path);
            
            return reversed_path;
        }

        visited[current.point.x][current.point.y] = 1;

        for (int dx = -npc_size.x + 1; dx < npc_size.x; ++dx) {
            for (int dy = -npc_size.y + 1; dy < npc_size.y; ++dy) {
                int x = current.point.x + dx;
                int y = current.point.y + dy;
                if (0 <= x && x < astar->width && 0 <= y && y < astar->height && astar->grid[x][y] == 0 && visited[x][y] == 0) {
                    int new_g_cost = g_cost[current.point.x][current.point.y] + 1;
                    if (new_g_cost < g_cost[x][y] || g_cost[x][y] == -1) {
                        g_cost[x][y] = new_g_cost;
                        parent[x][y] = current.point;
                        open_set[open_set_size++] = (Node){new_g_cost + heuristic((Point){x, y}, end), (Point){x, y}};
                    }
                }
            }
        }
    }

    // No path found
    *path_length = 0;
    free(open_set);
    for (int i = 0; i < astar->width; i++) {
        free(visited[i]);
        free(g_cost[i]);
        free(parent[i]);
    }
    free(visited);
    free(g_cost);
    free(parent);
    return NULL;
}

// Function to free memory allocated for path
void AStar_delete_path(Point* path) {
    free(path);
}
