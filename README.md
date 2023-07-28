# Path drawing animation with Fourier series
Python program with manim to create animation of drawing of a path with Fourier circles as done from a [3b1b youtube video](https://www.youtube.com/watch?v=spUNpyF58BY)

* First make a single path in your svg or you can also modify the ipynb to stitch multiple paths, but I have done in a single path
* Use this svg file in `fourierCircles.ipynb` to compute the Fourier coefficients or the Fourier circle dimensions, which should create a `fourierCoefficients.txt` file
* Then run the `fourierCircles.py` with the manim command as you need, also refer to manim page for better usage or modifications

    `manim -pqh ./FourierCircles.py FourierCircles`
