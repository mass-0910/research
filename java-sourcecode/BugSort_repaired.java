import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class BugSort_repaired{

    final int arraysize = 10;
    int[] A = new int[arraysize];
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    
    public static void main(String[] args){
        System.out.println("Hello World");
        BugSort_repaired b = new BugSort_repaired();
        b.input();
        b.output();
        b.sort();
        b.output();
    }

    public void input(){
        String line;

        Arrays.fill(A, 0);
        try{
            for(int i = 0; i < arraysize; i++){
                if((line = in.readLine()) != null){
                    A[i] = Integer.valueOf(line);
                }
            }
        }catch(IOException e){
            e.printStackTrace();
        }
    }

    public void output(){
        System.out.print("A = [");
        for(int i = 0; i < arraysize; i++){
            System.out.print(String.valueOf(A[i]));
            if(i < arraysize - 1) System.out.print(", ");
        }
        System.out.print("]\n");
    }

    public void sort(){
        for(int j = 0; j < arraysize; j++){
            for(int i = 0; i < arraysize - 1; i++){
                if(A[i] > A[i + 1]){
                    int tmp = A[i];
                    A[i] = A[i + 1];
                    A[i + 1] = tmp;
                }
            }
        }
    }
}