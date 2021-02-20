package data_structures;

/**
 * Created by William Fox on 1/18/2017.
 */
public class Tester {
    public static void main(String args[]){
        ArrayLinearList<Integer> list = new ArrayLinearList<Integer>();
        for(int i = 1; i <= 20; i++) {
            list.addFirst(i);
        }
        for(int i = 0; i < 5; i++){
            list.removeLast();
        }
        for (Integer I : list) {
            System.out.println(I);
        }

    }

}
