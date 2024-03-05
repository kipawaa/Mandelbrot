__kernel void mandelbrotCellValue(__global int* c, __global int* convergenceLimit, __global int* divergenceLimit, __global int* numIterations) {
	// starting value is always 0
	double value = 0;

	// while we havent crossed either the convergence of divergence limit
	while (*(numIterations) < *(convergenceLimit) && value < *(divergenceLimit)) {
		// square value and add c
		value = value * value + *(c);

		// increment the number of iterations
		*(numIterations)++;
	}
}
