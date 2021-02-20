package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * William Fox cssc0917
 * Prog2, PriorityQueue, UnorderedArrayImplementation
 */
public class OrderedArrayPriorityQueue<E extends Comparable<E>> implements PriorityQueue<E> {
    E[] array;
    int size, capacity;
    long modificationCounter;

    public OrderedArrayPriorityQueue() {
        this(DEFAULT_MAX_CAPACITY);
    }

    public OrderedArrayPriorityQueue(int capacity) {
        this.capacity = capacity;
        array = (E[]) new Comparable[capacity];
        modificationCounter = size = 0;
    }

    public boolean insert(E object) {
        int index;
        if (isFull())
            return false;
        index = binSearchInsert(object, 0, size - 1);
        shift(index);
        array[index] = object;
        size++;
        modificationCounter++;
        return true;
    }

    public E remove() {
        if (isEmpty())
            return null;
        modificationCounter++;
        return array[--size];
    }

    public E peek() {
        if (isEmpty())
            return null;
        return array[size - 1];
    }

    public boolean contains(E obj) {
        return binSearch(obj, 0, size - 1) != -1;
    }

    public int size() {
        return size;
    }

    public void clear() {
        modificationCounter++;
        size = 0;
    }

    public boolean isEmpty() {
        return size == 0;
    }
    public boolean isFull() {
        return size == capacity;
    }

    public Iterator<E> iterator() {
        return new IteratorHelper();
    }

    private class IteratorHelper implements Iterator<E> {
        private int iterIndex;
        private long stateCheck;
        public IteratorHelper() {
            iterIndex = 0;
            stateCheck = modificationCounter;
        }
        public boolean hasNext() {
            if (stateCheck != modificationCounter) throw new ConcurrentModificationException();
            return iterIndex < size;
        }
        public E next() {
            if (!hasNext())
                throw new NoSuchElementException();
            return array[iterIndex++];
        }
    }
    //My Helper Methods are below
    //Returns Index to insert at
    private int binSearchInsert(E obj, int lo, int hi) {
        if (hi < lo) return lo;
        int mid = (lo + hi) / 2;
        int comp = obj.compareTo(array[mid]);
        if (comp >= 0) return binSearchInsert(obj, lo, --mid);
        return binSearchInsert(obj, ++mid, hi);
    }
    //Return index obj is at
    private int binSearch(E obj, int lo, int hi) {
        if (hi < lo) return -1;
        int mid = (lo + hi) / 2;
        int comp = obj.compareTo(array[mid]);
        if (comp == 0) return mid;
        if (comp > 0) return binSearch(obj, lo, --mid);
        return binSearch(obj, ++mid, hi);
    }
    private void shift(int index) {
        for (int i = size; i > index; i--)
            array[i] = array[i - 1];
    }
}//Eof
