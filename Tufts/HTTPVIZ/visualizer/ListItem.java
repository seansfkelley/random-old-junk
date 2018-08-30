package visualizer;

import prefuse.data.Node;

public class ListItem {
	private Node m_host1, m_host2, m_bkrd;
	private boolean m_host1_sent_more_bytes;
	private long m_activity;
	
	public ListItem(Node host1, Node host2, Node background){
		m_host1 = host1;
		m_host2 = host2;
		m_bkrd = background;
	}
	
	public void addBytes(String host_ip, int bytes){
		int host1_bytes = m_host1.getInt(HTTPVisualizer.FIELD_BYTES_SENT), host2_bytes = m_host2.getInt(HTTPVisualizer.FIELD_BYTES_SENT);
		if (m_host1.getString(HTTPVisualizer.FIELD_IP).equals(host_ip)){
			host1_bytes += bytes;
			m_host1.setInt(HTTPVisualizer.FIELD_BYTES_SENT, host1_bytes);
		}
		else{
			host2_bytes += bytes;
			m_host2.setInt(HTTPVisualizer.FIELD_BYTES_SENT, host2_bytes);
		}
		
		m_host1_sent_more_bytes = host1_bytes > host2_bytes;
		if (m_host1_sent_more_bytes){
			m_host1.setBoolean(HTTPVisualizer.FIELD_IS_SERVER, true);
			m_host2.setBoolean(HTTPVisualizer.FIELD_IS_SERVER, false);
		}
		else{
			m_host1.setBoolean(HTTPVisualizer.FIELD_IS_SERVER, false);
			m_host2.setBoolean(HTTPVisualizer.FIELD_IS_SERVER, true);
		}
		m_bkrd.setInt(HTTPVisualizer.FIELD_BYTES_SENT, host1_bytes + host2_bytes);
		
		m_activity = System.currentTimeMillis();
	}
	
	public Node getServerNode(){
		return m_host1_sent_more_bytes ? m_host1 : m_host2;
	}
	
	public Node getClientNode(){
		return m_host1_sent_more_bytes ? m_host2 : m_host1;
	}
	
	public int getBytesTransferred(){
		return m_bkrd.getInt(HTTPVisualizer.FIELD_BYTES_SENT);
	}
	
	public void setSortPosition(int i){
		m_host1.setInt(HTTPVisualizer.FIELD_SORT_POS, i);
		m_host2.setInt(HTTPVisualizer.FIELD_SORT_POS, i);
		m_bkrd.setInt(HTTPVisualizer.FIELD_SORT_POS, i);
	}

	public long getLastActivity() {
		return m_activity;
	}
}
