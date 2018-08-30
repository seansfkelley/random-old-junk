class FloatTable{
  HashMap data;
  String[] rows, cols;
  
  public FloatTable(String tsvFilename){
    data = new HashMap();
    
    String[] data_rows = loadStrings(tsvFilename);
    
    cols = subset(split(data_rows[0], TAB), 1);
    rows = new String[data_rows.length - 1];
    
    for (int i = 0; i < rows.length; ++i){
      String[] current_row = split(data_rows[i + 1], TAB);
      rows[i] = current_row[0];
      
      float[] row_data = new float[cols.length];
      for (int j = 0; j < cols.length; ++j){
        row_data[j] = Float.valueOf(current_row[j + 1]);
      }
      
      data.put(rows[i], row_data);
    }
    
    rows = sort(rows);
  }
  
  public String[] getRowNames(){
    return rows;
  }
  
  public String[] getColumnNames(){
    return cols;
  }
  
  public int getNumRows(){
    return rows.length;
  }
  
  public int getNumColumns(){
    return cols.length;
  }
  
  public float[] getRow(String row){
    return (float[]) data.get(row);
  }
  
  // Slow!
  public float[] getColumn(int col){
    float[] values = new float[rows.length];
    for (int i = 0; i < rows.length; ++i){
      values[i] = getValue(rows[i], col);
    }
    return values;
  }
  
  public float getValue(String row, int col){
    return ((float[]) data.get(row))[col];
  }
}
