/* this class was used to grade project #1.  Expected output:

101 100 99 98 97 96 95 94 93 92 91 90 89 88 87 86 85 84 83 82 81 80 79 78 77 76 75 74 73 72 71 70 69 68 67 66 65 64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1

1 2 3 4 5 6 7 8 9 10
Should not print anything before MARK
 ***** MARK *****
10 9 8 7 6 5 4 3 2 1 X
Size is 100000
100 99 98 97 6 5 4 3 2 1
Should not print anything before MARK, if so -10
 ***** MARK *****

 */


import data_structures.*;

public class Tester {
    private LinearListADT<String> list;

    public Tester() {
        list = new LinearLinkedList<String>();
        try {
            for(int i=0; i < 101; i++)
                list.addFirst(""+ (i+1));
            for(String s : list)
                System.out.print(s + " ");
            System.out.println("\n");
            for(int i=0; i < 101; i++)
                list.removeFirst();
        }
        catch(Exception e) {
            System.out.println("Block #1 " +e);
            e.printStackTrace();
        }
        try {
            for(int i=0; i < 10; i++)
                list.addLast(""+ (i+1));
            for(String s : list)
                System.out.print(s + " ");
            System.out.println();
        }
        catch(Exception e) {
            System.out.println("Block #2 " +e);
            e.printStackTrace();
        }
        try {
            list.clear();
            System.out.print("Should not print anything before MARK");
            for(String s : list)
                System.out.print(s + " ");
            System.out.println("\n ***** MARK *****");
            list.addLast("X");
            for(int i=0; i < 10; i++)
                list.insert(""+ (i+1),1);
            for(String s : list)
                System.out.print(s + " ");
            System.out.println();
            if(list.locate("X") != 11)
                System.out.println("ERROR, -10 location should be 11, but locate returned " + list.locate("X"));
            String tmp = list.remove("X");
            if(tmp.compareTo("X") != 0)
                System.out.println("ERROR, -10 remove should return 11, but remoe returned " + tmp);
            if(list.locate("X") != -1 )
                System.out.println("ERROR, -10 found removed item X");
            if(list.contains("X"))
                System.out.println("ERROR -10, found removed item X");
            list.clear();
            for(int i=0; i < 100000; i++)
                list.insert(i+"", (i+1));
            System.out.println("Size is " + list.size());
            list.clear();

            for(int i=0; i < 100;  i++)
                list.addFirst(""+(i+1));
            for(int i=0; i < 90;  i++)
                list.remove(5);
            for(String s : list)
                System.out.print(s + " ");
            System.out.println();
            for(int i=0; i < 10;  i++)
                list.remove(1);
            System.out.print("Should not print anything before MARK, if so -10");
            for(String s : list)
                System.out.print(s + " ");
            System.out.println("\n ***** MARK *****");
        }
        catch(Exception e) {
            System.out.println("Block #3 " +e);
            e.printStackTrace();
        }
    }

    public static void main(String [] args)  {
        new Tester();
    }
}