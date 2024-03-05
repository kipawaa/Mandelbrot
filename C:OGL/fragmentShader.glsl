#version 330 core

// input data (comes from vertex shader)
in vec3 position;

// output data
out vec4 FragColor;

void main() {
        FragColor = vec4(position.z/80.0f, position.z/80.0f, position.z/80.0f, 1.0f);
} 
