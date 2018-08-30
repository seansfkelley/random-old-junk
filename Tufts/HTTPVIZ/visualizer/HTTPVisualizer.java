package visualizer;

import java.awt.event.ActionEvent;
import java.beans.PropertyChangeListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.ButtonGroup;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JRadioButtonMenuItem;

import prefuse.Visualization;
import prefuse.data.Graph;
import prefuse.data.Node;
import prefuse.data.Schema;
import prefuse.data.Table;
import prefuse.data.tuple.TupleSet;
import prefuse.render.PolygonRenderer;
import prefuse.util.ui.UILib;

public class HTTPVisualizer extends JFrame{
	public static final Comparator CMP_TOTAL = new Comparator(){
		public int compare(Object o1, Object o2) {
			ListItem l1 = (ListItem) o1, l2 = (ListItem) o2;
			
			return l2.getBytesTransferred() - l1.getBytesTransferred();
		}
	};
	
	public static final Comparator CMP_ACTIVITY = new Comparator(){
		public int compare(Object o1, Object o2) {
			ListItem l1 = (ListItem) o1, l2 = (ListItem) o2;
			
			return (int) Math.max(Math.min(l2.getLastActivity() - l1.getLastActivity(), Integer.MAX_VALUE), Integer.MIN_VALUE);
		}
	};
	
	private TupleSet m_endpoints, m_backgrounds;
	private ArrayList<ListItem> m_sorted_items = new ArrayList<ListItem>();
	private HashMap<String, ListItem> m_ip_pair_to_listitem = new HashMap<String, ListItem>();
	private Comparator m_cmp = CMP_TOTAL;
	private int m_max_bytes = 1;

	private static int s_ordinal = 0;
	
	public static final String GROUP_ENDPOINTS = "endpoints";
	public static final String GROUP_BACKGROUND = "bkrds";
	public static final String GROUP_ALL = "all_items";
	
	public static final String FIELD_IP = "ip";
	public static final String FIELD_BYTES_SENT = "sent";
	public static final String FIELD_ORDINAL = "ord";
	public static final String FIELD_SORT_POS = "sort";
	public static final String FIELD_IS_SERVER = "is_server";
	
	public static final Visualization VISUALIZATION = new Visualization();
	public static final Graph GRAPH = new Graph();
	public static final HTTPVisualizer HTTPVIZ = new HTTPVisualizer();
	
	public static void main(String[] args) throws FileNotFoundException {
		HTTPVIZ.setVisible(true);
		HTTPVIZ.readInput(args.length > 0 ? new FileInputStream(args[0]) : System.in);
	}
	
	public HTTPVisualizer(){
		super("HTTP Visualizer");
		
		UILib.setPlatformLookAndFeel();
	    // Move the menubar onto the global menubar for OS X.
        if (System.getProperty("os.name").startsWith("Mac")){
            System.setProperty("apple.laf.useScreenMenuBar", "true");
        }
        
        Table nodes = GRAPH.getNodeTable();
        
    	nodes.addColumn(FIELD_IP, String.class, null);
    	nodes.addColumn(FIELD_BYTES_SENT, int.class, 0);
    	nodes.addColumn(FIELD_ORDINAL, int.class, 0);
    	nodes.addColumn(FIELD_SORT_POS, int.class, 0);
    	nodes.addColumn(FIELD_IS_SERVER, boolean.class, false);
    	nodes.addColumn(PolygonRenderer.POLYGON, float[].class, null);

        VISUALIZATION.add(GROUP_ALL, GRAPH);
    	VISUALIZATION.addFocusGroup(GROUP_ENDPOINTS);
    	VISUALIZATION.addFocusGroup(GROUP_BACKGROUND);
    	
    	m_endpoints = VISUALIZATION.getGroup(GROUP_ENDPOINTS);
    	m_backgrounds = VISUALIZATION.getGroup(GROUP_BACKGROUND);
        
		add(new HTTPTableView());
		
		createMenubar();
		
        pack();
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	private void createMenubar(){
		JMenuBar menubar = new JMenuBar();
		JMenu menu = new JMenu("Sorting");
		ButtonGroup bg = new ButtonGroup();
		
		JRadioButtonMenuItem jrbmi = new JRadioButtonMenuItem(new AbstractAction("Bytes Transferred"){
			public void actionPerformed(ActionEvent arg0) {
				m_cmp = CMP_TOTAL;
				sort();
			}
		});
		bg.add(jrbmi);
		menu.add(jrbmi);
		jrbmi.setSelected(true);
		
		jrbmi = new JRadioButtonMenuItem(new AbstractAction("Latest Activity"){
			public void actionPerformed(ActionEvent arg0) {
				m_cmp = CMP_ACTIVITY;
				sort();
			}
		});
		bg.add(jrbmi);
		menu.add(jrbmi);
		
		menubar.add(menu);
		
		setJMenuBar(menubar);
	}
	
	private void readInput(InputStream in){
		BufferedReader stdin = new BufferedReader(new InputStreamReader(in));
		while (true){
			String s = null;
			try {
				s = stdin.readLine();
			} catch (IOException e) {
				e.printStackTrace();
				System.exit(0);
			}
			
			if (s == null) break;
			String[] split = s.split(";");
			String from = split[0], to = split[1], data = split[2];
			addToGraph(from, to, data.length() / 2); // Divide by 2 because 2 hex characters represent 1 byte.
			extractImage(data);
		}
		System.out.println("Reached end of input.");
	}
	
	private void addToGraph(String src_ip, String dst_ip, int bytes){
		ListItem item = m_ip_pair_to_listitem.get(src_ip + ";" + dst_ip);
		if (item == null){
			Node h1 = GRAPH.addNode(), h2 = GRAPH.addNode(), bkrd = GRAPH.addNode();
			
			h1.setString(FIELD_IP, src_ip);
			h1.setInt(FIELD_ORDINAL, s_ordinal);
			h1.setBoolean(FIELD_IS_SERVER, true);
			m_endpoints.addTuple(h1);
			
			h2.setString(FIELD_IP, dst_ip);
			h2.setInt(FIELD_ORDINAL, s_ordinal);
			m_endpoints.addTuple(h2);

			bkrd.setInt(FIELD_ORDINAL, s_ordinal);
			bkrd.set(PolygonRenderer.POLYGON, new float[8]);
			m_backgrounds.addTuple(bkrd);
			
			s_ordinal++;
			
			item = new ListItem(h1, h2, bkrd);
			m_ip_pair_to_listitem.put(src_ip + ";" + dst_ip, item);
			m_ip_pair_to_listitem.put(dst_ip + ";" + src_ip, item);
			
			m_sorted_items.add(item);
		}
		
		item.addBytes(src_ip, bytes);
		m_max_bytes = Math.max(item.getBytesTransferred(), m_max_bytes);
		sort();
	}
	
	private void extractImage(String s){
		hexStringToByteArray(s);
	}
	
	// Courtesy of Stack Overflow: 
	// http://stackoverflow.com/questions/140131/convert-a-string-representation-of-a-hex-dump-to-a-byte-array-using-java
	public static byte[] hexStringToByteArray(String s) {
	    int len = s.length();
	    byte[] data = new byte[len / 2];
	    for (int i = 0; i < len; i += 2) {
	        data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
	                             + Character.digit(s.charAt(i + 1), 16));
	    }
	    return data;
	}
	
	public int getMaxBytes(){
		return m_max_bytes;
	}
	
	public void sort(){
		Collections.sort(m_sorted_items, m_cmp);
		
		int i = 0;
		for (Iterator<ListItem> l_iter = m_sorted_items.iterator(); l_iter.hasNext(); ){
			l_iter.next().setSortPosition(i++);
		}
	}
}
