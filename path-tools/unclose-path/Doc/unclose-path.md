# unclose-path

This script fixes a incorrect behavior in
Gimp. When using **"stroke"**
fonts (such as those ![external link](external_link_icon.svg)[available
here](http://featurecam.com/general/support/engrave_fonts.asp))

Gimp "closes" all the strokes (perhaps to be able to "fill"
the characters), producing extra line segments.

Unfortunately the strokes remain closed even in a "`Path from text`":

![ClosedStrokes.png](images/ClosedStrokes.png)

This script "uncloses" the strokes to restore a usable path:

![UnclosedStrokes.png](images/UnclosedStrokes.png)

This script bluntly re-opens all strokes. So far this does not
appear to have any ill effects
since in all the fonts encountered, even the strokes that should remain
closed ("O", for instance) do not
rely on the closure to draw the last segment. If you come across a
counter-example, I will be glad to fix the script.
