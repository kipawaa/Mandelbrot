#include<stdio.h>
#include<stdlib.h>
#include<complex.h>

#ifdef __APPLE__
	#include<OpenCL/opencl.h>
#else
	#include<CL/cl.h>
#endif

int main() {
	// get the size of the map the user would like to generate
	int width = 0;
	int height = 0;
	printf("enter the dimensions of the map you would like in the following format \"width height\": ");
	scanf("%d %d", &width, &height);

	// array to store the calculation data
	int* img = (int*)malloc(width * height * sizeof(int));

	// create a pointer to the OCL source code of sufficient size to ensure it can hold all of the data in the .cl file
	const size_t maxOCLFileSize = 0x100000;
	char* clSource = (char*)malloc(maxOCLFileSize * sizeof(char));
	
	// read from the .cl file
	FILE* clFile = fopen("mandelbrotKernel.cl", "r");
	fread(clSource, 1, maxOCLFileSize, clFile);
	fclose(clFile);


	// used to store the return values from cl functions (always zero unless a function returns an error)
	cl_int ret;

	// get platform information
	cl_platform_id platform = NULL;
	cl_uint numPlatforms;
	ret = clGetPlatformIDs(1, &platform, &numPlatforms);
	if (ret) {
		printf("platform error: %d\n", ret);
		return ret;
	}

	// get device information
	cl_device_id device = NULL;
	cl_uint numDevices;
	ret = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, &numDevices);
	if (ret) {
		printf("device error: %d\n", ret);
		return ret;
	}

	// get context
	cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &ret);
	if (ret) {
		printf("context error: %d\n", ret);
		return ret;
	}

	// create command queue for device
	cl_command_queue queue = clCreateCommandQueue(context, device, 0, &ret);
	if (ret) {
		printf("command queue error: %d\n", ret);
		return ret;
	}

	// create buffers
	cl_mem complexBuffer = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(double complex), NULL, &ret);
	if (ret) printf("complex_obj buffer error: %d\n", ret);
	cl_mem convergenceLimitBuffer = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &ret);
	cl_mem divergenceLimitBuffer = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &ret);
	cl_mem numIterationsBuffer = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(int), NULL, &ret);

	// load source code into program
	cl_program program = clCreateProgramWithSource(context, 1, (const char**)&clSource, &maxOCLFileSize, &ret);
	if (ret) {
		printf("program error: %d\n", ret);
		return ret;
	}

	// now that the program has been built from the source string, it can be freed
	free(clSource);

	// compile the program
	ret = clBuildProgram(program, 1, &device, NULL, NULL, NULL);
	if (ret) {
		printf("program build error: %d\n", ret);

		// determine the size of the build log
		size_t logSize;
		clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &logSize);

		// get build log
		char* log = (char*)malloc(logSize);
		clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, logSize, log, NULL);
		
		// output the build log for the user
		printf("%s\n", log);

		return ret;
	}

	// create the kernel
	cl_kernel kernel = clCreateKernel(program, "mandelbrotCellValue", &ret);
	if (ret) {
		printf("kernel error: %d\n", ret);
		return ret;
	}

	// declare work group and work unit sizes early so they're not re-designated each iteration of the loop
	const size_t globalSize = sizeof(double complex);
	const size_t localSize = 1;
	
	// con- and div-ergence limits for calculations
	int divergenceLimit = 2;
	int convergenceLimit = 80;

	// number of iterations used to calculate given value
	int numIterations;

	// range of values for real and imaginary axis
	int rrange[2] = {-2, 1};
	int irange[2] = {-1, 1};

	//printf("starting calculations...\n");

	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			// reset the number of iterations
			numIterations = 0;

			// define the complex value of the set at this point
			double complex c = (rrange[0] + (x / width) * (rrange[1] - rrange[0])) + // real part of the number
						(irange[0] + (y / height) * (irange[1] - irange[0])); // imaginary part of the number

			// use the kernel to get the mandelbrot value at this point
			// write data to the buffers
			ret = clEnqueueWriteBuffer(queue, complexBuffer, CL_TRUE, 0, sizeof(double), &c, 0, NULL, NULL);
			ret = clEnqueueWriteBuffer(queue, convergenceLimitBuffer, CL_TRUE, 0, sizeof(int), &convergenceLimit, 0, NULL, NULL);
			ret = clEnqueueWriteBuffer(queue, divergenceLimitBuffer, CL_TRUE, 0, sizeof(int), &divergenceLimit, 0, NULL, NULL);
			ret = clEnqueueWriteBuffer(queue, numIterationsBuffer, CL_TRUE, 0, sizeof(int), &numIterations, 0, NULL, NULL);
			//printf("buffers enqueued\n");

			// set kernel arguments
			ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void*)&complexBuffer);
			if (ret) printf("kernel arg 0 error: %d\n", ret);
			ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), (void*)&convergenceLimitBuffer);
			if (ret) printf("kernel arg 1 error: %d\n", ret);
			ret = clSetKernelArg(kernel, 2, sizeof(cl_mem), (void*)&divergenceLimitBuffer);
			if (ret) printf("kernel arg 2 error: %d\n", ret);
			ret = clSetKernelArg(kernel, 3, sizeof(cl_mem), (void*)&numIterationsBuffer);
			//printf("kernel args set\n");
			
			// run the kernel
			ret = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &globalSize, &localSize, 0, NULL, NULL);

			// read the number of iterations from the kernel
			ret = clEnqueueReadBuffer(queue, numIterationsBuffer, CL_TRUE, 0, sizeof(int), &numIterations, 0, NULL, NULL);

			// copy the number of iterations to the map
			//printf("modifying the map\n");
			img[y * width + x] = numIterations;
		}
	}

	printf("image generated\n");

	// clean up OCL stuff
	clFinish(queue);
	clFlush(queue);
	clReleaseKernel(kernel);
	clReleaseProgram(program);
	clReleaseMemObject(complexBuffer);
	clReleaseMemObject(convergenceLimitBuffer);
	clReleaseMemObject(divergenceLimitBuffer);
	clReleaseMemObject(numIterationsBuffer);
	clReleaseCommandQueue(queue);
	clReleaseContext(context);

	// free all dynamically allocated memory
	free(img);
}
