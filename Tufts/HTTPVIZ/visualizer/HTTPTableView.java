package visualizer;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.geom.Rectangle2D;

import prefuse.Constants;
import prefuse.Display;
import prefuse.action.ActionList;
import prefuse.action.RepaintAction;
import prefuse.action.assignment.ColorAction;
import prefuse.action.layout.Layout;
import prefuse.action.layout.RandomLayout;
import prefuse.action.layout.graph.ForceDirectedLayout;
import prefuse.activity.Activity;
import prefuse.controls.DragControl;
import prefuse.controls.FocusControl;
import prefuse.controls.NeighborHighlightControl;
import prefuse.controls.PanControl;
import prefuse.controls.WheelZoomControl;
import prefuse.controls.ZoomControl;
import prefuse.controls.ZoomToFitControl;
import prefuse.data.expression.parser.ExpressionParser;
import prefuse.render.DefaultRendererFactory;
import prefuse.render.EdgeRenderer;
import prefuse.render.LabelRenderer;
import prefuse.render.PolygonRenderer;
import prefuse.render.ShapeRenderer;
import prefuse.util.ColorLib;
import prefuse.visual.VisualItem;
import prefuse.visual.expression.InGroupPredicate;

public class HTTPTableView extends Display{
    public HTTPTableView(){
    	super(HTTPVisualizer.VISUALIZATION);
    	
    	setupRenderers();
    	setupActions();
    	setupUI();
    	
        m_vis.run("draw");
    }

    private void setupRenderers(){
        DefaultRendererFactory drf = new DefaultRendererFactory();
        
        drf.add(PolygonRenderer.POLYGON + " == null", new LabelRenderer(HTTPVisualizer.FIELD_IP));
        drf.add(PolygonRenderer.POLYGON + " != null", new PolygonRenderer());

        m_vis.setRendererFactory(drf);
    }
    
    private void setupActions(){
        ColorAction fill = new ColorAction(HTTPVisualizer.GROUP_ALL, 
                VisualItem.FILLCOLOR, ColorLib.rgb(200,200,255));
        fill.add(VisualItem.FIXED, ColorLib.rgb(255,100,100));
        fill.add(VisualItem.HIGHLIGHT, ColorLib.rgb(255,200,125));
        
        ActionList draw = new ActionList();
        draw.add(fill);
        draw.add(new ColorAction(HTTPVisualizer.GROUP_ALL, VisualItem.STROKECOLOR, 0));
        draw.add(new ColorAction(HTTPVisualizer.GROUP_ALL, VisualItem.TEXTCOLOR, ColorLib.rgb(0,0,0)));
        ColorAction color = new ColorAction(HTTPVisualizer.GROUP_ALL, VisualItem.FILLCOLOR, ColorLib.rgba(0, 0, 0, 0));
        color.add(PolygonRenderer.POLYGON + " != null", ColorLib.gray(200));
        draw.add(color);
        
        ActionList animate = new ActionList(Activity.INFINITY);
        Layout l = new ListItemLayout();
        l.setLayoutBounds(new Rectangle2D.Float(0, 0, 500, 500));
        animate.add(l);
        // TODO: originally fill
        animate.add(draw);
        animate.add(new RepaintAction());
        
        // finally, we register our ActionList with the Visualization.
        // we can later execute our Actions by invoking a method on our
        // Visualization, using the name we've chosen below.
        m_vis.putAction("draw", draw);
        m_vis.putAction("layout", animate);

        m_vis.runAfter("draw", "layout");
    }
    
    private void setupUI(){
    	setItemSorter(new HTTPItemSorter());
        setSize(new Dimension(700, 700));
        setForeground(Color.GRAY);
        setBackground(Color.WHITE);

        addControlListener(new FocusControl(1));
        // addControlListener(new DragControl());
        addControlListener(new PanControl());
        addControlListener(new ZoomControl());
        addControlListener(new WheelZoomControl());
        addControlListener(new ZoomToFitControl());
        addControlListener(new NeighborHighlightControl());
        
        setForeground(Color.GRAY);
        setBackground(Color.WHITE);
    }
}
