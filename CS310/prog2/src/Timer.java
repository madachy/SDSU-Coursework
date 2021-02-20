/*  Timer.java
    A sample class to assist in performing empirical timing tests
    for your project #2.

    This timer includes only add/delete cycle times.
    The structure size is not doubled each time, but increases in a
    linear fashion.

    If it takes too long on your machine, reduce structureSize and
    increment.  Note that both vars must have same value.

    CS310 Spring 2017
    Alan Riggins
*/


import data_structures.*;

import java.io.IOException;
import java.io.PrintWriter;

public class Timer {
    public static void main(String[] args) {
        try {
            PrintWriter writer = new PrintWriter("Timing_Tests.txt", "UTF-8");
            writer.println("First Test");
            System.out.println("Starting Tests");
            new Timer(writer);
            System.out.println("First Test Completed");
            writer.println("Second Test");
            new Timer(writer);
            System.out.println("Second Test Completed");
            writer.println("Third Test");
            new Timer(writer);
            System.out.println("Third Test Completed");
            writer.println("Fourth Test");
            new Timer(writer);
            System.out.println("Fourth Test Completed");
            writer.println("Fifth Test");
            new Timer(writer);
            System.out.println("Fifth Test Completed");
            writer.close();
        } catch (IOException e) {
            System.out.println(e + " Something Broke, sorry.");
        }
    }

    public Timer(PrintWriter writer) {
        int iterations = 30;  // number of timing tests
        int workSize = 10000;   // size of add/removeMin cycle loop
        int structureSize = 10000;  // initial size of PQ
        int increment = 10000; // make this the same size as structureSize
        int loopStructureSize = structureSize; // helper var


        long start = 0, stop = 0;


        PriorityQueue<Integer> pq =
                // new OrderedArrayPriorityQueue<Integer>(512000);
                //new UnorderedArrayPriorityQueue<Integer>(512000);
                new OrderedListPriorityQueue<Integer>();
               // new UnorderedListPriorityQueue<Integer>();

        for (int i = 0; i < iterations; i++) {
            // build structure first

            for (int j = 0; j < increment; j++) {
                int x = (int) (Integer.MAX_VALUE * Math.random());
                pq.insert(x);
            }

            // time for add/removeMin cycles
            start = System.currentTimeMillis();
            for (int j = 0; j < workSize; j++) {
                int x = (int) (Integer.MAX_VALUE * Math.random());
                pq.insert(x);
                pq.remove();
            }
            stop = System.currentTimeMillis();
            System.out.println("n=" + pq.size() + "  Time: " + (stop - start));
            writer.println((stop - start));
            structureSize += increment;
        }


    }
}