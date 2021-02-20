/**
 * William Fox cssc0917
 * Prog2
 */

import data_structures.*;

public class MyDriver {
    public MyDriver() {
        runTestsUAPQ();
        PriorityQueue<Integer> PQ = new UnorderedArrayPriorityQueue<>();

        for (int i = 0; i < 1000; i++) {
            PQ.insert(i);
        }
        System.out.println("1000: " + PQ.size() + " || false: " + PQ.insert(1024) + " || 0: " + PQ.remove());
        for (Integer I : PQ) {
            System.out.print(I + ", ");
        }
        System.out.println();
        PQ.clear();

        System.out.println("true: " + PQ.isEmpty() + " || false: " + PQ.isFull() + " || null: " + PQ.peek());
        System.out.println("null: " + PQ.remove() + " || false: " + PQ.contains(128) + " || true: " + PQ.insert(256));
        System.out.println("256: " + PQ.peek() + " || 1: " + PQ.size());
        PQ.insert(16);
        PQ.insert(4);
        System.out.println("4: " + PQ.peek() + " || 4: " + PQ.remove());
        System.out.println("true: " + PQ.contains(16) + " || true: " + PQ.contains(256));
        PQ.clear();
        System.out.println("false: " + PQ.contains(7));
        for (int i = 0; i < 10; i++) {
            Integer random = (int )(Math.random() * 500 + 1);
            PQ.insert(random);
        }
        for (int i = 0; i < 10; i++) {
            System.out.print(PQ.remove() + ", ");
        }
        System.out.println();
    }

    private void runTestsUAPQ() {

    }

    public static void main(String[] args) {
        new MyDriver();
    }
}
