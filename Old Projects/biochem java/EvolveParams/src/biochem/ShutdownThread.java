package biochem;

public class ShutdownThread extends Thread{
  Process matlab_process;

  public ShutdownThread(){
    ;
  }

  public ShutdownThread(Process p){
    matlab_process = p;
  }

  public void setMatlabProcess(Process p){
    matlab_process = p;
  }

  @Override
  public void run(){
    GAMain.statusMessage("Shutting down matlab...", 2);
    matlab_process.destroy();
    GAMain.statusMessage("Done!", 2);
  }
}
