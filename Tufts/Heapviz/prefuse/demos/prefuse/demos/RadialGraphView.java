package prefuse.demos;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.MouseEvent;
import java.util.HashMap;
import java.util.Iterator;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

import prefuse.Constants;
import prefuse.Display;
import prefuse.Visualization;
import prefuse.action.ActionList;
import prefuse.action.GroupAction;
import prefuse.action.ItemAction;
import prefuse.action.RepaintAction;
import prefuse.action.animate.ColorAnimator;
import prefuse.action.animate.PolarLocationAnimator;
import prefuse.action.animate.QualityControlAnimator;
import prefuse.action.animate.VisibilityAnimator;
import prefuse.action.assignment.ColorAction;
import prefuse.action.assignment.FontAction;
import prefuse.action.filter.VisibilityFilter;
import prefuse.action.layout.CollapsedSubtreeLayout;
import prefuse.action.layout.graph.RadialTreeLayout;
import prefuse.activity.SlowInSlowOutPacer;
import prefuse.controls.ControlAdapter;
import prefuse.controls.DragControl;
import prefuse.controls.FocusControl;
import prefuse.controls.HoverActionControl;
import prefuse.controls.PanControl;
import prefuse.controls.ZoomControl;
import prefuse.controls.ZoomToFitControl;
import prefuse.data.Edge;
import prefuse.data.Graph;
import prefuse.data.Node;
import prefuse.data.Table;
import prefuse.data.Tuple;
import prefuse.data.event.TupleSetListener;
import prefuse.data.expression.AbstractPredicate;
import prefuse.data.expression.BooleanLiteral;
import prefuse.data.expression.NotPredicate;
import prefuse.data.io.GraphMLReader;
import prefuse.data.query.SearchQueryBinding;
import prefuse.data.search.PrefixSearchTupleSet;
import prefuse.data.search.SearchTupleSet;
import prefuse.data.tuple.DefaultTupleSet;
import prefuse.data.tuple.TupleSet;
import prefuse.render.AbstractShapeRenderer;
import prefuse.render.DefaultRendererFactory;
import prefuse.render.EdgeRenderer;
import prefuse.render.LabelRenderer;
import prefuse.util.ColorLib;
import prefuse.util.FontLib;
import prefuse.util.ui.JFastLabel;
import prefuse.util.ui.JSearchPanel;
import prefuse.util.ui.UILib;
import prefuse.visual.VisualItem;
import prefuse.visual.expression.InGroupPredicate;
import prefuse.visual.sort.TreeDepthItemSorter;


/**
 * Demonstration of a node-link tree viewer
 *
 * @version 1.0
 * @author <a href="http://jheer.org">jeffrey heer</a>
 */
public class RadialGraphView extends Display {

    public static final String DATA_FILE = "/Users/sk/Documents/Programming/Visualization/Final Project/new_summarized.xml";
	
    private static final String tree = "tree";
    private static final String treeNodes = "tree.nodes";
    private static final String treeEdges = "tree.edges";
    private static final String linear = "linear";
    
    private LabelRenderer m_nodeRenderer;
    private EdgeRenderer m_edgeRenderer;
    
    private String m_label = "label";
    
    public RadialGraphView(Graph g, String label) {
        super(new Visualization());
        m_label = label;

        // -- set up visualization --
        m_vis.add(tree, g);
        m_vis.setInteractive(treeEdges, null, false);
        
        setNodePropertyDefaults();
        
        m_vis.setVisible(tree, new BooleanLiteral(true), true);
        m_vis.setVisible(treeNodes, new IsHiddenPredicate(), false);
        m_vis.setVisible(treeEdges, new IsAttachedToHiddenPredicate(), false);
        
        // -- set up renderers --
        m_nodeRenderer = new LabelRenderer(m_label);
        m_nodeRenderer.setRenderType(AbstractShapeRenderer.RENDER_TYPE_DRAW_AND_FILL);
        m_nodeRenderer.setHorizontalAlignment(Constants.CENTER);
        m_nodeRenderer.setVerticalAlignment(Constants.CENTER);
        m_nodeRenderer.setRoundedCorner(8,8);
        m_edgeRenderer = new EdgeRenderer();
        
        DefaultRendererFactory rf = new DefaultRendererFactory(m_nodeRenderer);
        rf.add(new InGroupPredicate(treeEdges), m_edgeRenderer);
        m_vis.setRendererFactory(rf);
               
        // -- set up processing actions --
        
        // colors
        ItemAction nodeFillColor = new NodeFillColorAction(treeNodes);
        ItemAction nodeStrokeColor = new NodeStrokeColorAction(treeNodes);
        ItemAction textColor = new TextColorAction(treeNodes);
        m_vis.putAction("textColor", textColor);
        
        ItemAction edgeColor = new ColorAction(treeEdges,
                VisualItem.STROKECOLOR, ColorLib.rgb(200,200,200));
        
        FontAction fonts = new FontAction(treeNodes, 
                FontLib.getFont("Tahoma", 10));
        fonts.add("ingroup('_focus_')", FontLib.getFont("Tahoma", 12));
        
        // recolor
        ActionList recolor = new ActionList();
        recolor.add(nodeStrokeColor);
        recolor.add(nodeFillColor);
        recolor.add(textColor);
        m_vis.putAction("recolor", recolor);
        
        // repaint
        ActionList repaint = new ActionList();
        repaint.add(recolor);
        repaint.add(new RepaintAction());
        m_vis.putAction("repaint", repaint);
        
        // animate paint change
        ActionList animatePaint = new ActionList(400);
        animatePaint.add(new ColorAnimator(treeNodes));
        animatePaint.add(new RepaintAction());
        m_vis.putAction("animatePaint", animatePaint);
        
        // set visibility
        ActionList setVisibility = new ActionList();
        setVisibility.add(new VisibilityFilter(treeNodes, new NotPredicate(new IsHiddenPredicate())));
        setVisibility.add(new VisibilityFilter(treeEdges, new NotPredicate(new IsAttachedToHiddenPredicate())));
        m_vis.putAction("visibility", setVisibility);
        
        // create the tree layout action
        RadialTreeLayout treeLayout = new RadialTreeLayout(tree);
        // treeLayout.setAngularBounds(-Math.PI/2, Math.PI);
        m_vis.putAction("treeLayout", treeLayout);
        
        CollapsedSubtreeLayout subLayout = new CollapsedSubtreeLayout(tree);
        m_vis.putAction("subLayout", subLayout);
        
        // create rerooting
        ActionList reroot = new ActionList();
        reroot.add(new TreeRootAction(tree));
        m_vis.putAction("reroot", reroot);
        
        // create the filtering
        ActionList filter = new ActionList();
        filter.add(fonts);
        filter.add(setVisibility);
        filter.add(treeLayout);
        filter.add(subLayout);
        filter.add(textColor);
        filter.add(nodeFillColor);
        filter.add(edgeColor);
        m_vis.putAction("filter", filter);
        
        // animated transition
        ActionList animate = new ActionList(750);
        animate.setPacingFunction(new SlowInSlowOutPacer());
        animate.add(new QualityControlAnimator());
        animate.add(new VisibilityAnimator(tree));
        animate.add(new PolarLocationAnimator(treeNodes, linear));
        animate.add(new ColorAnimator(treeNodes));
        animate.add(new RepaintAction());
        m_vis.putAction("animate", animate);
        
        // toggle expansion
        ActionList toggleExpansion = new ActionList();
        toggleExpansion.add(new ToggleExpansionAction(treeNodes, this));
        m_vis.putAction("expand", toggleExpansion);
        
        m_vis.alwaysRunAfter("expand", "filter");
        m_vis.alwaysRunAfter("reroot", "filter");
        m_vis.alwaysRunAfter("filter", "animate");
        
        // ------------------------------------------------
        
        // initialize the display
        setSize(600,600);
        setItemSorter(new TreeDepthItemSorter());
        addControlListener(new DragControl());
        addControlListener(new ZoomToFitControl());
        addControlListener(new ZoomControl());
        addControlListener(new PanControl());
        addControlListener(new FocusControl(1, "expand"));
        addControlListener(new FocusControl(2, "reroot"));
        addControlListener(new HoverActionControl("repaint"));
        
        // ------------------------------------------------
        
        // filter graph and perform layout
        m_vis.run("filter");
        
        // maintain a set of items that should be interpolated linearly
        // this isn't absolutely necessary, but makes the animations nicer
        // the PolarLocationAnimator should read this set and act accordingly
        m_vis.addFocusGroup(linear, new DefaultTupleSet());
        m_vis.getGroup(Visualization.FOCUS_ITEMS).addTupleSetListener(
            new TupleSetListener() {
                public void tupleSetChanged(TupleSet t, Tuple[] add, Tuple[] rem) {
                    TupleSet linearInterp = m_vis.getGroup(linear);
                    if ( add.length < 1 ) return; linearInterp.clear();
                    for ( Node n = (Node)add[0]; n!=null; n=n.getParent() )
                        linearInterp.addTuple(n);
                }
            }
        );
        
        SearchTupleSet search = new PrefixSearchTupleSet();
        m_vis.addFocusGroup(Visualization.SEARCH_ITEMS, search);
        search.addTupleSetListener(new TupleSetListener() {
            public void tupleSetChanged(TupleSet t, Tuple[] add, Tuple[] rem) {
                m_vis.cancel("animatePaint");
                m_vis.run("recolor");
                m_vis.run("animatePaint");
            }
        });
    }
    
    public void setNodePropertyDefaults(){
    	HashMap<Integer, Integer> nodeChildren = new HashMap<Integer, Integer>();
    	Node n;
    	for (Iterator i = m_vis.getGroup(treeNodes).tuples(); i.hasNext();){
    		n = (Node) i.next();
    		
    		// Don't reset these if they've been instantiated by some other process!
    		if (!n.canGetInt("children")){
    			n.setInt("children", 0);
    		}
    		if (!n.canGetBoolean("hidden")){
    			n.setBoolean("hidden", false);
    		}
    		
    		if (!n.canGetBoolean("collapsed")){
    			n.setBoolean("collapsed", false);
    		}
    		else{
    			if (n.getBoolean("collapsed")){
    				hideAllBelowNode(n);
    			}
    		}
    		
    		if (!n.canGetInt("owner")){
    			n.setInt("owner", -1);
    		}
    		else{
    			int current = nodeChildren.containsKey(n.getInt("owner")) ? nodeChildren.get(n.getInt("owner")) : 0;
    			nodeChildren.put(n.getInt("owner"), current + 1);
    		}
    	}
    	
    	for (Iterator i = m_vis.getGroup(treeNodes).tuples(); i.hasNext();){
    		n = (Node) i.next();
    		
    		if (nodeChildren.containsKey(n.getInt("id"))){
    			n.setInt("children", nodeChildren.get(n.getInt("id")));
    		}
    		else{
    			n.setInt("children", 0);
    		}
    	}
    }
    
    // Does not collapse the nodes, just hides them.
    public void hideAllBelowNode(Node n){
    	Node neighbor;
		for (Iterator i = n.neighbors(); i.hasNext();){
        	neighbor = (Node) i.next();
        	if (neighbor.getInt("owner") == n.getInt("id")){
        		neighbor.setBoolean("hidden", true);
        		hideAllBelowNode(neighbor);
        	}
		}
    }
    
    // Generally not used, but here as an option.
    // Doesn't expand the nodes, just shows them.
    public void showAllBelowNode(Node n){
    	Node neighbor;
		for (Iterator i = n.neighbors(); i.hasNext();){
        	neighbor = (Node) i.next();
        	if (neighbor.getInt("owner") == n.getInt("id")){
        		neighbor.setBoolean("hidden", false);
        		showAllBelowNode(neighbor);
        	}
		}
    }
    
    public void showExpandedBelowNode(Node n){
    	boolean state = n.getBoolean("collapsed");
    	if (state){
    		return;
    	}
    	Node neighbor;
		for (Iterator i = n.neighbors(); i.hasNext();){
        	neighbor = (Node) i.next();
        	if (neighbor.getInt("owner") == n.getInt("id")){
        		neighbor.setBoolean("hidden", false);
        		showExpandedBelowNode(neighbor);
        	}
		}
    }
    
    // ------------------------------------------------------------------------
    
    public static void main(String argv[]) {
        String infile = DATA_FILE;
        String label = "types";
        
        if ( argv.length > 1 ) {
            infile = argv[0];
            label = argv[1];
        }
        
        UILib.setPlatformLookAndFeel();
        
        JFrame frame = new JFrame("p r e f u s e  |  r a d i a l g r a p h v i e w");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(demo(infile, label));
        frame.pack();
        frame.setVisible(true);
    }
    
    public static JPanel demo() {
        return demo(DATA_FILE, "types");
    }
    
    public static JPanel demo(String datafile, final String label) {
        Graph g = null;
        try {
            g = new GraphMLReader().readGraph(datafile);
        } catch ( Exception e ) {
            e.printStackTrace();
            System.exit(1);
        }
        return demo(g, label);
    }
    
    public static JPanel demo(Graph g, final String label) {        
        // create a new radial tree view
        final RadialGraphView gview = new RadialGraphView(g, label);
        Visualization vis = gview.getVisualization();
        
        // create a search panel for the tree map
        SearchQueryBinding sq = new SearchQueryBinding(
             (Table)vis.getGroup(treeNodes), label,
             (SearchTupleSet)vis.getGroup(Visualization.SEARCH_ITEMS));
        JSearchPanel search = sq.createSearchPanel();
        search.setShowResultCount(true);
        search.setBorder(BorderFactory.createEmptyBorder(5,5,4,0));
        search.setFont(FontLib.getFont("Tahoma", Font.PLAIN, 11));
        
        final JFastLabel title = new JFastLabel("                 ");
        title.setPreferredSize(new Dimension(350, 20));
        title.setVerticalAlignment(SwingConstants.BOTTOM);
        title.setBorder(BorderFactory.createEmptyBorder(3,0,0,0));
        title.setFont(FontLib.getFont("Tahoma", Font.PLAIN, 16));
        
        gview.addControlListener(new ControlAdapter() {
            public void itemEntered(VisualItem item, MouseEvent e) {
                if ( item.canGetString(label) )
                    title.setText(item.getString(label));
            }
            public void itemExited(VisualItem item, MouseEvent e) {
                title.setText(null);
            }
        });
        
        Box box = new Box(BoxLayout.X_AXIS);
        box.add(Box.createHorizontalStrut(10));
        box.add(title);
        box.add(Box.createHorizontalGlue());
        box.add(search);
        box.add(Box.createHorizontalStrut(3));
        
        JPanel panel = new JPanel(new BorderLayout());
        panel.add(gview, BorderLayout.CENTER);
        panel.add(box, BorderLayout.SOUTH);
        
        Color BACKGROUND = Color.WHITE;
        Color FOREGROUND = Color.DARK_GRAY;
        UILib.setColor(panel, BACKGROUND, FOREGROUND);
        
        return panel;
    }
    
    // ------------------------------------------------------------------------
    
    /**
     * Switch the root of the tree by requesting a new spanning tree
     * at the desired root
     */
    public static class TreeRootAction extends GroupAction {
        public TreeRootAction(String graphGroup) {
            super(graphGroup);
        }
        public void run(double frac) {
            TupleSet focus = m_vis.getGroup(Visualization.FOCUS_ITEMS);
            if ( focus==null || focus.getTupleCount() == 0 ) return;
            
            Graph g = (Graph)m_vis.getGroup(m_group);
            Node f = null;
            Iterator tuples = focus.tuples();
            while (tuples.hasNext() && !g.containsTuple(f=(Node)tuples.next()))
            {
                f = null;
            }
            if ( f == null ) return;
            g.getSpanningTree(f);
        }
    }
    
    /**
     * Set node fill colors
     */
    public static class NodeFillColorAction extends ColorAction {
        public NodeFillColorAction(String group) {
            super(group, VisualItem.FILLCOLOR, ColorLib.rgba(255, 255, 255, 0));
            add("ingroup('_search_')", ColorLib.rgb(255,190,190));
        }
                
    } // end of inner class NodeColorAction
    
    public static class NodeStrokeColorAction extends ColorAction{
    	public NodeStrokeColorAction(String group){
    		super(group, VisualItem.STROKECOLOR, ColorLib.rgba(255, 255, 255, 0));
    		add("_hover", ColorLib.gray(220, 255));
    		add("ingroup('_focus_')", ColorLib.gray(220, 255));
    		add(new IsCollapsedPredicate(), ColorLib.rgb(0, 0, 255));
    		add(new IsExpandedPredicate(), ColorLib.rgb(138, 193, 255));
    	}
    }
    
    /**
     * Set node text colors
     */
    public static class TextColorAction extends ColorAction {
        public TextColorAction(String group) {
            super(group, VisualItem.TEXTCOLOR, ColorLib.gray(0));
            add("_hover", ColorLib.rgb(255,0,0));
        }
    } // end of inner class TextColorAction
    
    public static class ToggleExpansionAction extends GroupAction {
    	RadialGraphView graph;
    	
    	public ToggleExpansionAction(String graphGroup, RadialGraphView graph){
    		super(graphGroup);
    		this.graph = graph;
    	}
    	
    	public void run(double frac){
            TupleSet focus = m_vis.getGroup(Visualization.FOCUS_ITEMS);
            if (focus == null || focus.getTupleCount() == 0)
            	return;
            Node n = (Node) focus.tuples().next();
            if (n.getInt("children") == 0){
            	return;
            }
            boolean state = !n.getBoolean("collapsed");
            n.setBoolean("collapsed", state);
            if (state){
            	graph.hideAllBelowNode(n);
            }
            else{
            	graph.showExpandedBelowNode(n);
            }
    	}
    }
 
    public static class IsHiddenPredicate extends AbstractPredicate{
    	public IsHiddenPredicate(){
    		super();
    	}
    	
    	public boolean getBoolean(Tuple t){
    		return t.getBoolean("hidden");
    	}
    }   
    
    public static class IsCollapsedPredicate extends AbstractPredicate{
    	public IsCollapsedPredicate(){
    		super();
    	}
    	
    	public boolean getBoolean(Tuple t){
    		return t.getBoolean("collapsed") && t.getInt("children") > 0;
    	}
    }
    
    public static class IsExpandedPredicate extends AbstractPredicate{
    	public IsExpandedPredicate(){
    		super();
    	}
    	
    	public boolean getBoolean(Tuple t){
    		return !t.getBoolean("collapsed") && t.getInt("children") > 0;
    	}
    }
    
    public static class IsAttachedToHiddenPredicate extends AbstractPredicate{
    	public IsAttachedToHiddenPredicate(){
    		super();
    	}
    	
    	public boolean getBoolean(Tuple t){
    		Edge e = (Edge) t;
    		return e.getSourceNode().getBoolean("hidden") || e.getTargetNode().getBoolean("hidden");
    	}
    }
    
} // end of class RadialGraphView
