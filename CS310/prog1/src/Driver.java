/*	CS310 Spring 2017
	Here is a simple driver program you can use to test your code.  If
	it fails to compile you have something wrong with your code.  Add
	additional statements to complete the testing.
*/


import data_structures.*;

public class Driver {
    public Driver() {
        runTests();
    }

    private void runTests() {
        LinearListADT<Integer> list = new LinearLinkedList<>();
        System.out.println(list.removeLast());
        System.out.println(list.removeFirst());
        System.out.println("Expected: Actual");
        System.out.println("True: " + list.isEmpty());
        System.out.println("0: " + list.size());
        list.addFirst(42);
        System.out.println("1: " + list.size());
        System.out.println("False: " + list.isEmpty());
        System.out.println("-1: " + list.locate(55) + " || 1: " + list.locate(42));
        System.out.println("42: " + list.removeLast());
        System.out.println("null: " + list.remove((Integer)17)); //Object isn't there
        list.addFirst(256);
        System.out.println("256: " + list.removeFirst());
        try {
            System.out.println("null: " + list.remove(23)); //Location isn't filled
        } catch (RuntimeException e) {
            System.out.println("Remove Object not present: Exception Properly thrown");
        }
        try {
            list.addFirst(128);
            System.out.println("128: " + list.get(1));
            list.remove((Integer)128);
            System.out.println(list.get(128));
        } catch (RuntimeException e) {
            System.out.println("Get Location isn't valid: Exception Properly thrown");
        }
        list.insert(1, 1);
        list.insert(2, 2);
        list.insert(3, 2);
        list.insert(4, 2);
        list.insert(5, 5);
        list.insert(6, 6);
        list.remove((Integer) 6);
        System.out.println("True: " + list.contains(3) + " || False: " + list.contains(528));

        for (int i = 1; i < 51; i++) {
            list.addFirst(i*5);
        }
        for (int i = 0; i < 51; i++) {
            list.removeFirst();
        }

        try {
            list.insert(2, 0);  // should throw an exception!
        } catch (RuntimeException e) {
            System.out.println("Inserting at 0: Exception Properly thrown");
        }
        try {
            list.insert(77777, list.size() + 2);  // should throw an exception!
        } catch (RuntimeException e) {
            System.out.println("Inserting above size: Exception Properly thrown");
        }
        list.addFirst(-1);
        list.addLast(-1);
        list.removeFirst();
        list.addFirst(-1);
        //Should print -1,1,4,3,2,5,-1
       for (int i : list)
           System.out.println(i);

        list.clear();
        for (int i : list) // should not print anything, nor crash
            System.out.println(i);

        for (int i = 0; i < 100; i++)
            list.insert((i + 1), 1);
        for (int i : list) // should print 100 .. 1
            System.out.print(i + " ");
        System.out.println();
    }

    public static void main(String[] args) {
        new Driver();
    }
}