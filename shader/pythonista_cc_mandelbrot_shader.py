# https://gist.github.com/balachandrana/82f643e38326ce9e7ce720e399b34cae

import scene, ui

shadercode_text = '''
// Modified Mandelbrot code from shadertoy.com
// https://www.shadertoy.com/view/XdtSRN
// used make_color function from ccc (pythonista forum)
// https://github.com/cclauss/fractal_hacks/blob/master/cc_mandelbrot.py

precision highp float;
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

int mandelbrot(vec2 uv) {
    vec2 z = vec2(0.0, 0.0);
    for (int i = 0; i < 64; i++) {
        // dot(z, z) > 4.0 is the same as length(z) > 2.0, but perhaps faster.
        if (dot(z, z) > 4.0) return i;
        // (x+yi)^2 = (x+yi) * (x+yi) = x^2 + (yi)^2 + 2xyi = x^2 - y^2 + 2xyi
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + uv;
    }
    return 0;
}

vec3 make_color(int i) {
    if (i == 0) return vec3(0.0,0.0,0.0);
    else if (i < 64) return vec3(float(i*4+128),float(i*4), 0.0)/255.0;
    else if ( i < 128) return vec3(64.0, 255.0, float((i-64)*4))/255.0;
    else if (i < 192) return vec3(64.0,float(255-(i-128)*4), 255.0)/255.0;
    else return vec3(64.0,0.0,float(255-(i-192)*4))/255.0;

}

void main(void) {
    // Screen coordinate, roughly -2 to +2
    vec2 uv = vec2((v_tex_coord.x-0.65)*4.0, (v_tex_coord.y-0.5)*4.0)

    // Evaluate mandelbrot for this coordinate.
    int ret = mandelbrot(uv);

    // Turn the iteration count into a color.
    //gl_FragColor = vec4(sin(vec3(0.1, 0.2, 0.5) * float(ret)), 1);
    gl_FragColor = vec4(make_color(ret), 1.0);
}
'''

class MyScene (scene.Scene):
	def setup(self):
		self.sprite = scene.SpriteNode('Snake', size=(600, 600), parent=self)
		self.sprite.shader = scene.Shader(shadercode_text)
		self.sprite.position = self.size/2
		
		
scene.run(MyScene(), show_fps=True)

