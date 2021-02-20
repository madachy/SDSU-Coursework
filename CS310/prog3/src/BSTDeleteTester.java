/**
 * William Fox cssc0917
 * prog3 ${FILE_NAME}
 */
import data_structures.*;

import java.util.Iterator;

public class BSTDeleteTester {
    private static final Integer[] NUMBERS = {50, 30,70,60,68,63,62,65};
    public static void main(String[] args){
        DictionaryADT<Integer, Integer> dictionary = new BinarySearchTree<>();
        for (Integer i: NUMBERS) dictionary.add(i, i);
        printBst(dictionary);
        dictionary.delete(50);
        printBst(dictionary);


    }//main

    public static void printBst(DictionaryADT<Integer,Integer> dictionary){
        Iterator<Integer> iterator = dictionary.keys();
        Integer i;
        for (i = null;  iterator.hasNext() ; i = iterator.next())
            if (i != null)
                System.out.print(i + ", ");
        System.out.println(i);
    }

}//Eof
