/**
 * William Fox cssc0917
 * Prog2
 */

import com.sun.org.apache.xpath.internal.SourceTree;
import com.sun.xml.internal.bind.v2.model.annotation.RuntimeInlineAnnotationReader;
import data_structures.*;

import java.util.ArrayList;
import java.util.ConcurrentModificationException;

public class FailFastTester {

    public static void main(String[] args) {
        ArrayList<PriorityQueue<Integer>> PQArray = new ArrayList<>();

        PQArray.add(new OrderedArrayPriorityQueue<>());    // 0
        PQArray.add(new OrderedListPriorityQueue<>());     // 1
        PQArray.add(new UnorderedArrayPriorityQueue<>());  // 2
        PQArray.add(new UnorderedListPriorityQueue<>());   // 3

        for (PriorityQueue PQ : PQArray) {
            insertPQ(PQ, 10);
        }

        for (PriorityQueue PQ : PQArray) {
            PQ.insert(256);
            PQ.insert(0);
            if (!PQ.contains(256) & !PQ.contains(0))
                throw new RuntimeException(PQ + " Contains not working");
            System.out.println(PQ + " Contains Test Working");
        }
        System.out.println("-----");

        for (PriorityQueue PQ : PQArray) {
            int peek = (int) PQ.remove();
            if (peek - (int) PQ.peek() > 0)
                throw new RuntimeException("Peek or Order not working");
            System.out.println(PQ + " Peek Test Working");
        }
        System.out.println("-----");

        for (PriorityQueue PQ : PQArray) {
            if (!tryConcurrentModification(PQ))
                throw new RuntimeException(PQ + " Concurrent Mod Break");
            System.out.println(PQ + " Concurrent Mod Work");
        }
        System.out.println("-----");

        for (PriorityQueue PQ : PQArray) {
            if (PQ.remove() == null & PQ.peek() == null & !PQ.contains(1024) & PQ.size() == 0 & PQ.isEmpty())
                System.out.println(PQ + " Empty/Not Found Conditions Work");
        }
        System.out.println("-----");
        insertPQ(PQArray.get(0), 1000);
        insertPQ(PQArray.get(2), 1000);
        for ( PriorityQueue PQ: PQArray){
            System.out.println(PQ.isFull());
        }
    }//Main

    private static void insertPQ(PriorityQueue<Integer> PQ, int ammount) {
        for (int i = 0; i < ammount; i++)
            PQ.insert((int) (Math.random() * 100 + 1));

    }

    private static void printPQ(PriorityQueue PQ) {
        while (!PQ.isEmpty())
            System.out.println(PQ.remove());
        System.out.println("-----");
    }

    /**
     * Returns true if exception is thrown (it should be), false if no exception
     *
     * @param PQ
     * @return boolean
     */
    private static boolean tryConcurrentModification(PriorityQueue<Integer> PQ) {

        try {
            for (Integer I :
                    PQ) {
                PQ.clear();
            }
            return false;
        } catch (ConcurrentModificationException e) {
            return true;
        }
    }

}//Eof
