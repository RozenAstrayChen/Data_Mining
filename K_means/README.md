The implementation can be divided into the following:

1. Handle Data: Clean the file, normalize the parameters, given numeric values to non-numeric attributes. Read data from the file and split the data for cross validation.
2. Find Initial Centroids: Choose k centroids in random.
3. Distance Calculation: Finding the distance between each of the datapoints with each of the centroids. This distance metric is used to find the which cluster the points belong to.
4. Re-calculating the centroids: Find the new values for centroid.using RGB
5. Stop the iteration: Stop the algorithm when the difference between the old and the new centroids is negligible.