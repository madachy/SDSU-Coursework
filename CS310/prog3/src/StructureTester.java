
import java.util.Arrays;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.Map;

import data_structures.*;

/**
 * William Fox cssc0917
 * prog3
 */
public class StructureTester {

    public static void main(String[] args) {
        printTesting("HashTable");
        new StructureTester(true, new HashTable<>(10));
        printTesting("OrderedArray");
        new StructureTester(true, new OrderedArrayDictionary<>(10));
        printTesting("Binary Search Tree");
        new StructureTester(false, new BinarySearchTree<>());
        printTesting("Red Black Tree");
        new StructureTester(false, new RedBlackTree<>());
    }

    public StructureTester(Boolean canBeFull, DictionaryADT<Integer, Integer> dict) {
        DictionaryADT<Integer, Integer> dictionary = dict;
        System.out.println("Empty Structure");
        printBool("IsEmpty()", "true", dictionary.isEmpty());
        printBool("isFull()", "false", dictionary.isFull());
        printBool("contains()", "false", dictionary.contains(256));
        printInteger("size()", 0, dictionary.size());

        System.out.println("\nFilled/Full Structure");
        for (int i = 1; i <= 10; i++)
            dictionary.add(i, i);
        printBool("IsEmpty()", "false", dictionary.isEmpty());
        printBool("isFull()", canBeFull.toString(), dictionary.isFull());
        printBool("contains()", "true", dictionary.contains(5));
        printInteger("size()", 10, dictionary.size());
        printBool("add()", String.valueOf((!canBeFull)), dictionary.add(512, 512));

        tuple[] elements = new tuple[dictionary.size()];
        Iterator<Integer> keys = dictionary.keys();
        Iterator<Integer> values = dictionary.values();

        for (int i = 0; keys.hasNext(); i++)
            elements[i] = new tuple(keys.next(), values.next());

        System.out.println("\nCurrent Elements (key, value)");
        System.out.println(Arrays.toString(elements));

        System.out.println("\nTesting Exception Throwing");

        //TODO: UNFUCK THIS MONKEY
        try {
            Iterator<Integer> temp = dictionary.values();
           while(temp.hasNext()){
               dictionary.delete(6);
               if(dictionary.isEmpty()) break;
            }
           throw new RuntimeException("Exception not thrown!!");
        } catch (ConcurrentModificationException e) {
            System.out.println("ConcurrentModProperlyThrown");
            dictionary.add(6, 86);//Cleanup
        }

        keys = dictionary.keys();
        values = dictionary.values();

        for (int i = 0; keys.hasNext(); i++)
            elements[i] = new tuple(keys.next(), values.next());

        System.out.println("\nCurrent Elements (key, value)");
        System.out.println(Arrays.toString(elements));

        System.out.println("\nDeletions and other tests");
        printBool("delete()", "false", dictionary.delete(256));
        printBool("delete()", "true", dictionary.delete(5));
        printBool("duplicateKey add", "false", dictionary.add(4, 4));
        printBool("contains()", "false", dictionary.contains(5));

        System.out.println("\nGetVal/Key");
        printInteger("GetVal", 9, dictionary.getValue(9));
        printInteger("GetVal", null, dictionary.getValue(289));
        printInteger("GetKey", 2, dictionary.getKey(2));
        printInteger("GetVal", null, dictionary.getKey(128));

        System.out.println("\nClearing Structure");
        dictionary.clear();
        System.out.println("[Size()], [isEmpty()], [contains(5)], [delete(7)]");
        System.out.println("[" + dictionary.size() + "], [" + dictionary.isEmpty() + "], ["
                + dictionary.contains(5) + "], [" + dictionary.delete(7) + "]");
    }


    private void printBool(String testing, String expected, boolean actual) {
        System.out.println(testing + " [" + expected + "] {" + actual + "}");
    }

    private void printInteger(String testing, Integer expected, Integer actual) {
        System.out.println(testing + " [" + expected + "] {" + actual + "}");
    }

    private static void printTesting(String structure) {
        System.out.println("---------------------------------------------------------------");
        System.out.println("                           " + structure + "                         ");
        System.out.println("---------------------------------------------------------------");
    }

    public class tuple {
        public Integer key;
        public Integer value;

        public tuple(Integer k, Integer v) {
            key = k;
            value = v;
        }

        public String toString() {
            return ("(" + key + ", " + value + ")");
        }

    }

}