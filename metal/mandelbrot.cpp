#define NS_PRIVATE_IMPLEMENTATION
#define CA_PRIVATE_IMPLEMENTATION
#define MTL_PRIVATE_IMPLEMENTATION
#include <Foundation/Foundation.hpp>
#include <Metal/Metal.hpp>
#include <QuartzCore/QuartzCore.hpp>

#include <cmath>
#include <complex>

using namespace std;

kernel void get_mandelbrot(device complex c, device int convergence_limit, device int divergence_limit, device int* result) {
        int n = 0;
        complex<double> z(0.0, 0.0);

        while (n < convergence_limit && abs(z) < divergence_limit) {
                z = pow(z, 2) + c;

                n += 1;
        }

        return n;
}


void draw_mandelbrot(int width, int height) {
        [renderEncoder drawPrimitives:MTLPrimitiveTypeRectangle
                vertexStart:0
                vertexCount:


int main() {
        
}
