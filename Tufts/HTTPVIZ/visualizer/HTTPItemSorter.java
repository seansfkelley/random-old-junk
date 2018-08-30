package visualizer;

import prefuse.visual.VisualItem;
import prefuse.visual.sort.ItemSorter;

public class HTTPItemSorter extends ItemSorter {
	public int score(VisualItem item){
		return item.getString(HTTPVisualizer.FIELD_IP) == null ? 0 : 1;
	}
}
