#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <time.h>
#include <limits>
#include <fstream>
#include <cmath>

using namespace std;

// Rather than use nested templating that obscures the meaning, I prefer to use these names (strictly
// for readability).
typedef double * MutablePoint;
typedef double const* Point;
typedef vector<Point> Dataset;
typedef vector<Dataset> Clustering;

/*
Data points are represented as double* with a globally fixed length (number of dimensions). After data
points are read in and normalized, the pointer representing each point is used throughout the program.
Any calculations using this pointers should not modify them but instead create new double*. This
reduces unnecessary duplication as well as makes freeing memory easier and equality comparisons O(1).
*/

// The number of dimensions each data point has. In any calculations with data points (i.e. double*),
// they are assumed to be this long.
int DIMS;

// For part 2: the number of preclustering trials to conduct to find the starting points.
const int PRECLUSTERINGS = 10;

// Squared Eucliean distance between two points.
double sq_distance(Point v1, Point v2){
    double total = 0;
    for (int i = 0; i < DIMS; ++i){
        double diff = v1[i] - v2[i];
        total += diff * diff;
    }
    return total;
}

// Sum all data points in a given list and return a newly allocated MutablePoint.
MutablePoint sum_dataset(Dataset ds){
    MutablePoint sum = (MutablePoint)malloc(sizeof(double) * DIMS);
    for (int i = 0; i < DIMS; ++ i) 
        sum[i] = 0;
    for (Dataset::iterator d_iter = ds.begin(); d_iter != ds.end(); ++d_iter){
        for (int i = 0; i < DIMS; ++i)
            sum[i] += (*d_iter)[i];
    }
    return sum;
}

// Average the given list of data points and return a newly allocated MutablePoint.
MutablePoint mean_dataset(Dataset ds){
    MutablePoint sum = sum_dataset(ds);
    for (int i = 0; i < DIMS; ++i)
        sum[i] /= ds.size();
    return sum;
}

// Compute the z-score normalized data points, preserving the order of the data points. Each element at
// some index i is normalized with respect to the elements at the same index i of each other data point.
// Dimensions with zero standard deviation are assigned a normalized value of 0.
Dataset z_norm(Dataset ds){
    MutablePoint mean = mean_dataset(ds);

    MutablePoint std_dev = (MutablePoint)malloc(sizeof(double) * DIMS);
    for (Dataset::iterator d_iter = ds.begin(); d_iter != ds.end(); ++d_iter){
        for (int i = 0; i < DIMS; ++i){
            double err = (*d_iter)[i] - mean[i];
            std_dev[i] += err * err;
        }
    }
    for (int i = 0; i < DIMS; ++i)
        std_dev[i] = sqrt(std_dev[i] / (ds.size() - 1));  
    
    Dataset norm_data;
    for (Dataset::iterator d_iter = ds.begin(); d_iter != ds.end(); ++d_iter){
        MutablePoint norm_datapoint = (MutablePoint)malloc(sizeof(double) * DIMS);
        for (int i = 0; i < DIMS; ++i)
            norm_datapoint[i] = (std_dev[i] == 0) ? 0 : ((*d_iter)[i] - mean[i]) / std_dev[i];
        norm_data.push_back(norm_datapoint);
    }

    free(std_dev);
    return norm_data;
}

// Assign each data point to the closest cluster center. Data points are guaranteed to be added
// to their appropriate clusters in the order they appear in the input.
Clustering compute_assignments(int k, Dataset centers, Dataset ds){
    Clustering clusters;

    for (int i = 0; i < k; ++i)
        clusters.push_back(Dataset());

    for (Dataset::iterator d_iter = ds.begin(); d_iter != ds.end(); ++d_iter){
        double smallest_distance = numeric_limits<double>::max();
        int smallest_distance_index;

        for (int i = 0; i < k; ++i){
            double dist = sq_distance(*d_iter, centers[i]);
            if (dist < smallest_distance){
                smallest_distance = dist;
                smallest_distance_index = i;
            }
        }
        clusters[smallest_distance_index].push_back(*d_iter);    
    }

    return clusters;
}

// Compute and return the new cluster centers for the given clustering. The ordering of the returned
// centers corresponds to the order of input clusters.
vector<Point> compute_centers(Clustering clusters){
    vector<Point> centers;
    for (Clustering::iterator c_iter = clusters.begin(); c_iter != clusters.end(); ++c_iter)
        centers.push_back(mean_dataset(*c_iter));
    return centers;
}

bool clusterings_identical(Clustering c1, Clustering c2){
    // Because compute_assignments is guaranteed to maintain the same order as the input, we know that
    // we can treat corresponding indices in c1 and c2 as corresponding clusters and that the elements
    // in those clusters will appear in the same order if they are indeed identical clusters.
    for(int i = 0; i < c1.size(); ++i){
        if (c1[i].size() != c2[i].size())
            return false;
        for (int j = 0; j < c1[i].size(); ++j){
            // This is a POINTER comparison. Since the pointers representing the data are shared
            // among all parts of the program, we can do a comparison for equality in this way
            // very quickly.
            if (c1[i][j] != c2[i][j])
                return false;
        }
    }
    return true;
}

// Split the given string using a comma as the delimiter.
vector<string> split(string s){
    vector<string> tokens;
    int index = -1, last_index = 0;
    while ((index = s.find(',', index + 1)) != string::npos){
        tokens.push_back(s.substr(last_index, index - last_index));
        last_index = index + 1;
    }
    tokens.push_back(s.substr(last_index, string::npos));
    return tokens;
}

// Run a single k-means instance with the given initial center points. Return the final
// clustering configuration. The center points are copied before being used; the data
// is used in-place without being modified.
Clustering kmeans(int k, vector<Point> initial_centers, Dataset ds){
    vector<Point> centers;
    // Copy the centers.
    for (vector<Point>::iterator c_iter = initial_centers.begin(); c_iter != initial_centers.end(); ++c_iter){
        MutablePoint c = (MutablePoint)malloc(sizeof(double) * DIMS);
        memcpy((void*)c, (void*)(*c_iter), sizeof(double) * DIMS);
        centers.push_back(c);
    }

    // Main k-means loop.
    Clustering clusters, old_clusters;
    for (int i = 0; i < 50; ++i){
        clusters = compute_assignments(k, centers, ds);

        for (int j = 0; j < k; ++j){
            free((void*)centers[j]);
        }
        centers = compute_centers(clusters);

        if (old_clusters.size() > 0 && clusterings_identical(clusters, old_clusters))
            break;

        old_clusters = clusters;
    }

    for (int i = 0; i < centers.size(); ++i)
        free((void*)centers[i]);
    
    return clusters;
}

// Return a n-sized list of randomly selected points from the population, without replacement.
// Points in the returned vector are NOT copies of the selected members of the population.
vector<Point> random_points(int n, Dataset population){
    vector<Point> sample;
    vector<int> indices;
    for (int i = 0; i < n; ++i){
        int index = rand() % population.size();
        while (find(indices.begin(), indices.end(), index) != indices.end())
            index = rand() % population.size();
        
        indices.push_back(index);
        sample.push_back(population[index]);
    }

    return sample;
}

// See writeup.
vector<Point> precluster_points(int k, Dataset ds){
    vector<Point> centers;
    
    Dataset small_dataset = random_points(ds.size() / 10, ds);
    Clustering c = kmeans(k, random_points(k, small_dataset), small_dataset);
    for (Clustering::iterator c_iter = c.begin(); c_iter != c.end(); ++c_iter)
        centers.push_back(mean_dataset(*c_iter));
    
    return centers;
    
    /*
    // This is the original version of the code.
    vector<Point> centers;
    
    for (int i = 0; i < PRECLUSTERINGS; ++i){
        Dataset small_dataset = random_points(ds.size() / 10, ds);
        Clustering c = kmeans(k, random_points(k, small_dataset), small_dataset);
        for (Clustering::iterator c_iter = c.begin(); c_iter != c.end(); ++c_iter)
                    centers.push_back(mean_dataset(*c_iter));
    }

    Clustering result = kmeans(k, random_points(k, centers), centers);

    vector<Point> precluster_centers;
    for (Clustering::iterator c_iter = result.begin(); c_iter != result.end(); ++c_iter)
        precluster_centers.push_back(mean_dataset(*c_iter));

    return precluster_centers;
    */
}

double sum_sq_err(Clustering clusters){
    double sum = 0;
    for (Clustering::iterator c_iter = clusters.begin(); c_iter != clusters.end(); ++c_iter){
        Point center = mean_dataset(*c_iter);
        for (Dataset::iterator d_iter = (*c_iter).begin(); d_iter != (*c_iter).end(); ++d_iter)
            sum += sq_distance(*d_iter, center);
    }
    
    return sum;
}

int main(int argc, char *argv[]){
    if (argc < 2){
        cout << "usage: " << argv[0] << " filename" << endl;
        exit(0);
    }

    ifstream input(argv[1]);
    string line;

    // Skip headers.
    while (true){
        getline(input, line);
        if (line == "@data")
            break;
    }
    
    Dataset data;

    // Figure out the number of dimensions we're going to need by looking at the first data point.
    getline(input, line);
    vector<string> values = split(line);
    DIMS = values.size();

    // Insert the first data point.
    MutablePoint datapoint = (MutablePoint)malloc(sizeof(double) * DIMS);
    for (int i = 0; i < values.size(); ++i)
        datapoint[i] = atof(values[i].c_str());
    data.push_back(datapoint);
    
    // Insert the remaining data points.
    while (true){
        getline(input, line);
        if (line == ""){
            if (input.eof()) break;
            else continue;
        }
        values = split(line);

        datapoint = (MutablePoint)malloc(sizeof(double) * DIMS);
        for (int i = 0; i < values.size(); ++i)
            datapoint[i] = atof(values[i].c_str());
        data.push_back(datapoint);

        if (input.eof())
            break;
    }

    Dataset norm_data = z_norm(data);

    for (Dataset::iterator d_iter = data.begin(); d_iter != data.end(); ++d_iter){
        free((void*) *d_iter);
    }

    srand(1);
    // srand(time(NULL));

    // Main k-means, part 1 ------------------------------------------------------------------------
    cout << "1 kmeans";

    /*
    // Generate chart output.
    cout.precision(0);
    cout << " k" << setw(12) << "mean" << setw(12) << "-2 stddev" << setw(12) << "+2 stddev" << endl;
    */
    for (int k = 1; k < 13; ++k){
        double sse_totals[25];
        double sse_mean = 0;
        for (int i = 0; i < 25; ++i){
            sse_totals[i] = sum_sq_err(kmeans(k, random_points(k, norm_data), norm_data));
            sse_mean += sse_totals[i];
        }
        sse_mean /= 25;

        double sse_std_dev = 0;
        for (int i = 0; i < 25; ++i)
            sse_std_dev += pow(sse_totals[i] - sse_mean, 2);
        sse_std_dev = sqrt(sse_std_dev / 24);
        
        /*
        // Generate chart output.
        cout << setw(2) << k << setw(12) << fixed << sse_mean;
        cout << setw(12) << fixed << (sse_mean - 2 * sse_std_dev);
        cout << setw(12) << fixed << (sse_mean + 2 * sse_std_dev) << endl;
        */

        cout << ' ' << sse_mean; 
    }
    cout << endl;
    
    // Main k-means, part 2 ------------------------------------------------------------------------
    cout << "2 kmeans";

    // Generate chart output.
    /*
    cout.precision(0);
    cout << " k" << setw(12) << "mean" << setw(12) << "-2 stddev" << setw(12) << "+2 stddev" << endl;
    */
    for (int k = 1; k < 13; ++k){
        double sse_totals[25];
        double sse_mean = 0;

        for (int i = 0; i < 25; ++i){
            // Note the difference: the starting centers here are from precluster_points.
            sse_totals[i] = sum_sq_err(kmeans(k, precluster_points(k, norm_data), norm_data));
            sse_mean += sse_totals[i];
        }
        sse_mean /= 25;

        double sse_std_dev = 0;
        for (int i = 0; i < 25; ++i)
            sse_std_dev += pow(sse_totals[i] - sse_mean, 2);
        sse_std_dev = sqrt(sse_std_dev / 24);
        
        /*
        // Generate chart output.
        cout << setw(2) << k << setw(12) << fixed << sse_mean;
        cout << setw(12) << fixed << (sse_mean - 2 * sse_std_dev);
        cout << setw(12) << fixed << (sse_mean + 2 * sse_std_dev) << endl;
        */
        cout << ' ' << sse_mean; 
    }
    cout << endl;

}
