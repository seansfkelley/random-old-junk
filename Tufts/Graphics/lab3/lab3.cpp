// Sean Kelley
// OS X 10.6
// Everything should work as specified. The only code added outside the expected functions are the two inlined functions immediately following:

#include "lab3.h"

#include <algorithm>

template<class T>
inline T min(T& a, T& b, T& c){
    return min(a, min(b, c));
}

template<class T>
inline T max(T& a, T& b, T& c){
    return max(a, max(b, c));
}

void init() {
	textureFile1 = "stonehenge.bmp";
	textureFile2 = "checker.bmp";

	// Initialize M to identity
	mtxIdentity(M);

	/********************************************************
	 * Endpoints for the triangle in world coordinates
	 *******************************************************/
	gTriangle.v0.x = 50;
	gTriangle.v0.y = 0;
	gTriangle.v0.z = 0;

	gTriangle.v1.x = 0;
	gTriangle.v1.y = 50;
	gTriangle.v1.z = 0;

	gTriangle.v2.x = 0;
	gTriangle.v2.y = 0;
	gTriangle.v2.z = 50;
	/********************************************************
	 * Normalized texture coordinate endpoints for triangle
	 *******************************************************/
	gTriangle.tex0.x = 0.35;
	gTriangle.tex0.y = 0.35;

	gTriangle.tex1.x = 0.65;
	gTriangle.tex1.y = 0.65;

	gTriangle.tex2.x = 0.65;
	gTriangle.tex2.y = 0.35;

	/********************************************************
	 * initialize coordinate axies
	 *******************************************************/

	gXaxis.x=100;
	gXaxis.y=0;
	gXaxis.z=0;

	gYaxis.x=0;
	gYaxis.y=100;
	gYaxis.z=0;

	gZaxis.x=0;
	gZaxis.y=0;
	gZaxis.z=100;

	gOrigin.x=0;
	gOrigin.y=0;
	gOrigin.z=0;
}

float LineEquation( float x0, float y0,
	    			float x1, float y1,
    				float xi, float yi) {

	return (xi - x0) * (y1 - y0) - (yi - y0) * (x1 - x0);
}

void ForceEdgeVertOrient(Edge *edge){
	if(edge->y0 > edge->y1){
		float temp = edge->x0;
		edge->x0 = edge->x1;
		edge->x1 = temp;
		temp = edge->y0;
		edge->y0 = edge->y1;
		edge->y1 = temp;
	}
}

int convertEdgetoTblEdge(Edge edge, TblEdge *newEdge){
	ForceEdgeVertOrient(&edge);
	newEdge->ymax = edge.y1;
	newEdge->revSlope = (edge.x1 - edge.x0)/(edge.y1 - edge.y0);
	newEdge->x = edge.x0;
	return (int)edge.y0;
}

void setXintersect(TblEdge *edge){
	edge->x = edge->x + edge->revSlope; 
}

void fillSpan(int start, int stop, int scanline, Color c, Raster* image){
	for(int i=start; i<stop; i++){
		image->setPixel(i, scanline, c);
	}
}

int getFirstScanline(int *scan2GEV, int height){
	for(int i=0; i<height; i++){
		if(scan2GEV[i] != -1){
			return i;
		}
	}
	return height;
}

bool SortByX (TblEdge &edge1, TblEdge &edge2)
{
	return (edge1.x < edge2.x);
}

bool SortByY (Edge *e1, Edge *e2)
{
	Vertex e1Min, e2Min;
	float x1Min, x2Min;
	x1Min = (e1->x0 < e1->x1) ? e1->x0 : e1->x1;
	x2Min = (e2->x0 < e2->x1) ? e2->x0 : e2->x1;
	if (e1->y0 < e1->y1) {
		e1Min.x = e1->x0;
		e1Min.y = e1->y0;
	}
	else {
		e1Min.x = e1->x1;
		e1Min.y = e1->y1;
	}
	if (e2->y0 < e2->y1) {
		e2Min.x = e2->x0;
		e2Min.y = e2->y0;
	}
	else {
		e2Min.x = e2->x1;
		e2Min.y = e2->y1;
	}
	if (e1Min.y != e2Min.y)
		return (e1Min.y < e2Min.y);
	return (x1Min < x2Min);
}

void FillPolygon(Edge *edgeArr,
                 int nEdges,
                 Color fill,
                 Raster* image) {
	/** Create global edge vector (GEV)
		vector of lists of edges grouped by their ymins **/

	int *scan2GEV = new int[image->getHeight()]; // assoc scanline to GEV index
	vector<EdgeList*> GEV; // Global Edge Vector (ordered by ymin)

	EdgeList *slEdgeList; // scan line edge list
	TblEdge *newEdge;		

	for(int i=0; i<image->getHeight(); i++){
		scan2GEV[i] = -1; // set default 
	}

	for(int i=0; i<nEdges; i++){
		if(edgeArr[i].y0 != edgeArr[i].y1){ // exclude horizontal lines m = inf
			newEdge = new TblEdge;
			int y0 = convertEdgetoTblEdge(edgeArr[i], newEdge);
		
			int GEVindex = scan2GEV[y0];
			if(GEVindex == -1){
				// make a new list for ymins at this scan line
				slEdgeList = new EdgeList;
				slEdgeList->push_back(*newEdge);
				GEV.push_back(slEdgeList);
				scan2GEV[y0] = GEV.size()-1;
			}else{
				// add edge to existing list
				slEdgeList = GEV.at(GEVindex);
				slEdgeList->push_back(*newEdge);
				slEdgeList->sort(SortByX);
			}
		}
	}

	/** Create active edge list (AEL)
		and being drawing spans       **/

	int first = getFirstScanline(scan2GEV, image->getHeight());

	EdgeList *AEL;	// Active Edge List
    EdgeListIt AELit; // AEL iterator

	AEL = GEV.at(scan2GEV[first]); // Init AEL
	AELit = AEL->begin();

	for(int scanLine=first; scanLine<gHeight; scanLine++){
		// fill spans
		AELit = AEL->begin();
		while(AELit != AEL->end()){
			int start = AELit->x;
			int stop;
			if(++AELit != AEL->end()){
				stop = AELit->x;
				AELit++;
			}else{
				stop = image->getWidth();
			}

			fillSpan(start, stop, scanLine, fill, image);
		}

		// Prepare AEL for next scanline
		int nextScanLine = scanLine+1;

		EdgeList *nextAEL = new EdgeList;
		// First review current AEL edges
		for(AELit = AEL->begin(); AELit != AEL->end(); AELit++){
			if(AELit->ymax != nextScanLine){
				setXintersect(&(*AELit));
				nextAEL->push_back(*AELit);	
			}
		}
		// Look for new edges to add
		if(nextScanLine < image->getHeight()){
			if(scan2GEV[nextScanLine] != -1){
				EdgeList *el = GEV.at(scan2GEV[nextScanLine]);
				for(EdgeListIt t = el->begin(); t != el->end(); t++){
					nextAEL->push_back(*t);
				}
			}
		}
		delete AEL;
		AEL = nextAEL;
		AEL->sort(SortByX);
	}
	delete []scan2GEV;
	GEV.clear();
}

void FillTextureTriangle(float x0, float y0,
						 float x1, float y1,
                         float x2, float y2,
						 float xt0, float yt0,
						 float xt1, float yt1,
						 float xt2, float yt2,
						 Raster* image, Raster* texImage) {
    float edge_norm_0 = 1 / LineEquation(x0, y0, x1, y1, x2, y2),
          edge_norm_1 = 1 / LineEquation(x1, y1, x2, y2, x0, y0),
          edge_norm_2 = 1 / LineEquation(x2, y2, x0, y0, x1, y1);

    int t_width = texImage->getWidth(), t_height = texImage->getHeight();
    // Iterate over the triangle's bounding box. Not the best, but way better than
    // going over the entire image.
    int xmax = ceil(max(x0, x1, x2)), ymax = ceil(max(y0, y1, y2));
    for(int i = floor(min(x0, x1, x2)); i < xmax; i++){
        for(int j = floor(min(y0, y1, y2)); j < ymax; j++){
            float b0 = edge_norm_0 * LineEquation(x0, y0, x1, y1, i, j),
                  b1 = edge_norm_1 * LineEquation(x1, y1, x2, y2, i, j),
                  b2 = edge_norm_2 * LineEquation(x2, y2, x0, y0, i, j);

            // 204 glorious columns!
            if(b0 > 0 && b1 > 0 && b2 > 0) image->setPixel(i, j, texImage->getPixel((int) (t_width * (b1 * xt0 + b2 * xt1 + b0 * xt2) + 0.5f), (int) (t_height * (b1 * yt0 + b2 * yt1 + b0 * yt2) + 0.5f)));
        }
    }
}

Vector3D getTriangleNormalVector(Triangle t) {
    return vecNorm(vecCross(vecSub(t.v0, t.v2), vecSub(t.v0, t.v1)));
}

void draw3D (char doWhat) {
	float a, b, c, xmin, xmax, ymin, ymax, zmin, zmax, deg;
	int axis;
	Vector3D xaxis=gXaxis, yaxis=gYaxis, zaxis=gZaxis, origin=gOrigin;
	Triangle triangle = gTriangle;
	switch(doWhat) {
		case 'T': // Revert to the identity transformation matrix
		case 'I': // Identity matrix
            mtxIdentity(M);
            break;
			
		case 'M': // Translate
			fscanf(gFp, "%f %f %f\n", &a, &b, &c);
			mtxTranslate(M, a, b, c);
            break;

		case 'S': // Scale
			fscanf(gFp, "%f %f %f\n", &a, &b, &c);
			mtxScale(M, a, b, c);
            break;

		case 'R': // Rotate
			fscanf(gFp, "%d %f\n", &axis, &deg);
			mtxRotate(M, axis, deg);
            break;

		case 'O': // Orthographic projection
			fscanf( gFp, "%f %f %f %f %f %f\n", &xmin, &xmax, &ymin, &ymax,
					&zmin, &zmax);
			mtxOrthographic(M, xmin, xmax, ymin, ymax, zmin, zmax);
			//----Scale by window height and width
			mtxScale(M, gWidth/2, gHeight/2, 1); 
            break;
	}
	// Transform triangle vertices using M
    triangle.v0 = mtxTransformPoint(M, triangle.v0);
    triangle.v1 = mtxTransformPoint(M, triangle.v1);
    triangle.v2 = mtxTransformPoint(M, triangle.v2);
	
	// Clear old triangle from image
	gImage->clear();

	// Check post transformed triangle normal vector to
	// Determine whether to use gTexture1 or gTexture2
	Raster * mTexture;
	if (getTriangleNormalVector(triangle).z >= 0)
		mTexture = gTexture1;
	else
		mTexture = gTexture2;


	//----Project transformed triangle into image space
	//----and rasterize using FillTextureTriangle
	//----rasterize into the Raster global variable gImage
	FillTextureTriangle(triangle.v0.x, triangle.v0.y, triangle.v1.x,
						triangle.v1.y, triangle.v2.x, triangle.v2.y, 
						triangle.tex0.x, triangle.tex0.y, triangle.tex1.x, 
						triangle.tex1.y, triangle.tex2.x, triangle.tex2.y,
						gImage, mTexture);

	origin = mtxTransformPoint(M, origin);
	xaxis = mtxTransformPoint(M, xaxis);
	yaxis = mtxTransformPoint(M, yaxis);
	zaxis = mtxTransformPoint(M, zaxis);

	gImage->drawLine(origin.x,origin.y,xaxis.x,xaxis.y);
	gImage->drawLine(origin.x,origin.y,yaxis.x,yaxis.y);
	gImage->drawLine(origin.x,origin.y,zaxis.x,zaxis.y);	
}

void drawPolygon() {
	Edge* edgeArr;
	float* points;
	int i, ip, n;
	Color c, c1, c2, c3;
	
	//----Read in number of points to follow
	fscanf(gFp, "%i", &n);

	//----Read in the color with which to fill the polygon
	fscanf(gFp, "%f", &c.r);
	fscanf(gFp, "%f", &c.g);
	fscanf(gFp, "%f", &c.b);

	//----Allocate memory
	points = (float *) malloc(2 * (n + 1) * sizeof(float));
	edgeArr = (Edge *) malloc(n * sizeof(Edge));

	//----Read in points
	for (i = 0; i < 2 * n; i++) {
		fscanf(gFp, "%f", &points[i]);
	}
	points[2 * n] = points[0];
	points[2 * n + 1] = points[1];

	//----Convert points to edges
	for (i = 0; i < n; i++) {
		ip = 2 * i;

		edgeArr[i].x0 = points[ip];
		edgeArr[i].y0 = points[ip + 1];
		edgeArr[i].x1 = points[ip + 2];
		edgeArr[i].y1 = points[ip + 3];
	}
	//ClearImage(gImage, gBackground);

	FillPolygon(edgeArr, n, c, gImage);

	free(edgeArr);
	free(points);
}

void keyboard (unsigned char key, int x, int y) {
	// key = key pressed; x, y = mouse position on key press

	char doWhat;
	float a, b, c, xmin, xmax, ymin, ymax, zmin, zmax, deg;
	int axis;
	Vector3D xaxis=gXaxis, yaxis=gYaxis, zaxis=gZaxis, origin=gOrigin;
	Triangle triangle = gTriangle;


	//----Check for Exit characters (x, q, esc)
    if (key == 'x' || key == 'X' || key == 'q' || key == 'Q' || key == 27) {
		delete gImage;
		delete gTexture1;
		delete gTexture2;
		fclose(gFp);
		exit(0);//----Exit now
	}

    if (feof(gFp)) return;			//----Return if file empty

    //----Read in command from input file
    fscanf(gFp, " %c", &doWhat);


	if (doWhat == 'P') {
		drawPolygon();
	} else draw3D(doWhat); // Else assume its a 3D value and draw accordingly

	glutPostRedisplay();
}



/*******************************************************
 *  void display(void)
 *
 *  GLUT window-repainting callback. Put all code in here
 *  that you need to paint your image.
 *******************************************************/
void display (void) {
    //----Tell openGL that the pixels are sequential (ie
    //----they were not aligned on certain boundaries when
    //----written to memory)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

	//----Draw the image pixels to our window
    glRasterPos2i(gLeft, gBottom);
	//----Apply transforms and render triangle
	//Apply3DTransform ();

	glDrawPixels(gWidth, gHeight, GL_RGB, GL_FLOAT, gImage->getPixels());

	//----Force remaining drawing
    glFlush();
}

//-------------------------------------------------------------------
// Read an image from disk. A NULL is returned if the request cannot
// be satisfied  (e.g., the specified file does not exist).
//-------------------------------------------------------------------
Raster *rtReadImage (char *fileName) {
    int               x, y;
    int	              n, lineLength, mod, add;
    float             *pRGBA;
    FILE              *fd;
    BITMAPFILEHEADER  bmpHeader;
    BITMAPINFOHEADER  bmpInfo;
    Raster           *image;
    unsigned char     r, g, b;


    //----Read the BMP header
    fd = fopen(fileName, "rb");
    if (!fd) return NULL;
    //fread(&bmpHeader, sizeof(BITMAPFILEHEADER), 1, fd);
	fread(&bmpHeader, 14, 1, fd);
    fread(&bmpInfo, sizeof(BITMAPINFOHEADER), 1, fd);


    //----Create an image of the specified size
	image = new Raster(bmpInfo.biWidth, bmpInfo.biHeight, 0, 0);

    if (image == 0) return(0);


    //----Read the RGB data from disk and set each color pixel
    pRGBA = image->getPixels();

    // Determine num bytes remain after last 4 byte boundary
    mod = (image->getWidth() * 3) % 4;

    // Determine the number of extra bytes to be added
    add = (mod ? 4 - mod : 0);

    lineLength = image->getWidth() * 3 + add;	// Should be divisible by 4

    for (y = 0; y < image->getHeight(); ++y) {
        //----Read the current scanline of color data
        n = lineLength;
        for (x = 0; x < image->getWidth(); ++x) {
            fread(&b, 1, 1, fd);
            fread(&g, 1, 1, fd);
            fread(&r, 1, 1, fd);
            *(pRGBA + 2) = (float) (b) / 255.f;
            *(pRGBA + 1) = (float) (g) / 255.f;
            *(pRGBA + 0) = (float) (r) / 255.f;
            pRGBA += 3;
            n -= 3;
        }
        //----Seek to the start of the next scanline
        while (n > 0) {
            unsigned char pad = 0;
            fread(&pad, 1, 1, fd);
            --n;
        }
    }

    fclose(fd);
    return(image);
}


/*******************************************************
 *  main
 *
 *  Main entry point for this program.
 *  main will
 *   1. Initialize your GLUT window and data
 *   2. Set up callbacks
 *   3. Enter the main event loop.
 *******************************************************/
int main (int argc, char* argv[]) {
    //----Open command file
    gFp = fopen("input3d.txt", "rt");
    if (!gFp) {
		printf("Error opening input file.\n");
		exit(0);
	}

    //----Read in widow size
    fscanf(gFp, "%d %d\n", &gWidth, &gHeight);

    gRight = gWidth / 2;
    gLeft = -1 * gRight;
    gTop = gHeight / 2.f;
    gBottom = -1 * gTop;

    //----Tell GLUT to use a single buffer with three
    //----color channels
	glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    //----Set the window size, location
    glutInitWindowSize(gWidth, gHeight);
    glutInitWindowPosition(200, 200);

    //----Create a window with a title.
    glutCreateWindow("Homework 3");

    //----Set background color
    glClearColor(0, 0, 0, 1);

    //----Set viewing window
    glViewport(gLeft, gBottom, (GLsizei) gWidth, (GLsizei) gHeight);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho (gLeft, gRight, gBottom, gTop, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);

	//----initialize global variables
	init();

	//----Allocate raster
	gImage = new Raster(gWidth, gHeight, gLeft, gBottom);
	gImage->clear();

	//---Fill texture image
	gTexture1 = rtReadImage(textureFile1);
	gTexture2 = rtReadImage(textureFile2);
	if (!gTexture1 || !gTexture2) {
		printf("Error opening texture file.\n");
		exit(0);
	}

    //----Register GLUT callback functions
    glutDisplayFunc (display);
    glutKeyboardFunc (keyboard);

    //----Enter the GLUT event loop.
    glutMainLoop();

    return 0;
}
