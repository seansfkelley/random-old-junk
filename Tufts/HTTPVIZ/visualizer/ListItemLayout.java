package visualizer;

import java.awt.geom.Rectangle2D;
import java.util.Iterator;

import prefuse.action.layout.Layout;
import prefuse.render.PolygonRenderer;
import prefuse.visual.VisualItem;

public class ListItemLayout extends Layout {
	

	public void run(double frac) {
        Rectangle2D b = getLayoutBounds();
        int x, y;
        double w = b.getWidth();
        double max_bytes_factor = 1.0 / HTTPVisualizer.HTTPVIZ.getMaxBytes();
        
        for (Iterator<VisualItem> v_iter = HTTPVisualizer.VISUALIZATION.visibleItems(); v_iter.hasNext(); ){
        	VisualItem item = v_iter.next();
        	
        	if (item.get(PolygonRenderer.POLYGON) == null){
	            x = (int) (b.getX() + (item.getBoolean(HTTPVisualizer.FIELD_IS_SERVER) ? b.getWidth() - item.getBounds().getWidth() / 2 : item.getBounds().getWidth() / 2));
	            y = (int) (b.getY() + item.getInt(HTTPVisualizer.FIELD_SORT_POS) * 32);
	            setX(item, null, x);
	            setY(item, null, y);
        	}
        	else{
	            x = (int) b.getX();
	            y = (int) (b.getY() + item.getInt(HTTPVisualizer.FIELD_SORT_POS) * 16 + 8);
	            setX(item, null, x);
	            setY(item, null, y);
	            
	            float[] points = (float[]) item.get(PolygonRenderer.POLYGON);
	            
	            points[0] = x; points[1] = y;
	            points[2] = x + (int) (item.getInt(HTTPVisualizer.FIELD_BYTES_SENT) * max_bytes_factor * w); points[3] = y;
	            points[4] = points[2]; points[5] = y - 30;
	            points[6] = x; points[7] = y - 30;
	            
	            // Necessary?
	            item.set(PolygonRenderer.POLYGON, points);
        	}
        }
	}
}
