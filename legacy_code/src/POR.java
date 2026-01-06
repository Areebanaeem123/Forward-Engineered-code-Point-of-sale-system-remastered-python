
import java.io.*;
import pos.util.TempFileManager;

public class POR extends PointOfSale {
  long phoneNum;
  
  public POR(long phoneNum){
    this.phoneNum = phoneNum;
  };
  
  public void deleteTempItem(int id){
    try {
      TempFileManager.deleteTempItem("Rental", transactionItem, id, String.valueOf(phoneNum));
    } catch (IOException ex) {
      System.err.println("Error deleting temp item: " + ex.getMessage());
    }
  }
  
  @SuppressWarnings("static-access")
public double endPOS(String textFile){
    Management man = new Management();
    man.addRental(this.phoneNum, this.transactionItem);
    detectSystem();
    if (transactionItem.size()>0){
      totalPrice = totalPrice*tax; //calculates price with tax
      //prints total with taxes
      //bool=payment();
      //f(bool==true){
        /*for (int counter = 0; counter < transactionItem.size(); counter++){
          //prints item name - price
          System.out.format("%d %s x %d  --- $ %.2f\n", transactionItem.get(counter).getItemID(),transactionItem.get(counter).getItemName(),
                            transactionItem.get(counter).getAmount(), 
                            transactionItem.get(counter).getPrice()*transactionItem.get(counter).getAmount());
        }
        System.out.format("Total with taxes: %.2f\n", totalPrice);
        inventory.updateInventory(textFile, transactionItem, databaseItem,true);
      }*/
      inventory.updateInventory(textFile, transactionItem, databaseItem,true);
    }
    //delete log file
    File file = new File(tempFile);
    file.delete();
    databaseItem.clear();
    transactionItem.clear();
    return totalPrice;
  }
  
  public void retrieveTemp(String textFile){
    try{
      FileReader fileR = new FileReader(tempFile);
      BufferedReader textReader = new BufferedReader(fileR);
      String line=null;
      String[] lineSort;
      line=textReader.readLine();
      inventory.accessInventory(textFile, databaseItem);
      line=textReader.readLine();
      System.out.println("Phone number:");
      System.out.println(line);
      
      while ((line = textReader.readLine()) != null)
      {
        lineSort = line.split(" ");
        int itemNo = Integer.parseInt(lineSort[0]);
        int itemAmount = Integer.parseInt(lineSort[1]);
        enterItem(itemNo,itemAmount);
      }
      textReader.close();
      updateTotal();
    }
    catch(FileNotFoundException ex) {
      System.out.println(
                         "Unable to open file 'temp'"); 
    }
    catch(IOException ex) {
      System.out.println(
                         "Error reading file 'temp'");  
    }

  }
}
