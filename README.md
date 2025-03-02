
How this app works: upload or drop an image into the field and wait for the result. The application identifies the 5 most dominant colors in the image, givess their hex code, a preview of the color and the percentage of the image that each color occupies.

-------------------------------------------------------
Requirements.txt uses:
1.Flask for the web framework
2.OpenCV (opencv-python) for image processing
3.NumPy for numerical operations
4.Pillow for additional image processing support

Main Application (app.py):
-    A Flask application that handles file uploads and color analysis
-   Uses OpenCV's K-means clustering to find the dominant colors
-   Processes images and returns color information in both RGB and HEX formats
-   Includes proper error handling and file validation
-   Automatically cleans up uploaded files after processing
Frontend (templates/index.html):
-   A modern, responsive design with a clean interface
-   Drag-and-drop file upload support
-   Real-time feedback with loading indicators
-   Displays colors in a grid layout with percentages
-   Error handling and user feedback
-   Mobile-friendly design