# Non-Photorealistic Rendering

## Motivations

As an art history enthusiast, I can now mimic the styles of impressionism, post-impressionism, expressionism, pointilism, and more in a computational manner.

Original Image:

![alt text](https://github.com/weimegan/painterly/blob/main/NPR_Starter/Input/chihuly.png?raw=true)

Applying Non-Photorealistic Rendering:

![alt text](https://github.com/weimegan/painterly/blob/main/NPR_Starter/Output/ChihulyLongBrushOrientedPaint.png?raw=true)



## Implementation

`inBounds(out, y, x, texture)`

Checks if point (`x`, `y`) is not within half the size of texture from the boundaries of `out`.


`brush(out, y, x, color, texture)`

Draws a brush stroke of the opacity `texture` and color `color` centered at `y`, `x` on `out`, a mutable image. Disregard points that are closer than half the size of `texture` away from the image boundaries. If `y`, `x` are in bounds, linearly interpolate between color in `out` and `color` based on `texture` at each pixel.


`singleScalePaint(im, out, importance, texture, size=10, N=1000, noise=0.3)`

Single-Scale Paint. Scale `texture` to size `size`. Splat brush with color `(1-noise/2+noise*np.random.rand(3))*im[y,x]` onto `out` for `N` random `y`, `x` points, which are in bounds and accepted according to `importance`.


`painterly(im, texture, N=10000, size=50, noise=0.3)`

Two-Scale Paint. First layer: coarse strokes of size `size` with constant `importance`. Second layer: fine strokes of size `size/4` with greater `importance` for higher frequencies in the image. Compute a sharpness map on `im` to determine these higher frequencies.


`computeAngles(im)`

Compute tensor from `im`. For each pixel, compute the eigenvalues from the structure tensor matrix and find the eigenvector that corresponds to the minimum eigenvalue. Find the angle between that eigenvector and the horizontal line and set all 3 channels to that angle.


`singleScaleOrientedPaint(im, out, thetas, importance, texture, size, N, noise, nAngles=36)`

Single-Scale Oriented Paint. Scale texture to `size`. Splat brush with color `(1-noise/2+noise*np.random.rand(3))*im[y,x]` onto `out` for `N` random `y`, `x` points, which are in bounds and accepted according to `importance`. Rotate brushes, creating a list of `nAngles` angles. Find theta at point `y`, `x` from `thetas` and use the `texture` from the list of rotated brushes that matches theta and brush.


`orientedPaint(im, texture, N=7000, size=50, noise=0.3)`

Two-Scale Oriented Paint. Similar to `painterly` with two layers. Compute angles of `im` and pass those into each `singleScaleOrientedPaint` call.

