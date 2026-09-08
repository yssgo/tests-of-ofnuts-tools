ofn-gradient-along-path
=======================

Purpose
-------

`ofn-gradient-along-path` draws a bilinear blend transversally along path strokes, using the current gradient.

Principle
---------

The gradient is rendered by stroking the path with decreasing widths,
setting the color by sampling the gradient at the corresponding position.

On layers, when the gradient is not fully opaque, a mask is added to the layer and the opacity part of gradient
is stroked in a similar way on the mask. The mask is then applied to the layer.

Usage
-----

The script can be found in the right-click menu of a path in the Paths list
(::Ofnuts &rarr; Decorate &rarr; Gradient along path...::{.menupath}).
The gradient is drawn on the active drawable (layer, layer mask, channel, quickmask…).

### Parameters

-   `Width`: this is the total width in pixels of the stroke (`width÷2` on each side of the path).
-   `Reverse gradient`: if false, the gradient is mapped inside-out, if true, it is mapped outside-in.
-   `Precision`: the precision of the rendering. The `Fine` renderings make each stroke smaller than
    its predecessor by one pixels (.5 pixel each side). The settings are currently : .5, 1, 2, 5, and 10 pixels.
    High precision require more stroking passes.
-   `Caps style`, `Join style` and `Miter limit`: these are the stroke line options
    (see the ::Ofnuts &rarr; Edit &rarr; Stroke path::{.menupath}
    documentation for a description). The value of `Current` means that the script will use whatever value is
    currently set in Gimp. the `Miter limit` setting is used only if the `Join style` is explicitly set to `Miter`.


### Usage notes

-   The principle of operation requires the use of a mask to implement transparency, and as a consequence,
    gradients with transparency cannot be used on:

    -   channels (this includes the quickmask)
    -   layer masks
    -   layers that already have a mask

-   The opacity of the gradient sets the opacity of the layer, the gradient isn’t drawn over the existing pixels,
    it completely replaces them.
-   You can render only one half of the gradient by using the path to create a selection.